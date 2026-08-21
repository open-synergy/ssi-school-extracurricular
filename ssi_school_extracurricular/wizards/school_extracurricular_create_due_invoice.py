# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SchoolExtracurricularCreateDueInvoice(models.TransientModel):
    """Wizard that consolidates one student's due extracurricular fees.

    A student may join several extracurricular offerings in the same
    term, each billed through its own ``billing_mode = "standalone"``
    payment term (Route B). This wizard picks every ``uninvoiced``
    payment term of the selected student whose ``date_due`` falls at
    or before the chosen cut-off date, and invoices all of them
    together as a single ``customer_invoice`` -- one document per
    student instead of one per participant. Every payment term's
    offering must agree on Receivable Journal, Receivable Account,
    and Customer Invoice Type; otherwise the wizard refuses to guess
    which one to use.
    """

    _name = "school_extracurricular_create_due_invoice"
    _description = "Create Due Invoice for Extracurricular Payment Terms"

    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        help="The student whose due extracurricular payment terms will "
        "be consolidated into one invoice.",
    )
    date_due_max = fields.Date(
        string="Due Date Until",
        required=True,
        help="Only payment terms whose Estimated Due Date is on or "
        "before this date are invoiced. Also used as the Due Date of "
        "the resulting customer invoice.",
    )
    date_invoice = fields.Date(
        string="Invoice Date",
        required=True,
        default=lambda self: fields.Date.context_today(self),
        help="Date used as the Date of the resulting customer invoice.",
    )
    term_ids = fields.Many2many(
        string="Payment Terms",
        comodel_name="school_extracurricular_payment_term",
        relation="rel_school_extracurricular_create_due_invoice",
        column1="wizard_id",
        column2="term_id",
        compute="_compute_term_ids",
        store=False,
        help="Uninvoiced payment terms of the selected Student whose "
        "Estimated Due Date is on or before Due Date Until. "
        "Automatically recomputed when Student or Due Date Until "
        "changes.",
    )

    @api.depends(
        "student_id",
        "date_due_max",
    )
    def _compute_term_ids(self):
        """Collect the student's due, uninvoiced payment terms.

        Searches ``school_extracurricular_payment_term`` for records
        whose participant belongs to ``student_id``, whose ``state``
        is ``uninvoiced``, and whose ``date_due`` is on or before
        ``date_due_max``. Left empty until both fields are set.

        :return: None
        """
        Term = self.env["school_extracurricular_payment_term"]  # noqa: N806
        for record in self:
            result = Term
            if record.student_id and record.date_due_max:
                result = Term.search(
                    [
                        ("participant_id.student_id", "=", record.student_id.id),
                        ("state", "=", "uninvoiced"),
                        ("date_due", "<=", record.date_due_max),
                    ]
                )
            record.term_ids = result

    def action_create_invoice(self):
        """Consolidate this student's due payment terms into one invoice.

        Triggered by the wizard button. Delegates to
        ``_create_invoice`` for each wizard record, then closes the
        dialog.

        :return: an ``ir.actions.act_window_close`` action
        :raises UserError: when no payment term is due, or the due
            payment terms' offerings disagree on Receivable Journal,
            Receivable Account, or Customer Invoice Type
        """
        for record in self.sudo():
            record._create_invoice()  # pylint: disable=protected-access
        return {"type": "ir.actions.act_window_close"}

    def _create_invoice(self):
        """Create one consolidated ``customer_invoice`` for this wizard.

        Both guards run first, so a missing selection or an offering
        mismatch aborts before any invoice is created. The header is
        built from the offering of the first payment term (ordered by
        sequence, then id); one ``customer_invoice.line`` is then
        created per detail line of every selected term, linked back
        via ``customer_invoice_line_id``, and every term is linked to
        the new invoice via ``customer_invoice_id``. When any involved
        offering has ``auto_confirm_customer_invoice`` enabled, the
        invoice is confirmed once every line has been created.

        :raises UserError: propagated from ``_check_term_ids`` or
            ``_check_offering_consistency``
        :return: None
        """
        self.ensure_one()
        self._check_term_ids()
        self._check_offering_consistency()
        line_model = self.env["customer_invoice.line"]
        first_term = self.term_ids.sorted(key=lambda term: (term.sequence, term.id))[0]
        invoice = self.env["customer_invoice"].create(
            self._prepare_invoice_data(first_term)
        )
        for term in self.term_ids:
            for detail in term.detail_ids:
                line_data = (
                    detail._prepare_invoice_line()  # pylint: disable=protected-access
                )
                line_data["customer_invoice_id"] = invoice.id
                line = line_model.create(line_data)
                detail.write({"customer_invoice_line_id": line.id})
            term.write({"customer_invoice_id": invoice.id})
        offerings = self.term_ids.mapped("participant_id.offering_id")
        if any(offerings.mapped("auto_confirm_customer_invoice")):
            invoice.action_confirm()

    def _check_term_ids(self):
        """Validate that at least one payment term is due.

        :raises UserError: when ``term_ids`` is empty -- no uninvoiced
            payment term of the selected Student is due on or before
            Due Date Until
        """
        self.ensure_one()
        if not self.term_ids:
            error_message = (
                _(
                    """
Context: Create due invoice for extracurricular payment terms
Database ID: %s
Problem: No uninvoiced payment term of Student '%s' is due on or
before %s
Solution: Choose a Student with due payment terms, or extend Due Date
Until
"""
                )
                % (self.id, self.student_id.name, self.date_due_max)
            )
            raise UserError(error_message)

    def _check_offering_consistency(self):
        """Validate that every due term's offering shares the same setup.

        Compares Receivable Journal, Receivable Account, and Customer
        Invoice Type across the offerings of every selected term's
        participant; the header of the resulting invoice can only be
        built from one of them, so a mismatch is rejected instead of
        picking one silently.

        :raises UserError: when the offerings disagree on Receivable
            Journal, Receivable Account, or Customer Invoice Type
        """
        self.ensure_one()
        offerings = self.term_ids.mapped("participant_id.offering_id")
        journals = offerings.mapped("receivable_journal_id")
        accounts = offerings.mapped("receivable_account_id")
        types = offerings.mapped("customer_invoice_type_id")
        if len(journals) > 1 or len(accounts) > 1 or len(types) > 1:
            error_message = (
                _(
                    """
Context: Create due invoice for extracurricular payment terms
Database ID: %s
Problem: The due payment terms' offerings do not share the same
Receivable Journal, Receivable Account, and Customer Invoice Type
Solution: Invoice the disagreeing offerings' payment terms separately,
or align their accounting configuration first
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

    def _prepare_invoice_data(self, first_term):
        """Build the ``customer_invoice`` header values for this run.

        Extension point: override in a glue module (Operating Unit,
        for instance) to add extra header values. Detail lines are
        deliberately excluded -- they are created one by one by
        ``_create_invoice`` so that each line can be written back to
        its originating detail.

        :param first_term: the payment term (sequence, then id) whose
            participant's offering supplies the accounting setup
        :return: dict of ``customer_invoice`` values
        """
        self.ensure_one()
        offering = first_term.participant_id.offering_id
        return {
            "type_id": offering.customer_invoice_type_id.id,
            "partner_id": self.student_id.contact_id.id,
            "currency_id": offering.currency_id.id,
            "pricelist_id": offering.pricelist_id.id,
            "journal_id": offering.receivable_journal_id.id,
            "receivable_account_id": offering.receivable_account_id.id,
            "date": self.date_invoice,
            "date_due": self.date_due_max,
            "customer_document_number": self.student_id.name,
        }
