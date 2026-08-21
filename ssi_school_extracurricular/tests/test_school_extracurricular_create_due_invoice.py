# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase
from psycopg2 import IntegrityError

from odoo.tests import tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularCreateDueInvoice(YamlTransactionCase):
    """Scenario tests for ``school_extracurricular_create_due_invoice``."""

    def test_school_extracurricular_create_due_invoice(self):
        """Run the consolidation, auto-confirm, and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_extracurricular_create_due_invoice.yaml"
        )

    @mute_logger("odoo.sql_db")
    def test_delete_invoiced_customer_invoice_is_restricted(self):
        """Reject deleting a customer invoice still linked to a term.

        Pure Python -- trigger P5 (L-22: ``ondelete="restrict"`` on
        ``school_extracurricular_payment_term.customer_invoice_id``
        raises ``psycopg2.IntegrityError`` at the database level, a
        type the YAML ``expect_error`` registry does not recognize).
        ``mute_logger("odoo.sql_db")`` silences the PostgreSQL ERROR
        line this deliberately triggers so ``oca_checklog_odoo`` does
        not fail the CI job over an intentional negative test.
        """
        grade_type = self.env["school_grade_type"].create(
            {"name": "Grade Type Wizard PY", "code": "EXTWIZ-GT-PY"}
        )
        school = self.env["school"].create(
            {
                "name": "School Wizard PY",
                "code": "EXTWIZ-SCH-PY",
                "grade_type_id": grade_type.id,
            }
        )
        category = self.env["school_extracurricular_category"].create(
            {"name": "Category Wizard PY", "code": "EXTWIZ-CAT-PY"}
        )
        extracurricular = self.env["school_extracurricular"].create(
            {
                "name": "Chess Club Wizard PY",
                "code": "EXTWIZ-EXT-PY",
                "category_id": category.id,
                "school_id": school.id,
            }
        )
        academic_year = self.env["school_academic_year"].create(
            {
                "name": "AY Wizard PY",
                "code": "EXTWIZ-AY-PY",
                "date_start": "2024-07-01",
                "date_end": "2025-06-30",
            }
        )
        academic_term = self.env["school_academic_term"].create(
            {
                "name": "Term Wizard PY",
                "code": "EXTWIZ-TERM-PY",
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "year_id": academic_year.id,
            }
        )
        employee = self.env["hr.employee"].create(
            {"name": "Teacher Employee Wizard PY"}
        )
        teacher = self.env["school_teacher"].create(
            {
                "name": "Teacher Wizard PY",
                "code": "EXTWIZ-TCH-PY",
                "employee_id": employee.id,
            }
        )
        product = self.env["product.product"].create(
            {"name": "Chess Club Fee Wizard PY"}
        )
        offering = self.env["school_extracurricular_offering"].create(
            {
                "extracurricular_id": extracurricular.id,
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "teacher_id": teacher.id,
                "date_start": "2024-07-01",
                "date_end": "2024-12-31",
                "product_id": product.id,
                "price_unit": 300000.0,
                "billing_mode": "standalone",
            }
        )
        grade = self.env["school_grade"].create(
            {
                "name": "Grade Wizard PY",
                "code": "EXTWIZ-GR-PY",
                "type_id": grade_type.id,
            }
        )
        grade_class = self.env["school_grade_class"].create(
            {
                "name": "Grade Class Wizard PY",
                "code": "EXTWIZ-GC-PY",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        contact = self.env["res.partner"].create({"name": "Student Contact Wizard PY"})
        student = self.env["school_student"].create(
            {
                "name": "Student Wizard PY",
                "code": "EXTWIZ-ST-PY",
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
                "billing_mode": "standalone",
                "product_id": product.id,
                "uom_quantity": 1.0,
                "price_unit": 300000.0,
            }
        )
        term = self.env["school_extracurricular_payment_term"].create(
            {"participant_id": participant.id, "name": "Chess Club Term 1 PY"}
        )

        receivable_type = self.env.ref("account.data_account_type_receivable")
        receivable_account = self.env["account.account"].create(
            {
                "name": "Extracurricular Wizard Receivable PY",
                "code": "EXTWIZ-REC-PY",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        journal = self.env["account.journal"].create(
            {
                "name": "Extracurricular Wizard Journal PY",
                "code": "EXWZPY",
                "type": "sale",
            }
        )
        invoice_type = self.env["customer_invoice_type"].create(
            {
                "name": "Extracurricular Wizard Invoice Type PY",
                "code": "/",
                "journal_id": journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        invoice = self.env["customer_invoice"].create(
            {
                "type_id": invoice_type.id,
                "partner_id": contact.id,
                "currency_id": self.env.company.currency_id.id,
                "journal_id": journal.id,
                "receivable_account_id": receivable_account.id,
                "date": "2024-06-01",
                "date_due": "2024-06-30",
            }
        )
        term.write({"customer_invoice_id": invoice.id})

        with self.assertRaises(IntegrityError):
            invoice.unlink()
