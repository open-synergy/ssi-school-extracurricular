# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolAdmissionPaymentTermExtraDetail(models.Model):
    """Represents one addendum fee line billed through an admission
    payment term.

    Twin of ``school_admission_payment_term_detail``
    (``ssi_school_admission``) and of
    ``school_enrollment_payment_term_extra_detail``
    (``ssi_school_extracurricular``), but sourced from an
    extracurricular participant's admission allocation instead of the
    admission's own payment template. One row is created per
    ``school_extracurricular_participant_admission_allocation`` when
    the participant is opened, and it is what makes the participant's
    fee show up on the admission payment term's totals and,
    eventually, on the customer invoice created from that term. Unlike
    its enrollment sibling, this line has no ``locked`` flag: an
    admission's payment terms are already ``locked`` once the
    admission is open, and a participant billed to admission can only
    be opened after the admission itself is already open.
    """

    _name = "school_admission_payment_term_extra_detail"
    _description = "School Admission Payment Term Extra Detail"
    _order = "sequence, product_category_id, product_id, id"
    _inherit = [
        "mixin.product_line_account",
    ]

    term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_admission_payment_term",
        ondelete="cascade",
        help="The admission payment term that owns this addendum fee line.",
    )
    participant_id = fields.Many2one(
        string="Extracurricular Participant",
        comodel_name="school_extracurricular_participant",
        required=True,
        ondelete="cascade",
        help="The extracurricular participant this fee line was billed from.",
    )
    product_id = fields.Many2one(required=True)
    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        related="term_id.admission_id",
        store=True,
        help="The admission owning the payment term of this addendum fee line.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="term_id.admission_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the admission.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        related="term_id.admission_id.pricelist_id",
        store=True,
        help="The pricelist used, automatically taken from the admission.",
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

    @api.model
    def create(self, vals):
        """Create the addendum line and refresh the product summary.

        Overridden so the aggregated ``product_summary_ids`` of the
        owning admission stays in sync with its addendum fee lines,
        mirroring ``school_admission_payment_term_detail.create``.

        :param vals: values of the addendum line to create
        :return: the created record
        """
        record = super().create(vals)
        admission = record.term_id.admission_id
        if admission:
            admission._recompute_product_summary()  # pylint: disable=protected-access
        return record

    def unlink(self):
        """Delete the addendum line and refresh the product summary.

        Overridden so the aggregated ``product_summary_ids`` of the
        owning admission stays in sync once the addendum fee line is
        removed, mirroring ``school_admission_payment_term_detail.unlink``.

        :return: ``True``
        """
        admissions = self.mapped("term_id.admission_id")
        result = super().unlink()
        admissions._recompute_product_summary()  # pylint: disable=protected-access
        return result

    def _prepare_invoice_line(self):
        """Build the ``customer_invoice.line`` values for this fee line.

        Twin of
        ``school_admission_payment_term_detail._prepare_invoice_line``,
        with ``admission_extra_detail_id`` added so the created invoice
        line can be traced back to this addendum fee line.

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
            "admission_extra_detail_id": self.id,
        }
