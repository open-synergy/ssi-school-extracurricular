# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SchoolExtracurricularOffering(models.Model):
    """Extends the offering with the admission billing mode.

    Adds ``admission`` to ``billing_mode`` so an offering can be set up
    to be billed through a student's admission payment term instead of
    an enrollment. Every participant created from an offering in this
    mode copies the value the same way it already copies ``enrollment``
    or ``standalone``.
    """

    _inherit = "school_extracurricular_offering"

    billing_mode = fields.Selection(
        selection_add=[("admission", "Charged to Admission")],
        ondelete={"admission": "set default"},
    )
