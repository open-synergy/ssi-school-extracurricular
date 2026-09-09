# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolExtracurricularSession(models.Model):
    """Represents one meeting of an extracurricular offering.

    ``school_extracurricular_offering`` and
    ``school_extracurricular_participant`` record who is enrolled in
    an activity and what it costs, but neither says anything about
    how the activity actually runs term to term: when a meeting
    happened, who attended it, and whether the number of meetings
    billed to a family actually took place. This model is that
    per-meeting record.

    It is deliberately NOT a full SSI transaction document. It is a
    high-volume operational record (dozens per offering per term)
    whose approval already happened at the Offering level, so it
    uses a plain three-value ``state`` instead of the multi-approval
    mixins, and has no sequence, approval, or policy template.
    """

    _name = "school_extracurricular_session"
    _description = "Extracurricular Session"
    _order = "date, time_start, id"

    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        required=True,
        ondelete="cascade",
        help="The term's offering this session is a meeting of.",
    )
    extracurricular_id = fields.Many2one(
        string="Extracurricular",
        comodel_name="school_extracurricular",
        related="offering_id.extracurricular_id",
        store=True,
        compute_sudo=True,
        help=(
            "The extracurricular activity being run, automatically "
            "populated from the selected Offering."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        related="offering_id.school_id",
        store=True,
        compute_sudo=True,
        help=(
            "The school running this session, automatically "
            "populated from the selected Offering."
        ),
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="offering_id.academic_term_id",
        store=True,
        compute_sudo=True,
        help=(
            "The academic term this session belongs to, automatically "
            "populated from the selected Offering."
        ),
    )
    date = fields.Date(
        string="Date",
        required=True,
        help="The date this session's meeting takes place.",
    )
    time_start = fields.Float(
        string="Start Time",
        required=True,
        help="The time this session's meeting starts.",
    )
    time_end = fields.Float(
        string="End Time",
        required=True,
        help=(
            "The time this session's meeting ends. Must be later "
            "than the Start Time."
        ),
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=False,
        help=(
            "The coach/teacher running this session's meeting. "
            "Defaults to the Offering's Teacher when the Offering is "
            "selected, but may be changed. Exactly one of Teacher or "
            "External Coach must be filled."
        ),
    )
    coach_partner_id = fields.Many2one(
        string="External Coach",
        comodel_name="res.partner",
        ondelete="restrict",
        required=False,
        help=(
            "The external coach (person or institution, not a school "
            "employee) running this session's meeting. Defaults to the "
            "Offering's External Coach when the Offering is selected, "
            "but may be changed. Exactly one of Teacher or External "
            "Coach must be filled."
        ),
    )
    location = fields.Char(
        string="Location",
        help="Where this session's meeting takes place.",
    )
    topic = fields.Char(
        string="Topic",
        help="A short label for what this session's meeting covers.",
    )
    description = fields.Text(
        string="Description",
        help="Free-form notes about this session's meeting.",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("planned", "Planned"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        default="planned",
        readonly=True,
        copy=False,
        help=(
            "Planned = the meeting has not happened yet or is being "
            "recorded. Done = the meeting took place and its "
            "attendance is final. Cancelled = the meeting did not "
            "take place."
        ),
    )
    cancel_reason = fields.Text(
        string="Cancel Reason",
        readonly=True,
        help="Why this session's meeting was cancelled.",
    )
    attendance_ids = fields.One2many(
        string="Attendance",
        comodel_name="school_extracurricular_session_attendance",
        inverse_name="session_id",
        help="The attendance of each participant at this meeting.",
    )
    instructor_ids = fields.One2many(
        string="Instructors",
        comodel_name="school_extracurricular_session_instructor",
        inverse_name="session_id",
        help=(
            "The instructors staffing this session's meeting, copied "
            "from the Offering's Instructor roster when this session "
            "is created, either through the form or through the "
            "session generator."
        ),
    )

    @api.onchange("offering_id")
    def onchange_teacher_id(self):
        self.teacher_id = False
        if self.offering_id:
            self.teacher_id = self.offering_id.teacher_id

    @api.onchange("offering_id")
    def onchange_coach_partner_id(self):
        self.coach_partner_id = False
        if self.offering_id:
            self.coach_partner_id = self.offering_id.coach_partner_id

    @api.onchange("offering_id")
    def onchange_instructor_ids(self):
        """Copy the Offering's Instructor roster onto a new session.

        Runs only while ``instructor_ids`` is still empty, so a user
        who already edited the roster by hand before changing the
        Offering does not have their edits silently discarded.

        :return: None
        """
        if self.offering_id and not self.instructor_ids:
            self.instructor_ids = [
                (0, 0, self._prepare_session_instructor_data(template_line))
                for template_line in self.offering_id.instructor_ids
            ]

    @api.constrains("teacher_id", "coach_partner_id")
    def _check_coach(self):
        """Validate that exactly one coach reference is filled.

        Rejects a record where both ``teacher_id`` and
        ``coach_partner_id`` are empty, and a record where both are
        filled -- exactly one of the two must identify the coach
        running this session's meeting.

        :raises ValidationError: on zero or two coach references filled
        :return: None
        """
        for record in self.sudo():
            if not record.teacher_id and not record.coach_partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular session coach
Database ID: %s
Problem: Neither Teacher nor External Coach is filled
Solution: Select either a Teacher or an External Coach
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if record.teacher_id and record.coach_partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular session coach
Database ID: %s
Problem: Both Teacher and External Coach are filled
Solution: Select only one of Teacher or External Coach
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("time_start", "time_end")
    def _check_time_start_end(self):
        """Reject a session whose end time is not after its start.

        :raises ValidationError: when ``time_end`` is not later than
            ``time_start``
        """
        for record in self.sudo():
            if not record._check_time_start_end_condition():
                error_message = (
                    _(
                        """
Context: Set extracurricular session time
Database ID: %s
Problem: End Time '%s' is not later than Start Time '%s'
Solution: Select an End Time that is later than the Start Time
"""
                    )
                    % (record.id, record.time_end, record.time_start)
                )
                raise ValidationError(error_message)

    def _check_time_start_end_condition(self):
        """Tell whether ``time_end`` is later than ``time_start``.

        :return: True when valid; never raises
        """
        self.ensure_one()
        return self.time_end > self.time_start

    @api.constrains("date", "offering_id")
    def _check_date_within_offering(self):
        """Reject a session date outside its offering's period.

        :raises ValidationError: when ``date`` falls outside the
            offering's ``date_start``/``date_end`` range
        """
        for record in self.sudo():
            if not record._check_date_within_offering_condition():
                error_message = (
                    _(
                        """
Context: Set extracurricular session date
Database ID: %s
Problem: Date '%s' is outside Offering '%s' period ('%s' - '%s')
Solution: Select a Date between the Offering's Start Date and End
Date
"""
                    )
                    % (
                        record.id,
                        record.date,
                        record.offering_id.name,
                        record.offering_id.date_start,
                        record.offering_id.date_end,
                    )
                )
                raise ValidationError(error_message)

    def _check_date_within_offering_condition(self):
        """Tell whether ``date`` falls within the offering's period.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.date or not self.offering_id:
            return True
        if not self.offering_id.date_start or not self.offering_id.date_end:
            return True
        return self.offering_id.date_start <= self.date <= self.offering_id.date_end

    @api.model
    def create(self, vals):
        """Create a session, copying the Offering's Instructor roster.

        Side effect: when ``instructor_ids`` is not given in ``vals``,
        populates it from the selected Offering's Instructor roster
        via ``_prepare_session_instructor_data`` -- the same
        extension point used by ``onchange_instructor_ids``, so the
        session generator wizard is served automatically without
        being touched.

        :param vals: values for the new record
        :return: the created record
        :rtype: recordset
        """
        if vals.get("offering_id") and "instructor_ids" not in vals:
            offering = self.env["school_extracurricular_offering"].browse(
                vals["offering_id"]
            )
            vals["instructor_ids"] = [
                (0, 0, self._prepare_session_instructor_data(template_line))
                for template_line in offering.instructor_ids
            ]
        return super().create(vals)

    def _prepare_session_instructor_data(self, template_line):
        """Build the values of one session instructor line.

        Extension point: override to carry extra fields from the
        Offering's ``school_extracurricular_offering_instructor``
        template line into the generated
        ``school_extracurricular_session_instructor`` line. Called
        once per template line, both by ``onchange_instructor_ids``
        and by ``create()`` -- do not inline this into either caller.

        :param template_line: the
            ``school_extracurricular_offering_instructor`` template
            line being copied
        :return: dict of ``school_extracurricular_session_instructor``
            values, without ``session_id``
        """
        return {
            "sequence": template_line.sequence,
            "role": template_line.role,
            "teacher_id": template_line.teacher_id.id,
            "partner_id": template_line.partner_id.id,
        }

    def action_done(self):
        """Mark this session's meeting as done.

        :return: nothing; rejected when the Offering's tracked
            attendance is not recorded
        """
        for record in self.sudo():
            record._done()

    def _done(self):
        """Move this session to ``done``.

        The gate is conditional on the Offering's two tracking
        switches: neither is checked unconditionally, matching what
        the Offering declares it administers.

        Side effect: writes ``state`` on this session.

        :raises UserError: when ``participant_attendance_tracked`` is
            enabled and ``attendance_ids`` is empty, or when
            ``instructor_attendance_tracked`` is enabled and
            ``instructor_ids`` is empty or has a line with a blank
            ``attendance_state``
        """
        self.ensure_one()
        if self.offering_id.participant_attendance_tracked and not self.attendance_ids:
            error_message = (
                _(
                    """
Context: Mark extracurricular session as done
Database ID: %s
Problem: Session has no attendance line
Solution: Record at least one attendance line before marking the
session as done
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        if self.offering_id.instructor_attendance_tracked:
            if not self.instructor_ids:
                error_message = (
                    _(
                        """
Context: Mark extracurricular session as done
Database ID: %s
Problem: Session has no instructor roster line
Solution: Record at least one instructor roster line before marking
the session as done
"""
                    )
                    % (self.id,)
                )
                raise UserError(error_message)
            unset_attendance = self.instructor_ids.filtered(
                lambda line: not line.attendance_state
            )
            if unset_attendance:
                error_message = (
                    _(
                        """
Context: Mark extracurricular session as done
Database ID: %s
Problem: An instructor roster line has no Attendance recorded
Solution: Record the Attendance of every instructor roster line
before marking the session as done
"""
                    )
                    % (self.id,)
                )
                raise UserError(error_message)
        self.write({"state": "done"})

    def action_cancel(self):
        """Open the Cancel Reason wizard for this session.

        :return: an ``ir.actions.act_window`` dict opening the wizard
        """
        for record in self.sudo():
            result = record._open_cancel_wizard()
        return result

    def _open_cancel_wizard(self):
        """Build the window action opening the cancel reason wizard.

        :return: an ``ir.actions.act_window`` dict, pre-filled with
            this session via the ``default_session_id`` context key
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Cancel Session",
            "res_model": "cancel_extracurricular_session",
            "view_mode": "form",
            "target": "new",
            "context": {"default_session_id": self.id},
        }

    def _cancel(self, cancel_reason):
        """Move this session to ``cancelled`` with the given reason.

        Extension point: called by
        ``cancel_extracurricular_session.action_confirm`` instead of
        that wizard writing to this session directly, so other
        modules may override it to react to a session being
        cancelled.

        Side effect: writes ``state`` and ``cancel_reason`` on this
        session.

        :param cancel_reason: the reason text supplied by the wizard
        :return: None
        """
        self.ensure_one()
        self.write(
            {
                "state": "cancelled",
                "cancel_reason": cancel_reason,
            }
        )

    def action_fill_attendance(self):
        """Fill this session's attendance from its active participants.

        Creates one ``present`` attendance line for every Offering
        participant currently ``open`` and active on this session's
        date. A participant that already has a line on this session
        is skipped, so the button stays idempotent.

        :raises UserError: when this session is not ``planned``
        :return: nothing
        """
        for record in self.sudo():
            record._fill_attendance()

    def _fill_attendance(self):
        """Create attendance lines for this session's active participants.

        Side effect: creates
        ``school_extracurricular_session_attendance`` records.

        :raises UserError: when this session is not ``planned``
        """
        self.ensure_one()
        if self.state != "planned":
            error_message = (
                _(
                    """
Context: Fill extracurricular session attendance
Database ID: %s
Problem: Session is not in Planned state
Solution: Only a session in Planned state may have its attendance
filled automatically
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)
        attendance_obj = self.env["school_extracurricular_session_attendance"]
        already_filled = self.attendance_ids.mapped("participant_id")
        for participant in self._get_active_participants():
            if participant in already_filled:
                continue
            attendance_obj.create(self._prepare_attendance_data(participant))

    def _get_active_participants(self):
        """List the Offering participants active on this session's date.

        Active means ``open`` state, joined on or before the session
        date, and not yet left (empty ``date_leave``, or a leave date
        on or after the session date).

        :return: a ``school_extracurricular_participant`` recordset
        """
        self.ensure_one()
        return self.offering_id.participant_ids.filtered(
            lambda participant: (
                participant.state == "open"
                and participant.date_join
                and participant.date_join <= self.date
                and (not participant.date_leave or participant.date_leave >= self.date)
            )
        )

    def _prepare_attendance_data(self, participant):
        """Build the values of one generated attendance line.

        Extension point: override to carry extra fields into the
        generated attendance line.

        :param participant: the participant the line is generated for
        :return: dict of
            ``school_extracurricular_session_attendance`` values
        """
        self.ensure_one()
        return {
            "session_id": self.id,
            "participant_id": participant.id,
        }

    def action_restart(self):
        """Return this session to ``planned``.

        :return: nothing; clears any recorded cancel reason
        """
        for record in self.sudo():
            record._restart()

    def _restart(self):
        """Reset state to ``planned`` and clear ``cancel_reason``.

        Side effect: writes ``state`` and ``cancel_reason`` on this
        session. Allowed from ``done`` and ``cancelled``.
        """
        self.ensure_one()
        self.write({"state": "planned", "cancel_reason": False})
