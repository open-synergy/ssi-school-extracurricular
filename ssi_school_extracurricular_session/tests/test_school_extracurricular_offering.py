# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularOffering(YamlTransactionCase):
    """Pure Python tests for the offering's session smart buttons."""

    def _create_fixture(self, code):
        """Build a minimal Offering with one Planned and one Done session.

        :param code: short suffix making every record's ``code``
            unique across test methods
        :return: the created ``school_extracurricular_offering`` record
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Offering %s" % code, "code": "EXTOFF-GT-%s" % code}
        )
        school = self.env["school"].create(
            {
                "name": "School Offering %s" % code,
                "code": "EXTOFF-SCH-%s" % code,
                "grade_type_id": grade_type.id,
            }
        )
        category = self.env["school_extracurricular_category"].create(
            {"name": "Category Offering %s" % code, "code": "EXTOFF-CAT-%s" % code}
        )
        extracurricular = self.env["school_extracurricular"].create(
            {
                "name": "Futsal Club Offering %s" % code,
                "code": "EXTOFF-EXT-%s" % code,
                "category_id": category.id,
                "school_id": school.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Offering %s" % code,
                "code": "EXTOFF-AY-%s" % code,
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Offering %s" % code,
                "code": "EXTOFF-TERM-%s" % code,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Teacher Employee Offering %s" % code}
        )
        teacher = self.env["school_teacher"].create(
            {
                "name": "Teacher Offering %s" % code,
                "code": "EXTOFF-TCH-%s" % code,
                "employee_id": employee.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Extracurricular Fee Offering %s" % code}
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
        planned_session = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-03",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        done_session = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-04",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        self.env["school_extracurricular_session_attendance"].create(
            {
                "session_id": done_session.id,
                "participant_id": self._create_participant(
                    offering, school, academic_year, academic_term, code
                ).id,
            }
        )
        done_session.action_done()
        return offering, planned_session, done_session

    def _create_participant(self, offering, school, academic_year, academic_term, code):
        """Create a participant of ``offering``, for the fill-attendance line.

        :param offering: the participant's Offering
        :param school: the Offering's School
        :param academic_year: the enrollment's Academic Year
        :param academic_term: the enrollment's Academic Term
        :param code: short suffix keeping ``code`` unique
        :return: the created ``school_extracurricular_participant`` record
        """
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Offering %s" % code,
                "code": "EXTOFF-GR-%s" % code,
                "type_id": school.grade_type_id.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Grade Class Offering %s" % code,
                "code": "EXTOFF-GC-%s" % code,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Offering %s" % code}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Offering %s" % code,
                "code": "EXTOFF-ST-%s" % code,
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
        return self.env["school_extracurricular_participant"].create(
            {
                "offering_id": offering.id,
                "student_id": student.id,
                "enrollment_id": enrollment.id,
                "billing_mode": "enrollment",
                "product_id": offering.product_id.id,
                "uom_quantity": 1.0,
                "price_unit": 150000.0,
            }
        )

    def test_action_view_session_returns_all_sessions(self):
        """Assert ``action_view_session``'s ``ir.actions.act_window`` dict.

        Pure Python -- trigger P1 (L-01/L-02: ``action: call`` in YAML
        discards a method's return value, and every assert's target is
        a dotted path on a registry record, so the returned window
        action's ``res_model``/``domain`` cannot be asserted in YAML).
        The domain matches ``_compute_session_count`` exactly: every
        session of this offering, in any state.
        """
        offering, planned_session, done_session = self._create_fixture("P1A")
        action = offering.action_view_session()
        self.assertEqual(action["res_model"], "school_extracurricular_session")
        self.assertEqual(action["domain"], [("offering_id", "=", offering.id)])
        found = self.env["school_extracurricular_session"].search(action["domain"])
        self.assertEqual(found, planned_session | done_session)
        self.assertEqual(len(found), offering.session_count)

    def test_action_view_session_done_returns_done_sessions(self):
        """Assert ``action_view_session_done``'s window action.

        Pure Python -- trigger P1 (L-01/L-02, same as above). The
        domain matches ``_compute_session_done_count`` exactly: only
        this offering's sessions currently ``done``.
        """
        offering, planned_session, done_session = self._create_fixture("P1B")
        action = offering.action_view_session_done()
        self.assertEqual(action["res_model"], "school_extracurricular_session")
        self.assertEqual(
            action["domain"],
            [("offering_id", "=", offering.id), ("state", "=", "done")],
        )
        found = self.env["school_extracurricular_session"].search(action["domain"])
        self.assertEqual(found, done_session)
        self.assertEqual(len(found), offering.session_done_count)
