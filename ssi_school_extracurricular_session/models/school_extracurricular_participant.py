# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SchoolExtracurricularParticipant(models.Model):
    """Adds session attendance recap fields to the participant.

    Once sessions are filled with attendance, nothing on the
    participant itself said how the student was actually doing --
    how many meetings ran, and how many the student showed up to.
    These read-only fields answer that without leaving the
    participant record.
    """

    _name = "school_extracurricular_participant"
    _inherit = [
        "school_extracurricular_participant",
    ]

    session_planned_count = fields.Integer(
        string="Planned Session",
        compute="_compute_session_planned_count",
        store=False,
        compute_sudo=True,
        help="Number of the Offering's sessions currently Planned.",
    )
    session_done_count = fields.Integer(
        string="Done Session",
        compute="_compute_session_done_count",
        store=False,
        compute_sudo=True,
        help="Number of the Offering's sessions currently Done.",
    )
    attendance_present_count = fields.Integer(
        string="Present Count",
        compute="_compute_attendance_present_count",
        store=False,
        compute_sudo=True,
        help=(
            "Number of this participant's attendance lines marked "
            "Present or Late on a Done session."
        ),
    )
    attendance_rate = fields.Float(
        string="Attendance Rate",
        compute="_compute_attendance_rate",
        store=False,
        compute_sudo=True,
        help=(
            "Percentage of the Offering's Done sessions this "
            "participant was Present or Late for. 0 when the "
            "Offering has no Done session yet."
        ),
    )

    @api.depends(
        "offering_id.session_ids.state",
    )
    def _compute_session_planned_count(self):
        """Count the Offering's sessions currently Planned.

        :return: nothing; assigns ``session_planned_count``
        """
        for record in self:
            result = len(
                record.offering_id.session_ids.filtered(
                    lambda session: session.state == "planned"
                )
            )
            record.session_planned_count = result

    @api.depends(
        "offering_id.session_ids.state",
    )
    def _compute_session_done_count(self):
        """Count the Offering's sessions currently Done.

        :return: nothing; assigns ``session_done_count``
        """
        for record in self:
            result = len(
                record.offering_id.session_ids.filtered(
                    lambda session: session.state == "done"
                )
            )
            record.session_done_count = result

    @api.depends(
        "offering_id.session_ids.state",
        "offering_id.session_ids.attendance_ids.attendance_state",
        "offering_id.session_ids.attendance_ids.participant_id",
    )
    def _compute_attendance_present_count(self):
        """Count this participant's Present/Late lines on Done sessions.

        :return: nothing; assigns ``attendance_present_count``
        """
        for record in self:
            result = 0
            done_sessions = record.offering_id.session_ids.filtered(
                lambda session: session.state == "done"
            )
            for session in done_sessions:
                lines = session.attendance_ids.filtered(
                    lambda line, record=record: (
                        line.participant_id == record
                        and line.attendance_state in ("present", "late")
                    )
                )
                result += len(lines)
            record.attendance_present_count = result

    @api.depends(
        "attendance_present_count",
        "session_done_count",
    )
    def _compute_attendance_rate(self):
        """Compute the percentage of Done sessions attended.

        Returns ``0.0`` when the Offering has no Done session yet,
        instead of raising a division error.

        :return: nothing; assigns ``attendance_rate``
        """
        for record in self:
            result = 0.0
            if record.session_done_count:
                result = (
                    record.attendance_present_count / record.session_done_count * 100
                )
            record.attendance_rate = result
