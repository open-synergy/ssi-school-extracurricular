# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolEnrollment(models.Model):
    """Extends the enrollment to fold in extracurricular addendum lines.

    ``product_summary_ids`` and the payment term lock now also cover
    ``school_enrollment_payment_term_extra_detail`` rows, so
    extracurricular fees billed through Route A show up in the same
    places as the enrollment's own payment template lines.
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
