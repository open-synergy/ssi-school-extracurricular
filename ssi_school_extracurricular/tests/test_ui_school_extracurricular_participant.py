# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularParticipant(HttpSavepointCase):
    """Tour tests for the ``school_extracurricular_participant`` work instructions."""

    @classmethod
    def _create_student(cls, name):
        """Create a Student (and its backing Contact) with a unique name.

        Used to give every fixture Participant a distinct, list-visible
        marker (the Student column is shown in the tree view), so tour
        selectors can find the right row.

        :param name: unique name shared by the Contact and the Student
        :return: the created ``school_student`` record
        :rtype: recordset
        """
        contact = cls.env["res.partner"].create({"name": name})
        return cls.env["school_student"].create(
            {
                "name": name,
                "code": "/",
                "contact_id": contact.id,
                "school_id": cls.school.id,
            }
        )

    @classmethod
    def _create_enrollment(cls, student):
        """Create an Enrollment for the given Student in the shared term.

        :param student: the ``school_student`` record to enrol
        :return: the created ``school_enrollment`` record
        :rtype: recordset
        """
        return cls.env["school_enrollment"].create(
            {
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
                "grade_class_id": cls.grade_class.id,
                "student_id": student.id,
            }
        )

    @classmethod
    def _create_participant(cls, student, enrollment, billing_mode):
        """Create a Draft Participant on the shared Offering.

        :param student: the ``school_student`` record joining
        :param enrollment: the student's ``school_enrollment`` record
        :param billing_mode: ``"free"`` or ``"enrollment"``
        :return: the created ``school_extracurricular_participant`` record
        :rtype: recordset
        """
        return cls.env["school_extracurricular_participant"].create(
            {
                "offering_id": cls.offering.id,
                "student_id": student.id,
                "enrollment_id": enrollment.id,
                "billing_mode": billing_mode,
                "product_id": cls.product.id,
                "price_unit": 600000.0,
            }
        )

    @classmethod
    def _allocate_to_enrollment(cls, participant, enrollment):
        """Add one Allocation line billing the participant to the enrollment.

        Required before a Billing Mode "Charged to Enrollment" participant
        can be opened -- see ``05-approve.md``.

        :param participant: the ``school_extracurricular_participant``
            record to allocate
        :param enrollment: the ``school_enrollment`` record whose payment
            term receives the addendum fee line
        :return: None
        """
        term = cls.env["school_enrollment_payment_term"].create(
            {
                "enrollment_id": enrollment.id,
                "name": "TOUR-PARTICIPANT-ALLOC-TERM",
            }
        )
        cls.env["school_extracurricular_participant_allocation"].create(
            {
                "participant_id": participant.id,
                "payment_term_id": term.id,
                "product_id": cls.product.id,
                "name": "TOUR-PARTICIPANT-ALLOC-FEE",
                "account_id": cls.income_account.id,
                "uom_quantity": 1.0,
                "price_unit": 600000.0,
            }
        )

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one Participant per tour scenario.

        Participants for the approve/finish/cancel/restart tours are billed
        through Charged to Enrollment with an Allocation line already set,
        and advanced to their Pre-Condition state here via direct method
        calls (not by clicking through the UI), following the same pattern
        already used by this module's YAML workflow scenarios.
        """
        super().setUpClass()
        # ``approve_ok``/``reject_ok`` are only granted to users listed in
        # ``active_approver_user_ids`` (policy_template/
        # school_extracurricular_participant.xml, Approve/Reject) --
        # SUPERUSER is never a member (it is inactive at SQL level, see
        # odoo/addons/base/data/base_data.sql), so any fixture that reaches
        # an approve/reject call must run as a genuine approver instead of
        # ``cls.env`` (which is SUPERUSER here).
        cls.admin = cls.env.ref("base.user_admin")
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR-PARTICIPANT-GRADE-TYPE", "code": "/"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR-PARTICIPANT-SCHOOL",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.category = cls.env["school_extracurricular_category"].create(
            {"name": "TOUR-PARTICIPANT-CATEGORY", "code": "/"}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "TOUR-PARTICIPANT-PRODUCT"}
        )
        cls.extracurricular = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-PARTICIPANT-EXTRACURRICULAR",
                "code": "/",
                "category_id": cls.category.id,
                "school_id": cls.school.id,
                "product_id": cls.product.id,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR-PARTICIPANT-YEAR",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR-PARTICIPANT-TERM",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        teacher_employee = cls.env["hr.employee"].create(
            {"name": "TOUR-PARTICIPANT-TEACHER"}
        )
        cls.teacher = cls.env["school_teacher"].create(
            {
                "name": "TOUR-PARTICIPANT-TEACHER",
                "code": "/",
                "employee_id": teacher_employee.id,
            }
        )
        cls.grade = cls.env["school_grade"].create(
            {
                "name": "TOUR-PARTICIPANT-GRADE",
                "code": "/",
                "type_id": cls.grade_type.id,
            }
        )
        cls.grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR-PARTICIPANT-GRADE-CLASS",
                "code": "/",
                "school_id": cls.school.id,
                "grade_id": cls.grade.id,
            }
        )
        revenue_type = cls.env.ref("account.data_account_type_revenue")
        cls.income_account = cls.env["account.account"].create(
            {
                "name": "TOUR-PARTICIPANT-INCOME",
                "code": "TOURPARINC",
                "user_type_id": revenue_type.id,
            }
        )
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-PARTICIPANT-CANCEL-REASON",
                "code": "/",
                "global_use": True,
            }
        )

        cls.offering = cls.env["school_extracurricular_offering"].create(
            {
                "name": "TOUR-PARTICIPANT-OFFERING",
                "extracurricular_id": cls.extracurricular.id,
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "teacher_id": cls.teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": cls.product.id,
                "price_unit": 150000.0,
            }
        )

        create_student = cls._create_student("TOUR-PARTICIPANT-CREATE-STUDENT")
        create_enrollment = cls._create_enrollment(create_student)
        create_enrollment.write({"name": "TOUR-PARTICIPANT-ENROLLMENT"})

        edit_student = cls._create_student("TOUR-PARTICIPANT-EDIT")
        cls.participant_edit = cls._create_participant(
            edit_student, cls._create_enrollment(edit_student), "free"
        )

        delete_student = cls._create_student("TOUR-PARTICIPANT-DELETE")
        cls.participant_delete = cls._create_participant(
            delete_student, cls._create_enrollment(delete_student), "free"
        )

        confirm_student = cls._create_student("TOUR-PARTICIPANT-CONFIRM")
        cls.participant_confirm = cls._create_participant(
            confirm_student, cls._create_enrollment(confirm_student), "free"
        )

        approve_student = cls._create_student("TOUR-PARTICIPANT-APPROVE")
        approve_enrollment = cls._create_enrollment(approve_student)
        cls.participant_approve = cls._create_participant(
            approve_student, approve_enrollment, "enrollment"
        )
        cls._allocate_to_enrollment(cls.participant_approve, approve_enrollment)
        # Plain SUPERUSER call, no with_user() needed: confirm_ok has
        # restrict_user=1 (policy_template/
        # school_extracurricular_participant.xml, Confirm), and
        # mixin.policy._get_policy short-circuits restrict_user to True
        # for SUPERUSER_ID -- unlike approve_ok/reject_ok below, which
        # use restrict_additional's active_approver_user_ids check that
        # has no such bypass. The actual approve happens in the browser
        # (as "admin"), not here.
        cls.participant_approve.action_confirm()

        reject_student = cls._create_student("TOUR-PARTICIPANT-REJECT")
        cls.participant_reject = cls._create_participant(
            reject_student, cls._create_enrollment(reject_student), "free"
        )
        # Same reasoning as participant_approve above.
        cls.participant_reject.action_confirm()

        finish_student = cls._create_student("TOUR-PARTICIPANT-FINISH")
        finish_enrollment = cls._create_enrollment(finish_student)
        cls.participant_finish = cls._create_participant(
            finish_student, finish_enrollment, "enrollment"
        )
        cls._allocate_to_enrollment(cls.participant_finish, finish_enrollment)
        cls.participant_finish.with_user(cls.admin).action_confirm()
        # approve_ok is a non-stored compute that only depends on
        # policy_template_id (see mixin.policy._compute_policy) --
        # not on the approval_ids that action_confirm() just created
        # -- so its cached (pre-confirm, False) value must be
        # invalidated here or action_approve_approval() below raises
        # "Document is not allowed to approve" even though admin is a
        # genuine approver. ``with_user(cls.admin)`` is also required on
        # the approve call itself: ``cls.env`` is SUPERUSER, which is
        # never in ``active_approver_user_ids`` (see comment above
        # ``cls.admin``), so calling as SUPERUSER always raises
        # "Document is not allowed to approve" regardless of the cache.
        cls.participant_finish.invalidate_cache()
        cls.participant_finish.with_user(cls.admin).action_approve_approval()
        cls.participant_finish.invalidate_cache()

        cancel_student = cls._create_student("TOUR-PARTICIPANT-CANCEL")
        cancel_enrollment = cls._create_enrollment(cancel_student)
        cls.participant_cancel = cls._create_participant(
            cancel_student, cancel_enrollment, "enrollment"
        )
        cls._allocate_to_enrollment(cls.participant_cancel, cancel_enrollment)
        cls.participant_cancel.with_user(cls.admin).action_confirm()
        # approve_ok is subject to the same non-stored, confirm-blind
        # compute as above -- invalidate before approving. Same
        # SUPERUSER-is-not-an-approver reasoning as participant_finish
        # above applies to ``with_user(cls.admin)`` here too.
        cls.participant_cancel.invalidate_cache()
        cls.participant_cancel.with_user(cls.admin).action_approve_approval()
        cls.participant_cancel.invalidate_cache()

        restart_student = cls._create_student("TOUR-PARTICIPANT-RESTART")
        restart_enrollment = cls._create_enrollment(restart_student)
        cls.participant_restart = cls._create_participant(
            restart_student, restart_enrollment, "enrollment"
        )
        cls._allocate_to_enrollment(cls.participant_restart, restart_enrollment)
        cls.participant_restart.with_user(cls.admin).action_confirm()
        # reject_ok is subject to the same non-stored, confirm-blind
        # compute as approve_ok above -- invalidate before rejecting.
        # Same SUPERUSER-is-not-an-approver reasoning as
        # participant_finish above applies to ``with_user(cls.admin)``
        # here too.
        cls.participant_restart.invalidate_cache()
        cls.participant_restart.with_user(cls.admin).action_reject_approval()
        cls.participant_restart.invalidate_cache()

    def test_create(self):
        """Run the create tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_extracurricular_participant``.

        IK: docs/school_extracurricular_participant/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_participant_restart",
            login="admin",
        )
