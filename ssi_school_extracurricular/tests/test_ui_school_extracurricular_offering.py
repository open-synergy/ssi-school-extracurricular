# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularOffering(HttpSavepointCase):
    """Tour tests for the ``school_extracurricular_offering`` work instructions."""

    @classmethod
    def _create_teacher(cls, name):
        """Create a Teacher (and its backing Employee) with a unique name.

        Used to give every fixture Offering a distinct, list-visible marker
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
    def _create_offering(cls, teacher):
        """Create a Draft Offering for the given Teacher fixture.

        :param teacher: the ``school_teacher`` record used both as the
            offering's Teacher and as the row's list marker
        :return: the created ``school_extracurricular_offering`` record
        :rtype: recordset
        """
        return cls.env["school_extracurricular_offering"].create(
            {
                "extracurricular_id": cls.extracurricular.id,
                "academic_year_id": cls.academic_year.id,
                "academic_term_id": cls.academic_term.id,
                "teacher_id": teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": cls.product.id,
                "price_unit": 150000.0,
            }
        )

    @classmethod
    def setUpClass(cls):
        """Create shared master data and one Offering per tour scenario.

        Offerings for the confirm/approve/reject/finish/cancel/restart tours
        are advanced to their Pre-Condition state here via direct method
        calls (not by clicking through the UI), following the same pattern
        already used by this module's YAML workflow scenarios.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR-OFFERING-GRADE-TYPE", "code": "/"}
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR-OFFERING-SCHOOL",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.category = cls.env["school_extracurricular_category"].create(
            {"name": "TOUR-OFFERING-CATEGORY", "code": "/"}
        )
        cls.product = cls.env["product.product"].create(
            {"name": "TOUR-OFFERING-PRODUCT"}
        )
        cls.extracurricular = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-OFFERING-EXTRACURRICULAR",
                "code": "/",
                "category_id": cls.category.id,
                "school_id": cls.school.id,
                "product_id": cls.product.id,
            }
        )
        cls.academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR-OFFERING-YEAR",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        cls.academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR-OFFERING-TERM",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": cls.academic_year.id,
            }
        )
        cls.env["school_teacher"].create(
            {
                "name": "TOUR-OFFERING-TEACHER",
                "code": "/",
                "employee_id": cls.env["hr.employee"]
                .create({"name": "TOUR-OFFERING-TEACHER"})
                .id,
            }
        )
        cls.env["base.cancel_reason"].create(
            {
                "name": "TOUR-OFFERING-CANCEL-REASON",
                "code": "/",
                "global_use": True,
            }
        )

        cls.offering_edit = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-EDIT")
        )
        cls.offering_delete = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-DELETE")
        )
        cls.offering_confirm = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-CONFIRM")
        )
        cls.offering_cancel = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-CANCEL")
        )

        cls.offering_approve = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-APPROVE")
        )
        cls.offering_approve.action_confirm()

        cls.offering_reject = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-REJECT")
        )
        cls.offering_reject.action_confirm()

        cls.offering_finish = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-FINISH")
        )
        cls.offering_finish.action_confirm()
        # approve_ok is a non-stored compute that only depends on
        # policy_template_id (see mixin.policy._compute_policy) --
        # not on the approval_ids that action_confirm() just created
        # -- so its cached (pre-confirm, False) value must be
        # invalidated here or action_approve_approval() below raises
        # "Document is not allowed to approve" even though admin is a
        # genuine approver.
        cls.offering_finish.invalidate_cache()
        cls.offering_finish.action_approve_approval()

        cls.offering_restart = cls._create_offering(
            cls._create_teacher("TOUR-OFFERING-RESTART")
        )
        cls.offering_restart.action_confirm()
        # reject_ok is subject to the same non-stored, confirm-blind
        # compute as approve_ok above -- invalidate before rejecting.
        cls.offering_restart.invalidate_cache()
        cls.offering_restart.action_reject_approval()

    def test_create(self):
        """Run the create tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_delete",
            login="admin",
        )

    def test_confirm(self):
        """Run the confirm tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/04-confirm.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_confirm",
            login="admin",
        )

    def test_approve(self):
        """Run the approve tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/05-approve.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_approve",
            login="admin",
        )

    def test_reject(self):
        """Run the reject tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/06-reject.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_reject",
            login="admin",
        )

    def test_finish(self):
        """Run the finish tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/09-finish.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_finish",
            login="admin",
        )

    def test_cancel(self):
        """Run the cancel tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/10-cancel.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_cancel",
            login="admin",
        )

    def test_restart(self):
        """Run the restart tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/12-restart.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_offering_restart",
            login="admin",
        )
