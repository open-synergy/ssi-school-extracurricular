# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularOfferingInstructor(models.Model):
    """Adds outsource work configuration to the instructor template.

    ``outsource_work_type_id`` and ``outsource_work_usage_id`` are not
    required at the field level -- a school that does not pay honor
    through this module must still be able to use the roster -- so
    the requirement is enforced by a structured ``UserError`` when an
    honor is actually built (see
    ``school_extracurricular_session._done``).
    """

    _name = "school_extracurricular_offering_instructor"
    _inherit = [
        "school_extracurricular_offering_instructor",
    ]

    outsource_work_type_id = fields.Many2one(
        string="Outsource Work Type",
        comodel_name="outsource_work_type",
        ondelete="restrict",
        help=(
            "The Outsource Work Type -- and therefore the product -- "
            "used to build this person's honor document. Copied onto "
            "every session generated from this offering. Required "
            "only when the session is marked Done with this person "
            "recorded present."
        ),
    )
    outsource_work_usage_id = fields.Many2one(
        string="Outsource Work Usage",
        comodel_name="product.usage_type",
        ondelete="restrict",
        help=(
            "The Usage resolving the accounting account of this "
            "person's honor document. Copied onto every session "
            "generated from this offering. Required only when the "
            "session is marked Done with this person recorded "
            "present."
        ),
    )
