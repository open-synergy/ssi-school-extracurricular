# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularParticipant(YamlTransactionCase):
    """Pure Python tests for the participant's session smart buttons."""

    def _create_fixture(self, code):
        """Build one Participant with a Planned session and a Done one.

        The Done session gets a ``present`` attendance line for the
        Participant, and a second Done session gets an ``absent``
        line -- so ``attendance_present_count`` (1) differs from
        ``session_done_count`` (2), proving the two actions are not
        accidentally sharing one domain.

        :param code: short suffix making every record's ``code``
            unique across test methods
        :return: tuple of (participant, planned_session, done_session)
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Part %s" % code, "code": "EXTPART-GT-%s" % code}
        )
        school = self.env["school"].create(
            {
                "name": "School Part %s" % code,
                "code": "EXTPART-SCH-%s" % code,
                "grade_type_id": grade_type.id,
            }
        )
        category = self.env["school_extracurricular_category"].create(
            {"name": "Category Part %s" % code, "code": "EXTPART-CAT-%s" % code}
        )
        extracurricular = self.env["school_extracurricular"].create(
            {
                "name": "Futsal Club Part %s" % code,
                "code": "EXTPART-EXT-%s" % code,
                "category_id": category.id,
                "school_id": school.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Part %s" % code,
                "code": "EXTPART-AY-%s" % code,
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Part %s" % code,
                "code": "EXTPART-TERM-%s" % code,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Teacher Employee Part %s" % code}
        )
        teacher = self.env["school_teacher"].create(
            {
                "name": "Teacher Part %s" % code,
                "code": "EXTPART-TCH-%s" % code,
                "employee_id": employee.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Extracurricular Fee Part %s" % code}
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
                "name": "Grade Part %s" % code,
                "code": "EXTPART-GR-%s" % code,
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Grade Class Part %s" % code,
                "code": "EXTPART-GC-%s" % code,
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create(
            {"name": "Student Contact Part %s" % code}
        )
        student = self.env["school_student"].create(
            {
                "name": "Student Part %s" % code,
                "code": "EXTPART-ST-%s" % code,
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
        planned_session = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-03",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        done_session_present = self.env["school_extracurricular_session"].create(
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
                "session_id": done_session_present.id,
                "participant_id": participant.id,
                "attendance_state": "present",
            }
        )
        done_session_present.action_done()
        done_session_absent = self.env["school_extracurricular_session"].create(
            {
                "offering_id": offering.id,
                "teacher_id": teacher.id,
                "date": "2026-08-05",
                "time_start": 14.0,
                "time_end": 15.5,
            }
        )
        self.env["school_extracurricular_session_attendance"].create(
            {
                "session_id": done_session_absent.id,
                "participant_id": participant.id,
                "attendance_state": "absent",
            }
        )
        done_session_absent.action_done()
        return participant, planned_session, done_session_present

    def test_action_view_session_planned_returns_planned_sessions(self):
        """Assert ``action_view_session_planned``'s window action.

        Pure Python -- trigger P1 (L-01/L-02: ``action: call`` in
        YAML discards a method's return value, and every assert's
        target is a dotted path on a registry record, so the
        returned window action's ``res_model``/``domain`` cannot be
        asserted in YAML). The domain matches
        ``_compute_session_planned_count`` exactly: the Offering's
        sessions currently ``planned``.
        """
        participant, planned_session, __ = self._create_fixture("P1C")
        action = participant.action_view_session_planned()
        self.assertEqual(action["res_model"], "school_extracurricular_session")
        self.assertEqual(
            action["domain"],
            [
                ("offering_id", "=", participant.offering_id.id),
                ("state", "=", "planned"),
            ],
        )
        found = self.env["school_extracurricular_session"].search(action["domain"])
        self.assertEqual(found, planned_session)
        self.assertEqual(len(found), participant.session_planned_count)

    def test_action_view_session_done_returns_done_sessions(self):
        """Assert ``action_view_session_done``'s window action.

        Pure Python -- trigger P1 (L-01/L-02, same as above). The
        domain matches ``_compute_session_done_count`` exactly: the
        Offering's sessions currently ``done`` -- both of them,
        regardless of this participant's own attendance on each.
        """
        participant, __, done_session_present = self._create_fixture("P1D")
        action = participant.action_view_session_done()
        self.assertEqual(action["res_model"], "school_extracurricular_session")
        self.assertEqual(
            action["domain"],
            [
                ("offering_id", "=", participant.offering_id.id),
                ("state", "=", "done"),
            ],
        )
        found = self.env["school_extracurricular_session"].search(action["domain"])
        self.assertIn(done_session_present, found)
        self.assertEqual(len(found), participant.session_done_count)
        self.assertEqual(participant.session_done_count, 2)

    def test_action_view_attendance_present_returns_present_lines(self):
        """Assert ``action_view_attendance_present``'s window action.

        Pure Python -- trigger P1 (L-01/L-02, same as above). The
        domain matches ``_compute_attendance_present_count`` exactly:
        this participant's Present/Late lines on Done sessions --
        excluding the Absent line on the other Done session.
        """
        participant, __, done_session_present = self._create_fixture("P1E")
        action = participant.action_view_attendance_present()
        self.assertEqual(
            action["res_model"], "school_extracurricular_session_attendance"
        )
        self.assertEqual(
            action["domain"],
            [
                ("participant_id", "=", participant.id),
                ("attendance_state", "in", ("present", "late")),
                ("session_id.state", "=", "done"),
            ],
        )
        found = self.env["school_extracurricular_session_attendance"].search(
            action["domain"]
        )
        self.assertEqual(len(found), 1)
        self.assertEqual(found.session_id, done_session_present)
        self.assertEqual(len(found), participant.attendance_present_count)
