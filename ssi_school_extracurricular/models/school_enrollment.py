# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolEnrollment(models.Model):
    """Extends the enrollment to fold in extracurricular addendum lines.

    ``product_summary_ids`` and the payment term lock now also cover
    ``school_enrollment_payment_term_extra_detail`` rows, so
    extracurricular fees billed through Route A show up in the same
    places as the enrollment's own payment template lines. Revenue
    Recognition (``ssi_school``) is also extended to fold in both
    extracurricular billing routes -- the addendum fee line riding on
    the enrollment invoice (Route A), and the participant's own
    standalone invoice (Route B) -- so extracurricular fees invoiced
    alongside a tuition fee follow the same deferred-to-final
    recognition policy regardless of how they were billed.
    """

    _inherit = "school_enrollment"

    def _recompute_product_summaries(self):
        """Fold the addendum fee lines into the product summary.

        Runs ``super()`` first, which rebuilds ``product_summary_ids``
        from ``detail_ids`` alone, then merges every
        ``extra_detail_ids`` line into the resulting summary per
        product -- adding to an existing summary row when the product
        already has one, or creating a new row otherwise.

        :return: None
        """
        super()._recompute_product_summaries()
        Summary = self.env[  # pylint: disable=invalid-name
            "school_enrollment.product_summary"
        ]
        for record in self.sudo():
            extra_data = {}
            for term in record.payment_term_ids:
                for extra in term.extra_detail_ids:
                    pid = extra.product_id.id
                    if not pid:
                        continue
                    if pid not in extra_data:
                        extra_data[pid] = {
                            "uom_quantity": 0.0,
                            "amount_untaxed": 0.0,
                            "amount_tax": 0.0,
                            "amount_total": 0.0,
                        }
                    extra_data[pid]["uom_quantity"] += extra.uom_quantity
                    extra_data[pid]["amount_untaxed"] += extra.price_subtotal
                    extra_data[pid]["amount_tax"] += extra.price_tax
                    extra_data[pid]["amount_total"] += extra.price_total
            if not extra_data:
                continue
            existing = {
                summary.product_id.id: summary for summary in record.product_summary_ids
            }
            for pid, data in extra_data.items():
                if pid in existing:
                    summary = existing[pid]
                    summary.write(
                        {
                            "uom_quantity": summary.uom_quantity + data["uom_quantity"],
                            "amount_untaxed": summary.amount_untaxed
                            + data["amount_untaxed"],
                            "amount_tax": summary.amount_tax + data["amount_tax"],
                            "amount_total": summary.amount_total + data["amount_total"],
                        }
                    )
                else:
                    data["enrollment_id"] = record.id
                    data["product_id"] = pid
                    Summary.create(data)

    def _lock_payment_term(self):
        """Lock the addendum fee lines together with the payment terms.

        Runs ``super()`` first, then writes ``locked`` to ``True`` on
        every unlocked ``school_enrollment_payment_term_extra_detail``
        of this enrollment, passing ``bypass_addendum_lock`` in the
        context.

        :return: None
        """
        super()._lock_payment_term()
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_extra_detail"
        ]
        details = Detail.search(
            [
                ("term_id.enrollment_id", "=", self.id),
                ("locked", "=", False),
            ]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": True})

    def _unlock_payment_term(self):
        """Unlock the addendum fee lines together with the payment terms.

        Runs ``super()`` first, then writes ``locked`` to ``False`` on
        every locked ``school_enrollment_payment_term_extra_detail`` of
        this enrollment, passing ``bypass_addendum_lock`` in the
        context.

        :return: None
        """
        super()._unlock_payment_term()
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_extra_detail"
        ]
        details = Detail.search(
            [
                ("term_id.enrollment_id", "=", self.id),
                ("locked", "=", True),
            ]
        )
        if details:
            details.with_context(bypass_addendum_lock=True).write({"locked": False})

    def _check_revenue_recognition_readiness(self):
        """Extend the base readiness check with standalone invoices.

        Runs ``super()`` first -- which checks the Recognition Journal
        and the enrollment's own payment term invoices -- then also
        rejects when any non-cancelled extracurricular participant of
        this enrollment has a standalone payment term whose customer
        invoice is still ``draft``/``confirm``: that invoice never
        credited a temporary account, so it has nothing yet for the
        Recognition move to reclass.

        :raises UserError: when the journal is empty, when a payment
            term's own customer invoice is still draft/waiting for
            approval, or when a participant's standalone invoice is
            still draft/waiting for approval
        :return: None
        """
        self.ensure_one()
        super()._check_revenue_recognition_readiness()
        Participant = self.env[  # pylint: disable=invalid-name
            "school_extracurricular_participant"
        ]
        participants = Participant.search(
            [
                ("enrollment_id", "=", self.id),
                ("state", "!=", "cancel"),
            ]
        )
        draft_terms = participants.mapped("payment_term_ids").filtered(
            lambda term: term.customer_invoice_id
            and term.customer_invoice_id.state in ("draft", "confirm")
        )
        if draft_terms:
            error_message = (
                _(
                    """
Context: Finish enrollment
Database ID: %s
Problem: Extracurricular payment term '%s' has a customer invoice
that is not yet Unpaid/Paid
Solution: Confirm and open the standalone invoice before finishing
this enrollment
"""
                )
                % (self.id, draft_terms[0].name)
            )
            raise UserError(error_message)

    def _prepare_revenue_recognition_line_data(self):
        """Extend the base line data with both extracurricular routes.

        Runs ``super()`` first -- which covers the enrollment's own
        payment template details -- then appends one line per
        invoiced addendum fee line (Route A, charged to enrollment)
        and one line per invoiced standalone detail (Route B, separate
        invoice) that carries a Final Account different from the
        account already used on its own customer invoice line. Same
        selection and value rules as the base implementation.

        :return: list of dict of
            ``school_enrollment_revenue_recognition_line`` values
        """
        self.ensure_one()
        result = super()._prepare_revenue_recognition_line_data()
        ExtraDetail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_extra_detail"
        ]
        extra_details = ExtraDetail.search(
            [("term_id.enrollment_id", "=", self.id)]
        ).filtered(
            lambda extra: extra.customer_invoice_line_id
            and extra.customer_invoice_line_id.customer_invoice_id.state
            in ("open", "done")
            and extra.final_account_id
            and extra.final_account_id != extra.customer_invoice_line_id.account_id
        )
        for extra in extra_details:
            line = extra.customer_invoice_line_id
            result.append(
                {
                    "enrollment_id": self.id,
                    "name": extra.name,
                    "extra_detail_id": extra.id,
                    "debit_account_id": line.account_id.id,
                    "credit_account_id": extra.final_account_id.id,
                    "analytic_account_id": line.analytic_account_id.id,
                    "partner_id": line.partner_id.id,
                    "amount": line.price_subtotal,
                }
            )
        Participant = self.env[  # pylint: disable=invalid-name
            "school_extracurricular_participant"
        ]
        participants = Participant.search(
            [
                ("enrollment_id", "=", self.id),
                ("state", "!=", "cancel"),
            ]
        )
        standalone_details = participants.mapped(
            "payment_term_ids.detail_ids"
        ).filtered(
            lambda detail: detail.customer_invoice_line_id
            and detail.customer_invoice_line_id.customer_invoice_id.state
            in ("open", "done")
            and detail.final_account_id
            and detail.final_account_id != detail.customer_invoice_line_id.account_id
        )
        for detail in standalone_details:
            line = detail.customer_invoice_line_id
            result.append(
                {
                    "enrollment_id": self.id,
                    "name": detail.name,
                    "extracurricular_payment_term_detail_id": detail.id,
                    "debit_account_id": line.account_id.id,
                    "credit_account_id": detail.final_account_id.id,
                    "analytic_account_id": line.analytic_account_id.id,
                    "partner_id": line.partner_id.id,
                    "amount": line.price_subtotal,
                }
            )
        return result
