# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularCreateDueInvoice(HttpSavepointCase):
    """Tour test for the ``school_extracurricular_create_due_invoice`` work
    instruction.
    """

    @classmethod
    def setUpClass(cls):
        """Create one Student with one due, uninvoiced standalone payment term.

        The Offering is billed Separate Invoice (Route B) with a complete
        accounting setup (journal, receivable account, invoice type), and
        the Participant is advanced to Open via direct method calls (not by
        clicking through the UI) so its payment term's computed status
        becomes Uninvoiced -- exactly what the wizard's Payment Terms
        domain (``state = 'uninvoiced'``) picks up.
        """
        super().setUpClass()
        # ``approve_ok`` is only granted to users listed in
        # ``active_approver_user_ids`` (policy_template/
        # school_extracurricular_participant.xml, Approve) -- SUPERUSER is
        # never a member (it is inactive at SQL level, see
        # odoo/addons/base/data/base_data.sql), so the approve call below
        # must run as a genuine approver instead of ``cls.env`` (which is
        # SUPERUSER here).
        cls.admin = cls.env.ref("base.user_admin")
        grade_type = cls.env["school_grade_type"].create(
            {"name": "TOUR-WIZARD-GRADE-TYPE", "code": "/"}
        )
        school = cls.env["school"].create(
            {
                "name": "TOUR-WIZARD-SCHOOL",
                "code": "/",
                "grade_type_id": grade_type.id,
            }
        )
        category = cls.env["school_extracurricular_category"].create(
            {"name": "TOUR-WIZARD-CATEGORY", "code": "/"}
        )
        product = cls.env["product.product"].create({"name": "TOUR-WIZARD-PRODUCT"})
        extracurricular = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-WIZARD-EXTRACURRICULAR",
                "code": "/",
                "category_id": category.id,
                "school_id": school.id,
                "product_id": product.id,
            }
        )
        academic_year = cls.env["school_academic_year"].create(
            {
                "name": "TOUR-WIZARD-YEAR",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2027-06-30",
            }
        )
        academic_term = cls.env["school_academic_term"].create(
            {
                "name": "TOUR-WIZARD-TERM-ACADEMIC",
                "code": "/",
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "year_id": academic_year.id,
            }
        )
        teacher_employee = cls.env["hr.employee"].create(
            {"name": "TOUR-WIZARD-TEACHER"}
        )
        teacher = cls.env["school_teacher"].create(
            {
                "name": "TOUR-WIZARD-TEACHER",
                "code": "/",
                "employee_id": teacher_employee.id,
            }
        )
        grade = cls.env["school_grade"].create(
            {"name": "TOUR-WIZARD-GRADE", "code": "/", "type_id": grade_type.id}
        )
        grade_class = cls.env["school_grade_class"].create(
            {
                "name": "TOUR-WIZARD-GRADE-CLASS",
                "code": "/",
                "school_id": school.id,
                "grade_id": grade.id,
            }
        )
        revenue_type = cls.env.ref("account.data_account_type_revenue")
        income_account = cls.env["account.account"].create(
            {
                "name": "TOUR-WIZARD-INCOME",
                "code": "TOURWIZINC",
                "user_type_id": revenue_type.id,
            }
        )
        receivable_type = cls.env.ref("account.data_account_type_receivable")
        receivable_account = cls.env["account.account"].create(
            {
                "name": "TOUR-WIZARD-RECEIVABLE",
                "code": "TOURWIZREC",
                "user_type_id": receivable_type.id,
                "reconcile": True,
            }
        )
        journal = cls.env["account.journal"].create(
            {
                "name": "TOUR-WIZARD-JOURNAL",
                "code": "TOURWZ",
                "type": "sale",
            }
        )
        invoice_type = cls.env["customer_invoice_type"].create(
            {
                "name": "TOUR-WIZARD-INVOICE-TYPE",
                "code": "/",
                "journal_id": journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        offering = cls.env["school_extracurricular_offering"].create(
            {
                "extracurricular_id": extracurricular.id,
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "teacher_id": teacher.id,
                "date_start": "2026-07-01",
                "date_end": "2026-12-31",
                "product_id": product.id,
                "price_unit": 300000.0,
                "billing_mode": "standalone",
                "customer_invoice_type_id": invoice_type.id,
                "receivable_journal_id": journal.id,
                "receivable_account_id": receivable_account.id,
            }
        )
        contact = cls.env["res.partner"].create({"name": "TOUR-WIZARD-STUDENT"})
        student = cls.env["school_student"].create(
            {
                "name": "TOUR-WIZARD-STUDENT",
                "code": "/",
                "contact_id": contact.id,
                "school_id": school.id,
            }
        )
        enrollment = cls.env["school_enrollment"].create(
            {
                "academic_year_id": academic_year.id,
                "academic_term_id": academic_term.id,
                "school_id": school.id,
                "grade_id": grade.id,
                "grade_class_id": grade_class.id,
                "student_id": student.id,
            }
        )
        participant = cls.env["school_extracurricular_participant"].create(
            {
                "offering_id": offering.id,
                "student_id": student.id,
                "enrollment_id": enrollment.id,
                "billing_mode": "standalone",
                "product_id": product.id,
                "price_unit": 300000.0,
            }
        )
        participant.with_user(cls.admin).action_confirm()
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
        participant.invalidate_cache()
        participant.with_user(cls.admin).action_approve_approval()
        participant.invalidate_cache()

        term = cls.env["school_extracurricular_payment_term"].create(
            {
                "participant_id": participant.id,
                "name": "TOUR-WIZARD-TERM",
                "date_due": "2026-06-15",
            }
        )
        cls.env["school_extracurricular_payment_term_detail"].create(
            {
                "term_id": term.id,
                "product_id": product.id,
                "name": "TOUR-WIZARD-FEE",
                "account_id": income_account.id,
                "uom_quantity": 1.0,
                "price_unit": 300000.0,
            }
        )

    def test_create_invoice(self):
        """Run the create-invoice tour for the consolidation wizard.

        IK: docs/school_extracurricular_create_due_invoice/01-create-invoice.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_create_due_invoice"
            "_create_invoice",
            login="admin",
        )
