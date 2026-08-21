# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularSession(YamlTransactionCase):
    """Scenario tests for ``school_extracurricular_session``."""

    def test_school_extracurricular_session(self):
        """Run the create, workflow, default and negative scenarios."""
        self.run_yaml_scenario("test_data_school_extracurricular_session.yaml")

    def test_action_cancel_returns_wizard_action(self):
        """Assert the act_window dict returned by ``action_cancel``.

        Pure Python -- trigger P1 (L-01: the ``call`` action discards
        a method's return value, so YAML cannot assert the
        ``ir.actions.act_window`` dict opening the cancel wizard).
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Session P1", "code": "EXTSESS-GT-P1"}
        )
        school = self.env["school"].create(
            {
                "name": "School Session P1",
                "code": "EXTSESS-SCH-P1",
                "grade_type_id": grade_type.id,
            }
        )
        category = self.env["school_extracurricular_category"].create(
            {"name": "Category Session P1", "code": "EXTSESS-CAT-P1"}
        )
        extracurricular = self.env["school_extracurricular"].create(
            {
                "name": "Futsal Club Session P1",
                "code": "EXTSESS-EXT-P1",
                "category_id": category.id,
                "school_id": school.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Session P1",
                "code": "EXTSESS-AY-P1",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Session P1",
                "code": "EXTSESS-TERM-P1",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Teacher Employee Session P1"}
        )
        teacher = self.env["school_teacher"].create(
            {
                "name": "Teacher Session P1",
                "code": "EXTSESS-TCH-P1",
                "employee_id": employee.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Extracurricular Fee Session P1"}
        )
        offering = self.env["school_extracurricular_offering"].create(
            {
                "extracurricular_id": extracurricular.id,
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "teacher_id": teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": product.id,
                "price_unit": 150000.0,
            }
        )
        session = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-21",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        action = session.action_cancel()
        self.assertEqual(action["res_model"], "cancel_extracurricular_session")
        self.assertEqual(action["target"], "new")
        self.assertEqual(action["context"]["default_session_id"], session.id)

    @mute_logger("odoo.sql_db")
    def test_attendance_duplicate_participant_rejected(self):
        """Reject a second attendance line for the same participant.

        Pure Python -- trigger P5 (L-22: ``psycopg2.IntegrityError``
        from the ``session_participant_uniq`` SQL constraint is not
        one of the 12 error types ``expect_error`` understands).
        ``mute_logger("odoo.sql_db")`` silences the PostgreSQL ERROR
        line this constraint violation writes to the log; without it
        ``oca_checklog_odoo`` fails CI even though the test passes.
        """
        from psycopg2 import IntegrityError

        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Session P5", "code": "EXTSESS-GT-P5"}
        )
        school = self.env["school"].create(
            {
                "name": "School Session P5",
                "code": "EXTSESS-SCH-P5",
                "grade_type_id": grade_type.id,
            }
        )
        category = self.env["school_extracurricular_category"].create(
            {"name": "Category Session P5", "code": "EXTSESS-CAT-P5"}
        )
        extracurricular = self.env["school_extracurricular"].create(
            {
                "name": "Futsal Club Session P5",
                "code": "EXTSESS-EXT-P5",
                "category_id": category.id,
                "school_id": school.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Session P5",
                "code": "EXTSESS-AY-P5",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Session P5",
                "code": "EXTSESS-TERM-P5",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Teacher Employee Session P5"}
        )
        teacher = self.env["school_teacher"].create(
            {
                "name": "Teacher Session P5",
                "code": "EXTSESS-TCH-P5",
                "employee_id": employee.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Extracurricular Fee Session P5"}
        )
        offering = self.env["school_extracurricular_offering"].create(
            {
                "extracurricular_id": extracurricular.id,
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "teacher_id": teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": product.id,
                "price_unit": 150000.0,
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Session P5",
                "code": "EXTSESS-GR-P5",
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Grade Class Session P5",
                "code": "EXTSESS-GC-P5",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Student Contact Session P5"})
        student = self.env["school_student"].create(
            {
                "name": "Student Session P5",
                "code": "EXTSESS-ST-P5",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = self.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        participant = self.env["school_extracurricular_participant"].create(
            {
                "offering_id": offering.id,
                "student_id": student.id,
                "enrollment_id": enrollment.id,
                "billing_mode": "enrollment",
                "product_id": product.id,
                "uom_quantity": 1.0,
                "price_unit": 150000.0,
            }
        )
        session = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-20",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        self.env["school_extracurricular_session_attendance"].create(
            {
                "session_id": session.id,
                "participant_id": participant.id,
            }
        )
        with self.assertRaises(IntegrityError):
            self.env["school_extracurricular_session_attendance"].create(
                {
                    "session_id": session.id,
                    "participant_id": participant.id,
                }
            )
