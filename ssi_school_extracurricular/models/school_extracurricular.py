# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricular(models.Model):  # pylint: disable=too-few-public-methods
    """Represents a single extracurricular activity offered by a school.

    Acts as the catalog entry that other documents (offering,
    participant, billing) will refer to. Restricting ``allowed_grade_ids``
    limits which grades may join; leaving it empty means every grade is
    allowed, not that none is.
    """

    _name = "school_extracurricular"
    _inherit = ["mixin.master_data"]
    _description = "Extracurricular"

    category_id = fields.Many2one(
        string="Category",
        comodel_name="school_extracurricular_category",
        required=True,
        ondelete="restrict",
        help="The category this extracurricular activity belongs to.",
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        required=True,
        ondelete="restrict",
        help="The school that offers this extracurricular activity.",
    )
    allowed_grade_ids = fields.Many2many(
        string="Allowed Grades",
        comodel_name="school_grade",
        relation="rel_school_extracurricular_2_grade",
        column1="extracurricular_id",
        column2="grade_id",
        help="Grades allowed to join this extracurricular activity. "
        "Leave empty to allow every grade, not to allow none.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        ondelete="restrict",
        help="Default coach/teacher in charge of this extracurricular " "activity.",
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        ondelete="restrict",
        help="Default product used to bill the fee of this "
        "extracurricular activity.",
    )
