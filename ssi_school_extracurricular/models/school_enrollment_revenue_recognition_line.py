# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentRevenueRecognitionLine(models.Model):
    # Extends the recognition line with extracurricular origins.
    #
    # ``payment_term_detail_id`` (``ssi_school``) only traces a line
    # back to the enrollment's own payment template. Extracurricular
    # fees are billed through two other lines -- the addendum fee
    # line riding on the enrollment invoice, or the participant's
    # own standalone detail -- so a Recognition Line originating
    # from either of those needs its own trace field instead.

    _inherit = "school_enrollment_revenue_recognition_line"

    extra_detail_id = fields.Many2one(
        string="Payment Term Extra Detail",
        comodel_name="school_enrollment_payment_term_extra_detail",
        ondelete="restrict",
        help=(
            "The invoiced addendum fee line (Route A, charged to "
            "enrollment) this Recognition Line releases."
        ),
    )
    extracurricular_payment_term_detail_id = fields.Many2one(
        string="Extracurricular Payment Term Detail",
        comodel_name="school_extracurricular_payment_term_detail",
        ondelete="restrict",
        help=(
            "The invoiced standalone detail line (Route B, separate "
            "invoice) this Recognition Line releases."
        ),
    )
