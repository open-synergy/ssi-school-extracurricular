# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_WEEKDAY_FIELDS = [
    ("mon", 0),
    ("tue", 1),
    ("wed", 2),
    ("thu", 3),
    ("fri", 4),
    ("sat", 5),
    ("sun", 6),
]


class SchoolExtracurricularSessionGenerate(models.TransientModel):
    """Generate a term's worth of sessions from a weekly pattern.

    Typing one meeting at a time is impractical: one offering can run
    thirty to forty meetings a semester, always on the same weekday(s)
    and time, across the offering's period. This wizard creates one
    ``planned`` session for every date in a chosen range whose weekday
    is checked, skipping any date that already has a matching session
    so it can be run more than once without duplicating.
    """

    _name = "school_extracurricular_session_generate"
    _description = "Generate Extracurricular Sessions"

    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        required=True,
        help="The term's offering to generate sessions for.",
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        help="The first date sessions may be generated on.",
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        help="The last date sessions may be generated on.",
    )
    time_start = fields.Float(
        string="Start Time",
        required=True,
        help="The start time applied to every generated session.",
    )
    time_end = fields.Float(
        string="End Time",
        required=True,
        help="The end time applied to every generated session.",
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=True,
        help="The teacher applied to every generated session.",
    )
    location = fields.Char(
        string="Location",
        help="The location applied to every generated session.",
    )
    mon = fields.Boolean(
        string="Monday",
        default=False,
        help="Generate a session on every Monday in the range.",
    )
    tue = fields.Boolean(
        string="Tuesday",
        default=False,
        help="Generate a session on every Tuesday in the range.",
    )
    wed = fields.Boolean(
        string="Wednesday",
        default=False,
        help="Generate a session on every Wednesday in the range.",
    )
    thu = fields.Boolean(
        string="Thursday",
        default=False,
        help="Generate a session on every Thursday in the range.",
    )
    fri = fields.Boolean(
        string="Friday",
        default=False,
        help="Generate a session on every Friday in the range.",
    )
    sat = fields.Boolean(
        string="Saturday",
        default=False,
        help="Generate a session on every Saturday in the range.",
    )
    sun = fields.Boolean(
        string="Sunday",
        default=False,
        help="Generate a session on every Sunday in the range.",
    )

    @api.onchange("offering_id")
    def onchange_date_start(self):
        self.date_start = False
        if self.offering_id:
            self.date_start = self.offering_id.date_start

    @api.onchange("offering_id")
    def onchange_date_end(self):
        self.date_end = False
        if self.offering_id:
            self.date_end = self.offering_id.date_end

    @api.onchange("offering_id")
    def onchange_teacher_id(self):
        self.teacher_id = False
        if self.offering_id:
            self.teacher_id = self.offering_id.teacher_id

    def action_generate(self):
        """Generate this offering's sessions from the weekly pattern.

        Creates one ``planned`` session per matching date. No window
        is opened afterwards; the offering's Sessions list reflects
        the result once refreshed.
        """
        for record in self.sudo():
            record._generate_sessions()

    def _generate_sessions(self):
        """Create one planned session per matching date in the range.

        Side effect: creates ``school_extracurricular_session``
        records. A candidate date that already has a session for the
        same Offering and Start Time is skipped, so running this
        twice with the same parameters does not duplicate sessions.

        :raises UserError: when no weekday is checked, when the date
            range falls outside the Offering's period, or when no
            date in the range matches a checked weekday
        :return: None
        """
        self.ensure_one()
        weekdays = self._get_selected_weekdays()
        if not weekdays:
            error_message = (
                _(
                    """
Context: Generate extracurricular sessions
Database ID: %s
Problem: No weekday is checked
Solution: Check at least one weekday before generating sessions
"""
                )
                % (self.offering_id.id,)
            )
            raise UserError(error_message)
        if not self._check_range_within_offering_condition():
            error_message = (
                _(
                    """
Context: Generate extracurricular sessions
Database ID: %s
Problem: Date range is outside Offering '%s' period
Solution: Select a Start Date and End Date within the Offering's
period ('%s' - '%s')
"""
                )
                % (
                    self.offering_id.id,
                    self.offering_id.name,
                    self.offering_id.date_start,
                    self.offering_id.date_end,
                )
            )
            raise UserError(error_message)
        candidate_dates = self._get_candidate_dates(weekdays)
        if not candidate_dates:
            error_message = (
                _(
                    """
Context: Generate extracurricular sessions
Database ID: %s
Problem: No date in the range matches a checked weekday
Solution: Widen the date range, or check a weekday that falls
within it
"""
                )
                % (self.offering_id.id,)
            )
            raise UserError(error_message)
        session_obj = self.env["school_extracurricular_session"]
        for candidate_date in candidate_dates:
            if self._session_exists(candidate_date):
                continue
            session_obj.create(self._prepare_session_data(candidate_date))

    def _get_selected_weekdays(self):
        """List the Python weekday indexes of the checked days.

        Monday is ``0`` and Sunday is ``6``, matching
        ``date.weekday()``.

        :return: list of int weekday indexes
        """
        self.ensure_one()
        return [weekday for field_name, weekday in _WEEKDAY_FIELDS if self[field_name]]

    def _check_range_within_offering_condition(self):
        """Tell whether the wizard's range fits the Offering's period.

        :return: True when valid; never raises
        """
        self.ensure_one()
        if not self.offering_id.date_start or not self.offering_id.date_end:
            return True
        return (
            self.date_start >= self.offering_id.date_start
            and self.date_end <= self.offering_id.date_end
        )

    def _get_candidate_dates(self, weekdays):
        """List the dates in range whose weekday is checked.

        :param weekdays: list of int weekday indexes (Monday is 0)
        :return: list of ``date`` objects, in ascending order
        """
        self.ensure_one()
        result = []
        one_day = timedelta(days=1)
        current = self.date_start
        while current <= self.date_end:
            if current.weekday() in weekdays:
                result.append(current)
            current += one_day
        return result

    def _session_exists(self, candidate_date):
        """Tell whether a session already exists for the candidate date.

        Matches on Offering, Date, and Start Time, so re-running the
        generator with the same parameters does not duplicate a
        session already created for that date.

        :param candidate_date: the date being considered
        :return: True when a matching session already exists
        """
        self.ensure_one()
        session_obj = self.env["school_extracurricular_session"]
        return bool(
            session_obj.search_count(
                [
                    ("offering_id", "=", self.offering_id.id),
                    ("date", "=", candidate_date),
                    ("time_start", "=", self.time_start),
                ]
            )
        )

    def _prepare_session_data(self, candidate_date):
        """Build the values of one generated session.

        Extension point: override to carry extra fields into the
        generated sessions.

        :param candidate_date: the date of the session to create
        :return: dict of ``school_extracurricular_session`` values
        """
        self.ensure_one()
        return {
            "offering_id": self.offering_id.id,
            "date": candidate_date,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "teacher_id": self.teacher_id.id,
            "location": self.location,
        }
