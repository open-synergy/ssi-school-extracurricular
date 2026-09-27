# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator

REJECTED_TERM_STATES = ("invoiced", "paid", "voided", "cancelled")


class SchoolExtracurricularParticipant(models.Model):
    """Extends the participant with the admission billing route.

    Adds ``admission`` to ``billing_mode`` -- the same option added to
    the Offering, so a participant copied from an admission-mode
    Offering can actually store it -- and
    ``admission_id``/``admission_allocation_ids``, the admission-side
    twins of ``enrollment_id``/``allocation_ids``, used when
    ``billing_mode`` is ``admission``. ``enrollment_id`` is redefined
    non-required here since a participant billed to admission may not
    have an enrollment yet; the equivalent requirement is enforced by
    ``_check_enrollment_required`` instead, conditioned on
    ``billing_mode``. Unlike the Offering, ``billing_mode`` here has
    no ``default=``, so its ``ondelete`` policy for ``admission`` is a
    callable that falls back to ``enrollment`` instead of ``set
    default`` (a bare ``set default`` would fail module setup: it
    requires the field to define a default).
    """

    _inherit = "school_extracurricular_participant"

    billing_mode = fields.Selection(
        selection_add=[("admission", "Charged to Admission")],
        ondelete={
            "admission": lambda records: records.write({"billing_mode": "enrollment"}),
        },
    )
    enrollment_id = fields.Many2one(
        required=False,
        help=(
            "The Student's enrollment for the same academic term as "
            "the Offering. Required unless Billing Mode is Charged to "
            "Admission, in which case an Admission is used instead."
        ),
    )
    admission_id = fields.Many2one(
        string="Admission",
        comodel_name="school_admission",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The student's admission record used to bill this "
            "participant's fee. Required, and used instead of an "
            "Enrollment, when Billing Mode is Charged to Admission."
        ),
    )
    admission_allocation_ids = fields.One2many(
        string="Admission Allocation",
        comodel_name="school_extracurricular_participant_admission_allocation",
        inverse_name="participant_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Admission payment term(s) this participant's fee is "
            "allocated to. Required to open a participant whose "
            "Billing Mode is Charged to Admission; ignored otherwise."
        ),
    )

    @api.constrains("billing_mode", "enrollment_id")
    def _check_enrollment_required(self):
        """Require ``enrollment_id`` unless billed to admission.

        ``enrollment_id`` is no longer required at the field level
        (see the class docstring), so this constraint restores the
        requirement for every Billing Mode except ``admission``.

        :raises ValidationError: when ``enrollment_id`` is empty and
            ``billing_mode`` is not ``admission``
        :return: None
        """
        for record in self:
            if record.billing_mode != "admission" and not record.enrollment_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular participant enrollment
Database ID: %s
Problem: Enrollment is required when Billing Mode is not Charged to
Admission
Solution: Select an Enrollment, or change Billing Mode to Charged to
Admission
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)

    @api.constrains("admission_id", "student_id")
    def _check_admission_student(self):
        """Validate that the admission belongs to the selected student.

        Rejects a record whose ``admission_id.school_student_id``
        differs from its ``student_id``; records where either field is
        still empty pass.

        :raises ValidationError: on admission/student mismatch
        :return: None
        """
        for record in self:
            if (
                record.admission_id
                and record.student_id
                and record.admission_id.school_student_id != record.student_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant admission
Database ID: %s
Problem: Admission '%s' does not belong to Student '%s'
Solution: Select an Admission that belongs to the selected Student
"""
                    )
                    % (
                        record.id,
                        record.admission_id.name,
                        record.student_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("admission_id", "offering_id")
    def _check_admission_academic_term(self):
        """Validate that the admission matches the offering's term.

        Rejects a record whose ``admission_id.academic_term_id``
        differs from its ``offering_id.academic_term_id``; records
        where either field is still empty pass.

        :raises ValidationError: on academic term mismatch
        :return: None
        """
        for record in self:
            if (
                record.admission_id
                and record.offering_id
                and record.admission_id.academic_term_id
                != record.offering_id.academic_term_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant admission
Database ID: %s
Problem: Admission academic term '%s' does not match Offering
academic term '%s'
Solution: Select an Admission for the same academic term as the
Offering
"""
                    )
                    % (
                        record.id,
                        record.admission_id.academic_term_id.name,
                        record.offering_id.academic_term_id.name,
                    )
                )
                raise ValidationError(error_message)

    @ssi_decorator.pre_open_check()
    def _21_check_admission_allocation(self):
        """Block opening this participant without admission allocation.

        Runs after the enrollment-mode allocation check. When
        ``billing_mode`` is ``admission``, an ``admission_id`` and at
        least one ``admission_allocation_ids`` line must be set, and
        the enrollment-mode ``allocation_ids`` family must be empty.
        Other billing modes are not affected.

        :raises UserError: when billed through admission without an
            Admission, without any Admission Allocation line, or with
            a stray enrollment-mode Allocation line
        :return: None
        """
        self.ensure_one()
        if self.billing_mode != "admission":
            return
        if not self.admission_id:
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Billing Mode is 'Charged to Admission' but no Admission is
set
Solution: Select an Admission before opening
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)
        if not self.admission_allocation_ids:
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Billing Mode is 'Charged to Admission' but no Admission
Allocation line is set
Solution: Add at least one Admission Allocation line pointing to an
admission payment term before opening
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)
        if self.allocation_ids:
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Billing Mode is 'Charged to Admission' but enrollment
Allocation line(s) are still set
Solution: Remove the enrollment Allocation line(s) before opening
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)

    @ssi_decorator.pre_open_check()
    def _26_check_admission_allocation_term_state(self):
        """Block opening if an allocated admission term is billed.

        Runs after the allocation-required check. When
        ``billing_mode`` is ``admission``, rejects opening if any
        ``admission_allocation_ids.payment_term_id`` has become
        ``invoiced``, ``paid``, ``voided`` or ``cancelled`` since the
        allocation was created. Other billing modes are not affected.

        :raises UserError: when an allocated admission payment term is
            already invoiced, paid, voided or cancelled
        :return: None
        """
        self.ensure_one()
        if self.billing_mode != "admission":
            return
        billed_allocations = self.admission_allocation_ids.filtered(
            lambda allocation: allocation.payment_term_id.state in REJECTED_TERM_STATES
        )
        if billed_allocations:
            payment_term = billed_allocations[0].payment_term_id
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Allocated Admission Payment Term '%(term)s' is already
%(state)s
Solution: Remove or replace the Admission Allocation line pointing to
that Payment Term before opening
"""
                )
                % {
                    "id": self.id,
                    "term": payment_term.name,
                    "state": payment_term.state,
                }
            )
            raise UserError(error_message)

    @ssi_decorator.post_open_action()
    def _11_create_admission_extra_detail(self):
        """Create one addendum fee line per admission allocation.

        Post-open hook: for every ``admission_allocation_ids`` line,
        creates a ``school_admission_payment_term_extra_detail`` on
        the allocated admission payment term mirroring the
        allocation's product line values, and writes the created line
        back onto ``extra_detail_id`` for traceability. Unlike the
        enrollment-mode twin, no Final Usage/Final Account is copied:
        revenue recognition for admission billing is out of scope.

        :return: None
        """
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_admission_payment_term_extra_detail"
        ]
        for allocation in self.admission_allocation_ids:
            aa = (  # pylint: disable=invalid-name,consider-using-ternary
                allocation.analytic_account_id
                and allocation.analytic_account_id.id
                or False
            )
            detail = Detail.create(
                {
                    "term_id": allocation.payment_term_id.id,
                    "participant_id": self.id,
                    "product_id": allocation.product_id.id,
                    "name": allocation.name,
                    "account_id": allocation.account_id.id,
                    "uom_id": allocation.uom_id.id,
                    "uom_quantity": allocation.uom_quantity,
                    "price_unit": allocation.price_unit,
                    "tax_ids": [(6, 0, allocation.tax_ids.ids)],
                    "analytic_account_id": aa or False,
                }
            )
            allocation.write({"extra_detail_id": detail.id})

    @ssi_decorator.pre_cancel_check()
    def _11_check_invoiced_admission_extra_detail(self):
        """Block cancelling when an admission addendum line is invoiced.

        Pre-cancel hook: rejects cancellation when any addendum fee
        line created from ``admission_allocation_ids`` is already
        linked to a customer invoice line -- unlike the enrollment
        route, admission addendum lines have no ``locked`` flag of
        their own, since the admission's payment terms are already
        locked by the time an admission-mode participant can be
        opened at all.

        :raises UserError: when an addendum fee line is already
            invoiced
        :return: None
        """
        self.ensure_one()
        invoiced = self.admission_allocation_ids.mapped("extra_detail_id").filtered(
            "customer_invoice_line_id"
        )
        if invoiced:
            error_message = (
                _(
                    """
Context: Cancel extracurricular participant
Database ID: %(id)s
Problem: An admission addendum fee line is already linked to a
customer invoice line
Solution: Delete or disconnect the customer invoice from the
admission payment term before cancelling this participant
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)

    @ssi_decorator.post_cancel_action()
    def _11_remove_admission_extra_detail(self):
        """Remove the admission addendum fee lines of this participant.

        Post-cancel hook: deletes every addendum fee line created from
        ``admission_allocation_ids``, so the admission payment term's
        totals fall back to what they were before this participant
        was opened. Safe to run unconditionally: an invoiced line
        would have already blocked cancellation in
        ``_11_check_invoiced_admission_extra_detail``.

        :return: None
        """
        self.ensure_one()
        self.admission_allocation_ids.mapped("extra_detail_id").unlink()
