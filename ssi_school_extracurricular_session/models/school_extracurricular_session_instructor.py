# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolExtracurricularSessionInstructor(models.Model):
    """Represents one instructor's roster line on one session.

    A session on its own only says who was assigned to run it
    (``teacher_id``/``coach_partner_id``); it says nothing about who
    else staffed the meeting -- an assistant instructor -- nor
    whether any of them actually showed up. This model is that
    per-meeting roster line, normally copied from the Offering's
    ``school_extracurricular_offering_instructor`` template when the
    session is created, with its own ``attendance_state`` left blank
    until recorded.
    """

    _name = "school_extracurricular_session_instructor"
    _description = "Extracurricular Session Instructor"
    _order = "session_id, sequence"

    session_id = fields.Many2one(
        string="Session",
        comodel_name="school_extracurricular_session",
        required=True,
        ondelete="cascade",
        help="The session's meeting this roster line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Used to order this session's instructor roster.",
    )
    role = fields.Selection(
        string="Role",
        selection=[
            ("head", "Head Instructor"),
            ("assistant", "Assistant Instructor"),
        ],
        required=True,
        default="head",
        help=(
            "Whether this person is the head instructor or an "
            "assistant instructor for this session's meeting."
        ),
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=False,
        help=(
            "The teacher identified by this roster line. Exactly one "
            "of Teacher or Contact must be filled."
        ),
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        ondelete="restrict",
        required=False,
        help=(
            "The person or institution identified by this roster "
            "line, when not a school Teacher (e.g. an external "
            "coach or assistant). Exactly one of Teacher or Contact "
            "must be filled."
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
        required=False,
        help=(
            "Whether this person was present at this meeting. Left "
            "blank until recorded -- an empty value means attendance "
            "has not been recorded yet, which is what the session's "
            "Done gate checks when the Offering tracks instructor "
            "attendance."
        ),
    )
    note = fields.Text(
        string="Note",
        help="Free-form notes about this instructor's attendance.",
    )

    @api.constrains("teacher_id", "partner_id")
    def _check_identity(self):
        """Validate that exactly one identity reference is filled.

        Rejects a line where both ``teacher_id`` and ``partner_id``
        are empty, and a line where both are filled -- exactly one of
        the two must identify the person on this roster line.

        :raises ValidationError: on zero or two identity references
            filled
        """
        for record in self.sudo():
            if not record.teacher_id and not record.partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular session instructor
Database ID: %s
Problem: Neither Teacher nor Contact is filled
Solution: Select either a Teacher or a Contact
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if record.teacher_id and record.partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular session instructor
Database ID: %s
Problem: Both Teacher and Contact are filled
Solution: Select only one of Teacher or Contact
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("session_id", "teacher_id", "partner_id")
    def _check_instructor_uniq(self):
        """Reject a second roster line for the same person in one session.

        :raises ValidationError: when another roster line on the same
            ``session_id`` already identifies the same ``teacher_id``
            or the same ``partner_id``
        """
        for record in self.sudo():
            if not record._check_instructor_uniq_condition():
                error_message = (
                    _(
                        """
Context: Set extracurricular session instructor
Database ID: %s
Problem: This person already has an instructor roster line on
Session '%s'
Solution: Select a person who does not yet have an instructor
roster line on this Session
"""
                    )
                    % (record.id, record.session_id.display_name)
                )
                raise ValidationError(error_message)

    def _check_instructor_uniq_condition(self):
        """Tell whether this line is the only one for its person.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.session_id:
            return True
        domain = [
            ("id", "!=", self.id),
            ("session_id", "=", self.session_id.id),
        ]
        if self.teacher_id:
            domain.append(("teacher_id", "=", self.teacher_id.id))
        elif self.partner_id:
            domain.append(("partner_id", "=", self.partner_id.id))
        else:
            return True
        duplicate = self.search(domain, limit=1)
        return not duplicate
