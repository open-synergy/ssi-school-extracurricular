# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolEnrollmentPaymentTermExtraDetail(models.Model):
    """Extends the addendum fee line with single Operating Unit.

    ``school_enrollment_payment_term_extra_detail`` is local to
    ``ssi_school_extracurricular`` (no other repository's glue module
    ever inherits it), so this is the only place it can gain an
    Operating Unit field. The value itself is never derived here --
    ``school_extracurricular_participant._10_create_extra_detail``
    (this module) writes it right after each line is created, copying
    the owning Participant's Operating Unit.
    """

    _name = "school_enrollment_payment_term_extra_detail"
    _inherit = [
        "school_enrollment_payment_term_extra_detail",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
    )
