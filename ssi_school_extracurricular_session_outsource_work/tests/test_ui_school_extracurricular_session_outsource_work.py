# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so the Pre-Condition fixtures below
# would fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularSessionOutsourceWork(HttpSavepointCase):
    """Tour test for the Done -> honor creation work instruction delta."""

    @classmethod
    def setUpClass(cls):
        """Build one Offering/Session whose roster already has a rate.

        The roster line's Attendance is set directly (a plain field on
        a child line, not a workflow state) instead of through the UI
        -- Fill Attendance is a different IK/tour and is not this
        fixture's concern, matching the base module's own precedent
        for the Attendance tab.
        """
        super().setUpClass()
        cls.admin = cls.env.ref("base.user_admin")

        cls.instructor = cls.env["res.partner"].create(
            {"name": "TOUR-OW-INSTRUCTOR", "is_company": False}
        )
        account = cls.env["account.account"].search(
            [("internal_type", "=", "payable")], limit=1
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "TOUR-OW-ANALYTIC"}
        )
        owt_product = cls.env["product.product"].create({"name": "TOUR-OW-PRODUCT"})
        usage_type = cls.env["product.usage_type"].create(
            {
                "name": "TOUR-OW-USAGE",
                "code": "/",
                "account_id": account.id,
            }
        )
        owt_category = cls.env["outsource_work_type_category"].create(
            {"name": "TOUR-OW-CATEGORY", "code": "/"}
        )
        owt_type = cls.env["outsource_work_type"].create(
            {
                "name": "TOUR-OW-TYPE",
                "code": "/",
                "category_id": owt_category.id,
                "product_id": owt_product.id,
            }
        )
        pricelist = cls.env["product.pricelist"].create({"name": "TOUR-OW-PRICELIST"})
        rate = (
            cls.env["outsource_work_rate"]
            .with_user(cls.admin)
            .create(
                {
                    "partner_id": cls.instructor.id,
                    "date": "2026-01-01",
                    "date_start": "2026-01-01",
                }
            )
        )
        cls.env["outsource_work_rate_detail"].create(
            {
                "rate_id": rate.id,
                "product_id": owt_product.id,
                "pricelist_id": pricelist.id,
            }
        )
        rate.with_user(cls.admin).action_confirm()
        rate.invalidate_cache()
        rate.with_user(cls.admin).action_approve_approval()
        rate.invalidate_cache()
        rate.with_user(cls.admin).action_open()

        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR-OW-GRADE-TYPE", "code": "/"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR-OW-SCHOOL",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        category = cls.env["school_extracurricular_category"].create(
            {"name": "TOUR-OW-CATEGORY-EXT", "code": "/"}
        )
        product = cls.env["product.product"].create({"name": "TOUR-OW-EXT-PRODUCT"})
        extracurricular = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-OW-EXTRACURRICULAR",
                "code": "/",
                "category_id": category.id,
                "school_id": school.id,
                "product_id": product.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR-OW-YEAR",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR-OW-TERM",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        offering_employee = cls.env["hr.employee"].create(
            {"name": "TOUR-OW-OFFERING-TEACHER"}
        )
        offering_teacher = cls.env["school_teacher"].create(
            {
                "name": "TOUR-OW-OFFERING-TEACHER",
                "code": "/",
                "employee_id": offering_employee.id,
            }
        )
        cls.offering = cls.env["school_extracurricular_offering"].create(
            {
                "name": "TOUR-OW-OFFERING",
                "extracurricular_id": extracurricular.id,
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "teacher_id": offering_teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": product.id,
                "price_unit": 150000.0,
                "participant_attendance_tracked": False,
                "instructor_attendance_tracked": True,
                "analytic_account_id": cls.analytic_account.id,
            }
        )
        cls.env["school_extracurricular_offering_instructor"].create(
            {
                "offering_id": cls.offering.id,
                "role": "head",
                "partner_id": cls.instructor.id,
                "outsource_work_type_id": owt_type.id,
                "outsource_work_usage_id": usage_type.id,
            }
        )
        cls.session_done = cls.env["school_extracurricular_session"].create(
            {
                "offering_id": cls.offering.id,
                "teacher_id": offering_teacher.id,
                "date": "2026-08-11",
                "time_start": 9.0,
                "time_end": 10.0,
            }
        )
        cls.session_done.instructor_ids.write({"attendance_state": "present"})

    def test_done(self):
        """Run the Done tour, asserting the new honor log appears.

        IK: docs/school_extracurricular_session/05-done.md (extension)
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_session_outsource_work_"
            "school_extracurricular_session_done",
            login="admin",
        )
