# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CustomerInvoiceLine(models.Model):
    """Extends the invoice line with a trace back to its admission
    addendum line.

    ``admission_extra_detail_id`` is set when the line originates from
    a ``school_admission_payment_term_extra_detail`` addendum fee line
    (extracurricular fee charged to admission) instead of the
    admission's own payment template.
    """

    _inherit = "customer_invoice.line"

    admission_extra_detail_id = fields.Many2one(
        string="Admission Payment Term Extra Detail",
        comodel_name="school_admission_payment_term_extra_detail",
        readonly=True,
        ondelete="set null",
        help=(
            "The extracurricular admission addendum fee line this "
            "invoice line was generated from, if any."
        ),
    )
