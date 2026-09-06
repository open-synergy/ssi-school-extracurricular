# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


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
