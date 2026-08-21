# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularPaymentTermDetail(
    models.Model
):  # pylint: disable=too-few-public-methods
    """Represents a product/fee line on a standalone payment term.

    Twin of ``school_enrollment_payment_term_detail`` (``ssi_school``),
    used by Route B standalone extracurricular billing instead of
    Route A's enrollment addendum. Inherits
    ``mixin.product_line_account``, which provides the standard
    product line fields (``name``, ``account_id``, ``uom_id``,
    ``uom_quantity``, ``price_unit``, ``tax_ids``, ``price_subtotal``,
    ``price_tax``, ``price_total``). Once the owning term is
    consolidated into a customer invoice, this line references the
    resulting ``customer_invoice.line`` through
    ``customer_invoice_line_id``.
    """

    _name = "school_extracurricular_payment_term_detail"
    _description = "School Extracurricular Payment Term Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
        "mixin.many2one_configurator",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_extracurricular_payment_term",
        ondelete="cascade",
        help="The extracurricular payment term that owns this fee line.",
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.participant_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the participant.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.participant_id.offering_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the "
        "participant's offering.",
    )
    customer_invoice_line_id = fields.Many2one(
        string="Customer Invoice Line",
        comodel_name="customer_invoice.line",
        readonly=True,
        ondelete="restrict",
        help="The customer invoice line linked to this detail, "
        "automatically populated when the customer invoice is generated.",
    )

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Extension point: override in a glue module to add extra line
        values. The link to the parent document
        (``customer_invoice_id``) is intentionally left out -- it is
        added by the create-due-invoice wizard, which owns the newly
        created header.

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
        }
