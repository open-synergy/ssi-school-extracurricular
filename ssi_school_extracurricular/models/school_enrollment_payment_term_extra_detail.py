# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError

# The only fields ever blocked by the addendum lock -- see
# ``_check_addendum_lock``. Every other field (including
# ``final_usage_id``/``final_account_id``) stays freely writable
# regardless of ``locked``; only the temporary account classification
# itself is frozen, and only once the line is invoiced.
CONDITIONAL_LOCK_FIELDS = {"usage_id", "account_id"}


class SchoolEnrollmentPaymentTermExtraDetail(models.Model):
    """Represents one addendum fee line billed through a payment term.

    Twin of ``school_enrollment_payment_term_detail`` (``ssi_school``),
    but sourced from an extracurricular participant's allocation
    instead of the enrollment's own payment template. One row is
    created per ``school_extracurricular_participant_allocation`` when
    the participant is opened, and it is what makes the participant's
    fee show up on the payment term's totals and, eventually, on the
    customer invoice created from that term.
    """

    _name = "school_enrollment_payment_term_extra_detail"
    _description = "School Enrollment Payment Term Extra Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
        "mixin.many2one_configurator",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        ondelete="cascade",
        help="The enrollment payment term that owns this addendum fee line.",
    )
    participant_id = fields.Many2one(
        string="Extracurricular Participant",
        comodel_name="school_extracurricular_participant",
        required=True,
        ondelete="cascade",
        help="The extracurricular participant this fee line was billed from.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.enrollment_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the enrollment.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.enrollment_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the enrollment.",
    )
    customer_invoice_line_id = fields.Many2one(
        string="Customer Invoice Line",
        comodel_name="customer_invoice.line",
        readonly=True,
        ondelete="restrict",
        help=(
            "The customer invoice line linked to this addendum fee line, "
            "automatically populated when the customer invoice is "
            "generated."
        ),
    )
    locked = fields.Boolean(
        string="Locked",
        default=False,
        readonly=True,
        copy=False,
        help=(
            "Automatically set to True when the enrollment is opened. "
            "Locked addendum fee lines can no longer be edited or "
            "deleted."
        ),
    )
    final_usage_id = fields.Many2one(
        string="Final Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help=(
            "Usage used to auto-fill Final Account from the product's "
            "account configuration. Copied from the originating "
            "allocation when this line is created."
        ),
    )
    final_account_id = fields.Many2one(
        string="Final Account",
        comodel_name="account.account",
        ondelete="restrict",
        help=(
            "Revenue account this line is recognized to once the "
            "enrollment finishes and Revenue Recognition posts. "
            "Copied from the originating allocation when this line is "
            "created. Left empty, this line is never recognized."
        ),
    )

    def _check_addendum_lock(self, vals):
        """Reject re-classifying an invoiced, locked addendum fee line.

        The only thing the addendum lock ever freezes is the
        temporary account classification (``usage_id``/
        ``account_id``), and only once the line is already invoiced:
        an invoice line was generated from that account, so changing
        it afterwards would desynchronize the two. Every other field
        -- including ``final_usage_id``/``final_account_id`` -- stays
        freely writable no matter ``locked``, matching the Design
        Decision of the issue this guard was written for. The write
        also passes unconditionally when the context carries
        ``bypass_addendum_lock``.

        :param vals: write values whose keys are checked against
            ``CONDITIONAL_LOCK_FIELDS``
        :raises UserError: when ``usage_id``/``account_id`` is
            written on a locked, already invoiced line
        :return: None
        """
        if self.env.context.get("bypass_addendum_lock"):
            return
        if not set(vals.keys()) & CONDITIONAL_LOCK_FIELDS:
            return
        for record in self:
            if record.locked and record.customer_invoice_line_id:
                error_message = (
                    _(
                        """
Context: Update payment term extra detail
Database ID: %s
Problem: Payment term extra detail '%s' is already invoiced and its
account classification cannot be changed
Solution: The invoiced amount is already booked on the current
account; book a correction through the extracurricular participant
instead
"""
                    )
                    % (record.id, record.name)
                )
                raise UserError(error_message)

    def write(self, vals):
        """Enforce the addendum lock before writing.

        :param vals: values to write
        :raises UserError: when ``usage_id``/``account_id`` is
            written on a locked, already invoiced line
        :return: ``True``
        """
        self._check_addendum_lock(vals)
        return super().write(vals)

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Twin of
        ``school_enrollment_payment_term_detail._prepare_invoice_line``,
        with ``extra_detail_id`` added so the created invoice line can
        be traced back to this addendum fee line. When the owning
        enrollment already finished (``done``) with Revenue
        Recognition enabled and this line carries a Final Account, a
        due invoice created after the fact bills straight to that
        Final Account instead of the line's own temporary account --
        there is no later Revenue Recognition move to reclass it.

        :return: dict of ``customer_invoice.line`` values
        """
        self.ensure_one()
        aa = (  # pylint: disable=invalid-name,consider-using-ternary
            self.analytic_account_id and self.analytic_account_id.id or False
        )
        enrollment = self.term_id.enrollment_id
        account = self.account_id
        if (
            enrollment.state == "done"
            and enrollment.revenue_recognition
            and self.final_account_id
        ):
            account = self.final_account_id
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": account.id,
            "uom_id": self.uom_id.id,
            "uom_quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa or False,
            "extra_detail_id": self.id,
        }
