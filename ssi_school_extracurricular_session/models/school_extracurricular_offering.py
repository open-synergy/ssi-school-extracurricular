# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolExtracurricularOffering(models.Model):
    """Adds session recap fields to the extracurricular offering.

    Before this module, an offering only knew who joined it and what
    it cost -- not whether any meeting had actually happened yet.
    These fields let a homeroom teacher see, at a glance, how many
    sessions have been scheduled and how many have already run.
    """

    _name = "school_extracurricular_offering"
    _inherit = [
        "school_extracurricular_offering",
    ]

    session_ids = fields.One2many(
        string="Sessions",
        comodel_name="school_extracurricular_session",
        inverse_name="offering_id",
        help="This offering's sessions across the term.",
    )
    session_count = fields.Integer(
        string="Session Count",
        compute="_compute_session_count",
        store=False,
        compute_sudo=True,
        help="Number of this offering's sessions, in any state.",
    )
    session_done_count = fields.Integer(
        string="Done Session Count",
        compute="_compute_session_done_count",
        store=False,
        compute_sudo=True,
        help="Number of this offering's sessions currently Done.",
    )

    @api.depends(
        "session_ids",
    )
    def _compute_session_count(self):
        """Count all of this offering's sessions.

        :return: nothing; assigns ``session_count``
        """
        for record in self:
            record.session_count = len(record.session_ids)

    @api.depends(
        "session_ids.state",
    )
    def _compute_session_done_count(self):
        """Count this offering's sessions currently Done.

        :return: nothing; assigns ``session_done_count``
        """
        for record in self:
            result = len(
                record.session_ids.filtered(lambda session: session.state == "done")
            )
            record.session_done_count = result
