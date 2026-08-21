# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularCategory(
    models.Model
):  # pylint: disable=too-few-public-methods
    """Represents a group under which extracurricular catalog entries sit.

    Used to classify extracurricular activities, e.g. Sport, Art, Science
    Club. Each extracurricular activity belongs to one category.
    """

    _name = "school_extracurricular_category"
    _inherit = ["mixin.master_data"]
    _description = "Extracurricular Category"
    _order = "sequence asc, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        required=True,
        help="Display order of the category. Lower values appear first " "in the list.",
    )
