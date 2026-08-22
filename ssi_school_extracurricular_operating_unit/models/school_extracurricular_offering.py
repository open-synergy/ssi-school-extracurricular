# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularOffering(models.Model):
    """Extends School Extracurricular Offering with single Operating Unit.

    Adds ``operating_unit_id`` (via ``mixin.single_operating_unit``) so
    an offering can be scoped to one operating unit; visibility is then
    narrowed by this module's record rule. This document is the root of
    the extracurricular Operating Unit -- it does not itself derive its
    Operating Unit from anything else, but every fee-bearing document it
    is joined by (``school_extracurricular_participant``) copies its
    Operating Unit from here via onchange.
    """

    _name = "school_extracurricular_offering"
    _inherit = [
        "school_extracurricular_offering",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
