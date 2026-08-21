# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


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

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Twin of
        ``school_enrollment_payment_term_detail._prepare_invoice_line``,
        with ``extra_detail_id`` added so the created invoice line can
        be traced back to this addendum fee line.

        :return: dict of ``customer_invoice.line`` values
        """
        self.ensure_one()
        aa = (  # pylint: disable=invalid-name,consider-using-ternary
            self.analytic_account_id and self.analytic_account_id.id or False
        )
        return {
            "product_id": self.product_id.id,
            "name": self.name,
            "account_id": self.account_id.id,
            "uom_id": self.uom_id.id,
            "uom_quantity": self.uom_quantity,
            "price_unit": self.price_unit,
            "tax_ids": [(6, 0, self.tax_ids.ids)],
            "analytic_account_id": aa or False,
            "extra_detail_id": self.id,
        }
