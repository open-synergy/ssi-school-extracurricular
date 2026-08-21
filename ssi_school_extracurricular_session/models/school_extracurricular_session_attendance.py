# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolExtracurricularSessionAttendance(models.Model):
    """Represents one participant's attendance at one session.

    A session on its own only says a meeting happened; it does not
    say who showed up. This model is the join between a Session and
    the Participants of its Offering, one line per participant per
    session, so schools can produce attendance reports and prove the
    meetings they bill for actually took place.
    """

    _name = "school_extracurricular_session_attendance"
    _description = "Extracurricular Session Attendance"
    _order = "session_id, id"

    _sql_constraints = [
        (
            "session_participant_uniq",
            "unique(session_id, participant_id)",
            "A participant can only have one attendance line per " "session.",
        ),
    ]

    session_id = fields.Many2one(
        string="Session",
        comodel_name="school_extracurricular_session",
        required=True,
        ondelete="cascade",
        help="The session's meeting this attendance line belongs to.",
    )
    participant_id = fields.Many2one(
        string="Participant",
        comodel_name="school_extracurricular_participant",
        required=True,
        ondelete="restrict",
        help=(
            "The participant this attendance line is for. Must have "
            "joined the same Offering as the Session."
        ),
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        related="participant_id.student_id",
        store=True,
        compute_sudo=True,
        help=(
            "The student attending, automatically populated from the "
            "selected Participant."
        ),
    )
    attendance_state = fields.Selection(
        string="Attendance",
        selection=[
            ("present", "Present"),
            ("absent", "Absent"),
            ("excused", "Excused"),
            ("late", "Late"),
        ],
        required=True,
        default="present",
        help="Whether the participant was present at this meeting.",
    )
    note = fields.Text(
        string="Note",
        help="Free-form notes about this participant's attendance.",
    )

    @api.constrains("session_id", "participant_id")
    def _check_participant_offering(self):
        """Reject an attendance line for a participant of another offering.

        :raises ValidationError: when ``participant_id.offering_id``
            differs from ``session_id.offering_id``
        """
        for record in self.sudo():
            if not record._check_participant_offering_condition():
                error_message = (
                    _(
                        """
Context: Set extracurricular session attendance participant
Database ID: %s
Problem: Participant '%s' does not belong to the Offering of Session
'%s'
Solution: Select a Participant who joined the same Offering as the
Session
"""
                    )
                    % (
                        record.id,
                        record.participant_id.display_name,
                        record.session_id.display_name,
                    )
                )
                raise ValidationError(error_message)

    def _check_participant_offering_condition(self):
        """Tell whether the participant belongs to the session's offering.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.session_id or not self.participant_id:
            return True
        return self.session_id.offering_id == self.participant_id.offering_id
