# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularSession(HttpSavepointCase):
    """Tour tests for the ``school_extracurricular_session`` work instructions."""

    @classmethod
    def _create_teacher(cls, name):
        """Create a Teacher (and its backing Employee) with a unique name.

        Used to give each fixture Session a distinct, list-visible marker
        (the Teacher column is shown in the tree view), so tour selectors
        can find the right row.

        :param name: unique name shared by the Employee and the Teacher
        :return: the created ``school_teacher`` record
        :rtype: recordset
        """
        employee = cls.env["hr.employee"].create({"name": name})
        return cls.env["school_teacher"].create(
            {
                "name": name,
                "code": "/",
                "employee_id": employee.id,
            }
        )

    @classmethod
    def _create_session(cls, teacher, date):
        """Create a Planned Session on the shared Offering.

        :param teacher: the ``school_teacher`` record used both as the
            session's Teacher and as the row's list marker
        :param date: the meeting date, as a ``YYYY-MM-DD`` string
        :return: the created ``school_extracurricular_session`` record
        :rtype: recordset
        """
        return cls.env["school_extracurricular_session"].create(
            {
                "offering_id": cls.offering.id,
                "teacher_id": teacher.id,
                "date": date,
                "time_start": 9.0,
                "time_end": 10.0,
            }
        )

    @classmethod
    def setUpClass(cls):
        """Create shared master data, one Offering, and one Session per tour.

        The Fill Attendance Pre-Condition also needs one Open Participant on
        the shared Offering, advanced here via direct method calls (not by
        clicking through the UI), following the same pattern already used by
        ``school_extracurricular_participant``'s own UI tests. The Done
        Pre-Condition (at least one attendance line) is prepared directly
        too, since it is not this module's Fill Attendance IK being tested.
        """
        super().setUpClass()
        # ``approve_ok`` is only granted to users listed in
        # ``active_approver_user_ids`` (policy_template/
        # school_extracurricular_participant.xml, Approve) -- SUPERUSER is
        # never a member (it is inactive at SQL level, see
        # odoo/addons/base/data/base_data.sql), so reaching Open below must
        # run as a genuine approver instead of ``cls.env``.
        cls.admin = cls.env.ref("base.user_admin")
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR-SESSION-GRADE-TYPE", "code": "/"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR-SESSION-SCHOOL",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.category = cls.env["school_extracurricular_category"].create(
            {"name": "TOUR-SESSION-CATEGORY", "code": "/"}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "TOUR-SESSION-PRODUCT"}
        )
        cls.extracurricular = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-SESSION-EXTRACURRICULAR",
                "code": "/",
                "category_id": cls.category.id,
                "school_id": cls.school.id,
                "product_id": cls.product.id,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR-SESSION-YEAR",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR-SESSION-TERM",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR-SESSION-GRADE",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR-SESSION-GRADE-CLASS",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        offering_teacher = cls._create_teacher("TOUR-SESSION-OFFERING-TEACHER")
        cls.offering = cls.env["school_extracurricular_offering"].create(
            {
                "name": "TOUR-SESSION-OFFERING",
                "extracurricular_id": cls.extracurricular.id,
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "teacher_id": offering_teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": cls.product.id,
                "price_unit": 150000.0,
            }
        )

        # Fill Attendance Pre-Condition: one Open Participant, joined
        # before every fixture session's date.
        contact = cls.env["res.partner"].create({"name": "TOUR-SESSION-STUDENT"})
        cls.student = cls.env["school_student"].create(
            {
                "name": "TOUR-SESSION-STUDENT",
                "code": "/",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )
        cls.enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "grade_class_id": cls.grade_class.id,
                "student_id": cls.student.id,
            }
        )
        cls.participant = cls.env["school_extracurricular_participant"].create(
            {
                "offering_id": cls.offering.id,
                "student_id": cls.student.id,
                "enrollment_id": cls.enrollment.id,
                "billing_mode": "free",
                "product_id": cls.product.id,
                "price_unit": 600000.0,
                "date_join": "2026-07-01",
            }
        )
        cls.participant.with_user(cls.admin).action_confirm()
        # ``approve_ok`` is a non-stored compute that only depends on
        # ``policy_template_id`` (mixin.policy._compute_policy), not on
        # the approval record ``action_confirm`` just created --
        # invalidate the pre-confirm cached value before approving.
        cls.participant.invalidate_cache()
        cls.participant.with_user(cls.admin).action_approve_approval()
        cls.participant.invalidate_cache()
        # ``_after_approved_method = "action_open"`` on the participant
        # model moves it straight to Open once approved.

        cls.session_edit = cls._create_session(
            cls._create_teacher("TOUR-SESSION-EDIT"), "2026-07-06"
        )
        cls.session_delete = cls._create_session(
            cls._create_teacher("TOUR-SESSION-DELETE"), "2026-07-07"
        )
        cls.session_fill = cls._create_session(
            cls._create_teacher("TOUR-SESSION-FILL"), "2026-08-10"
        )
        cls.session_done = cls._create_session(
            cls._create_teacher("TOUR-SESSION-DONE"), "2026-08-11"
        )
        # Done Pre-Condition: at least one attendance line, prepared
        # directly here -- Fill Attendance is a different IK/tour.
        cls.env["school_extracurricular_session_attendance"].create(
            {
                "session_id": cls.session_done.id,
                "participant_id": cls.participant.id,
            }
        )
        cls.session_cancel = cls._create_session(
            cls._create_teacher("TOUR-SESSION-CANCEL"), "2026-08-12"
        )
        cls.session_restart = cls._create_session(
            cls._create_teacher("TOUR-SESSION-RESTART"), "2026-08-13"
        )
        # Restart Pre-Condition: status is Done or Cancelled. Set
        # directly -- reaching Done through action_done() is a separate
        # IK/tour and is not this fixture's concern.
        cls.session_restart.write({"state": "done"})

    def test_create(self):
        """Run the create tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_delete",
            login="admin",
        )

    def test_fill_attendance(self):
        """Run the fill attendance tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/04-fill-attendance.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_fill_attendance",
            login="admin",
        )

    def test_done(self):
        """Run the done tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/05-done.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_done",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/06-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/07-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_restart",
            login="admin",
        )

    def test_generate(self):
        """Run the generate tour for ``school_extracurricular_session``.

        IK: docs/school_extracurricular_session/08-generate.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_school_extracurricular_session_generate",
            login="admin",
        )
