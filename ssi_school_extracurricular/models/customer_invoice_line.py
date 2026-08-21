# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomerInvoiceLine(models.Model):
    """Extends the invoice line with a trace back to its addendum line.

    ``extra_detail_id`` is set when the line originates from a
    ``school_enrollment_payment_term_extra_detail`` addendum fee line
    (Route A extracurricular billing) instead of the enrollment's own
    payment template.
    """

    _inherit = "customer_invoice.line"

    extra_detail_id = fields.Many2one(
        string="Payment Term Extra Detail",
        comodel_name="school_enrollment_payment_term_extra_detail",
        readonly=True,
        ondelete="set null",
        help=(
            "The extracurricular addendum fee line this invoice line "
            "was generated from, if any."
        ),
    )
