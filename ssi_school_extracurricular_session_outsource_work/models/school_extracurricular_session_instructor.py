# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularSessionInstructor(models.Model):
    """Adds outsource work configuration to the session roster line.

    Values are carried over from the offering's instructor template
    by ``school_extracurricular_session._prepare_session_instructor_data``.
    See ``school_extracurricular_offering_instructor`` for why the
    fields are not required at the field level.
    """

    _name = "school_extracurricular_session_instructor"
    _inherit = [
        "school_extracurricular_session_instructor",
    ]

    outsource_work_type_id = fields.Many2one(
        string="Outsource Work Type",
        comodel_name="outsource_work_type",
        ondelete="restrict",
        help=(
            "The Outsource Work Type -- and therefore the product -- "
            "used to build this person's honor document when this "
            "session is marked Done. Required only when this person "
            "is recorded present."
        ),
    )
    outsource_work_usage_id = fields.Many2one(
        string="Outsource Work Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help=(
            "The Usage resolving the accounting account of this "
            "person's honor document when this session is marked "
            "Done. Required only when this person is recorded "
            "present."
        ),
    )
