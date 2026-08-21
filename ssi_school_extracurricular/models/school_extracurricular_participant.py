# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolExtracurricularParticipant(models.Model):
    """Represents one student joining one term's extracurricular offering.

    ``school_extracurricular_offering`` only opens an activity for a
    term; it does not say who joined. Joining is a decision that
    creates a fee obligation, so it needs its own approvable document
    rather than a plain line on the offering. This document is also
    the only place that links a student to the ``school_enrollment``
    of the same term -- that link is what lets billing through
    enrollment (a later feature) charge the correct enrollment without
    guessing. The approval workflow uses the standard multi-approval
    mixins: Draft -> Confirm -> Approve -> Open -> Done / Cancel.
    ``open`` means the student is actively enrolled in the activity;
    ``done`` means the term has ended; ``cancel`` means the enrollment
    into the activity was withdrawn.
    """

    _name = "school_extracurricular_participant"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "Extracurricular Participant"

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True
    _automatically_insert_open_policy_fields = False
    _automatically_insert_open_button = False

    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "done_ok",
        "cancel_ok",
        "restart_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "action_done",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        required=True,
        ondelete="restrict",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The term's offering this participant is joining.",
    )
    extracurricular_id = fields.Many2one(
        string="Extracurricular",
        comodel_name="school_extracurricular",
        related="offering_id.extracurricular_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The extracurricular activity being joined, automatically "
            "populated from the selected Offering."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        related="offering_id.school_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The school running this offering, automatically populated "
            "from the selected Offering."
        ),
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        related="offering_id.academic_year_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The academic year of the joined Offering, automatically "
            "populated from the selected Offering."
        ),
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        related="offering_id.academic_term_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The academic term of the joined Offering, automatically "
            "populated from the selected Offering."
        ),
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="school_student",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The student joining this extracurricular offering.",
    )
    enrollment_id = fields.Many2one(
        string="Enrollment",
        comodel_name="school_enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The Student's enrollment for the same academic term as "
            "the Offering. Used to link this participation to the "
            "correct billing enrollment."
        ),
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        related="student_id.contact_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The student's contact, automatically populated from the "
            "selected Student."
        ),
    )
    date_join = fields.Date(
        string="Join Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date this student joined the extracurricular offering.",
    )
    date_leave = fields.Date(
        string="Leave Date",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The date this student stopped participating, if "
            "applicable. Left empty while the student is still active."
        ),
    )
    billing_mode = fields.Selection(
        string="Billing Mode",
        selection=[
            ("enrollment", "Charged to Enrollment"),
            ("standalone", "Separate Invoice"),
            ("free", "Free of Charge"),
        ],
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "How this participant's fee is billed: charged to the "
            "student's enrollment, invoiced separately, or free of "
            "charge. Defaults from the selected Offering."
        ),
    )
    product_id = fields.Many2one(
        string="Product",
        comodel_name="product.product",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The product used to bill this participant's fee. Defaults "
            "from the selected Offering's Product, but may be changed."
        ),
    )
    uom_quantity = fields.Float(
        string="Quantity",
        default=1.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The billed quantity for this participant's fee.",
    )
    price_unit = fields.Float(
        string="Price Unit",
        default=0.0,
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The fee charged to this student, before tax. Defaults "
            "from the selected Offering's Price Unit, but may be "
            "changed."
        ),
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_school_extracurricular_participant_2_tax",
        column1="participant_id",
        column2="tax_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The taxes applied on top of the Price Unit. Defaults from "
            "the selected Offering's Taxes."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="offering_id.currency_id",
        store=True,
        compute_sudo=True,
        readonly=True,
        help=(
            "The currency used for this participant's fee, "
            "automatically populated from the selected Offering."
        ),
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="The fee amount before tax.",
    )
    amount_tax = fields.Monetary(
        string="Tax Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="The total tax amount applied on the fee.",
    )
    amount_total = fields.Monetary(
        string="Total Amount",
        compute="_compute_amount",
        store=True,
        compute_sudo=True,
        currency_field="currency_id",
        help="The fee amount including tax.",
    )
    allocation_ids = fields.One2many(
        string="Allocation",
        comodel_name="school_extracurricular_participant_allocation",
        inverse_name="participant_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "Enrollment payment term(s) this participant's fee is "
            "allocated to. Required to open a participant whose "
            "Billing Mode is Charged to Enrollment; ignored otherwise."
        ),
    )

    @api.depends(
        "uom_quantity",
        "price_unit",
        "tax_ids",
        "currency_id",
    )
    def _compute_amount(self):
        """Compute the untaxed, tax, and total amount of the fee.

        Uses ``tax_ids.compute_all`` over the Quantity and Price Unit
        so ``amount_total`` always reflects the currently configured
        taxes.

        :return: nothing; assigns ``amount_untaxed``, ``amount_tax``,
            and ``amount_total``
        """
        for record in self:
            untaxed = total = record.uom_quantity * record.price_unit
            tax = 0.0
            if record.tax_ids:
                taxes = record.tax_ids.compute_all(
                    record.price_unit,
                    currency=record.currency_id,
                    quantity=record.uom_quantity,
                    product=record.product_id,
                    partner=record.partner_id,
                )
                untaxed = taxes["total_excluded"]
                total = taxes["total_included"]
                tax = total - untaxed
            record.amount_untaxed = untaxed
            record.amount_tax = tax
            record.amount_total = total

    @api.onchange(
        "offering_id",
    )
    def onchange_billing_mode(self):
        """Copy the Billing Mode from the selected Offering.

        Resets to ``False`` when no Offering is selected, so the
        field never carries a stale value from a previously selected
        Offering.
        """
        self.billing_mode = False
        if self.offering_id:
            self.billing_mode = self.offering_id.billing_mode

    @api.onchange(
        "offering_id",
    )
    def onchange_product_id(self):
        """Copy the Product from the selected Offering.

        Resets to ``False`` when no Offering is selected, so the
        field never carries a stale value from a previously selected
        Offering.
        """
        self.product_id = False
        if self.offering_id:
            self.product_id = self.offering_id.product_id

    @api.onchange(
        "offering_id",
    )
    def onchange_price_unit(self):
        """Copy the Price Unit from the selected Offering.

        Resets to ``0.0`` when no Offering is selected, so the field
        never carries a stale value from a previously selected
        Offering.
        """
        self.price_unit = 0.0
        if self.offering_id:
            self.price_unit = self.offering_id.price_unit

    @api.onchange(
        "offering_id",
    )
    def onchange_tax_ids(self):
        """Copy the Taxes from the selected Offering.

        Resets to empty when no Offering is selected, so the field
        never carries a stale value from a previously selected
        Offering.
        """
        self.tax_ids = False
        if self.offering_id:
            self.tax_ids = self.offering_id.tax_ids

    @api.constrains("enrollment_id", "student_id")
    def _check_enrollment_student(self):
        """Validate that the enrollment belongs to the selected student.

        Rejects a record whose ``enrollment_id.student_id`` differs
        from its ``student_id``; records where either field is still
        empty pass.

        :raises ValidationError: on enrollment/student mismatch
        :return: None
        """
        for record in self:
            if (
                record.enrollment_id
                and record.student_id
                and record.enrollment_id.student_id != record.student_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant enrollment
Database ID: %s
Problem: Enrollment '%s' does not belong to Student '%s'
Solution: Select an Enrollment that belongs to the selected Student
"""
                    )
                    % (
                        record.id,
                        record.enrollment_id.name,
                        record.student_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("enrollment_id", "offering_id")
    def _check_enrollment_academic_term(self):
        """Validate that the enrollment matches the offering's term.

        Rejects a record whose ``enrollment_id.academic_term_id``
        differs from its ``offering_id.academic_term_id``; records
        where either field is still empty pass.

        :raises ValidationError: on academic term mismatch
        :return: None
        """
        for record in self:
            if (
                record.enrollment_id
                and record.offering_id
                and record.enrollment_id.academic_term_id
                != record.offering_id.academic_term_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant enrollment
Database ID: %s
Problem: Enrollment academic term '%s' does not match Offering
academic term '%s'
Solution: Select an Enrollment for the same academic term as the
Offering
"""
                    )
                    % (
                        record.id,
                        record.enrollment_id.academic_term_id.name,
                        record.offering_id.academic_term_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("state", "student_id", "offering_id")
    def _check_duplicate_open_participant(self):
        """Validate that a student has one active participant per offering.

        Rejects a record whose Student already has another participant
        in ``open`` state for the same Offering.

        :raises ValidationError: on duplicate active participation
        :return: None
        """
        for record in self:
            if (
                record.state != "open"
                or not record.student_id
                or not record.offering_id
            ):
                continue
            duplicate = self.search(
                [
                    ("id", "!=", record.id),
                    ("offering_id", "=", record.offering_id.id),
                    ("student_id", "=", record.student_id.id),
                    ("state", "=", "open"),
                ]
            )
            if duplicate:
                error_message = (
                    _(
                        """
Context: Open extracurricular participant
Database ID: %s
Problem: Student '%s' already has an active participation on
Offering '%s'
Solution: Cancel or finish the existing participation before
opening a new one
"""
                    )
                    % (
                        record.id,
                        record.student_id.name,
                        record.offering_id.name,
                    )
                )
                raise ValidationError(error_message)

    @ssi_decorator.pre_open_check()
    def _10_check_quota(self):
        """Block opening this participant when the offering's quota is full.

        Compares the number of ``open`` participants already on the
        Offering against ``offering_id.quota_max``. A ``quota_max`` of
        0 means unlimited, so no check is performed in that case.
        Runs before the state is written, so raising here leaves the
        document in its previous state.

        :raises UserError: when the offering's maximum quota is
            already reached
        :return: None
        """
        self.ensure_one()
        quota_max = self.offering_id.quota_max
        if quota_max <= 0:
            return
        open_count = self.search_count(
            [
                ("id", "!=", self.id),
                ("offering_id", "=", self.offering_id.id),
                ("state", "=", "open"),
            ]
        )
        if open_count >= quota_max:
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Offering '%(offering)s' has reached its maximum quota of
%(quota)s
Solution: Increase the Offering's Maximum Quota, or cancel an
existing participant before opening a new one
"""
                )
                % {
                    "id": self.id,
                    "offering": self.offering_id.name,
                    "quota": quota_max,
                }
            )
            raise UserError(error_message)

    @ssi_decorator.pre_open_check()
    def _20_check_allocation_required(self):
        """Block opening this participant without an allocation.

        Runs after the quota check. When ``billing_mode`` is
        ``enrollment``, at least one ``allocation_ids`` line must
        exist so the fee can be billed through the enrollment's
        payment term(s); other billing modes are not affected.

        :raises UserError: when billed through enrollment without any
            allocation line
        :return: None
        """
        self.ensure_one()
        if self.billing_mode == "enrollment" and not self.allocation_ids:
            error_message = (
                _(
                    """
Context: Open extracurricular participant
Database ID: %(id)s
Problem: Billing Mode is 'Charged to Enrollment' but no Allocation
line is set
Solution: Add at least one Allocation line pointing to an enrollment
payment term before opening
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)

    @ssi_decorator.post_open_action()
    def _10_create_extra_detail(self):
        """Create one addendum fee line per allocation.

        Post-open hook: for every ``allocation_ids`` line, creates a
        ``school_enrollment_payment_term_extra_detail`` on the
        allocated payment term mirroring the allocation's product line
        values, and writes the created line back onto
        ``extra_detail_id`` for traceability.

        :return: None
        """
        self.ensure_one()
        Detail = self.env[  # pylint: disable=invalid-name
            "school_enrollment_payment_term_extra_detail"
        ]
        for allocation in self.allocation_ids:
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

    @ssi_decorator.post_cancel_action()
    def _10_remove_extra_detail(self):
        """Remove the addendum fee lines created by this participant.

        Post-cancel hook: rejects cancellation when any addendum fee
        line created from ``allocation_ids`` is already ``locked``
        (meaning the enrollment has already been opened around it);
        otherwise deletes the unlocked lines so the payment term's
        totals fall back to what they were before this participant
        was opened.

        :raises UserError: when an addendum fee line is locked
        :return: None
        """
        self.ensure_one()
        extra_details = self.allocation_ids.mapped("extra_detail_id")
        locked = extra_details.filtered("locked")
        if locked:
            error_message = (
                _(
                    """
Context: Cancel extracurricular participant
Database ID: %(id)s
Problem: An addendum fee line on the payment term is already locked
Solution: The enrollment has already been opened around this fee;
it can no longer be cancelled through this document
"""
                )
                % {"id": self.id}
            )
            raise UserError(error_message)
        extra_details.unlink()

    @api.model
    def _get_policy_field(self):
        """Return the list of policy boolean fields for this model.

        Extends the base list with the standard workflow policy
        fields used by this model's ``_policy_field_order``. No
        custom policy field is added beyond what the transaction
        mixins already provide.

        :return: list of policy field names
        :rtype: list
        """
        res = super()._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "cancel_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    @ssi_decorator.insert_on_form_view()
    def _insert_form_element(self, view_arch):
        if self._automatically_insert_view_element:
            view_arch = self._reconfigure_statusbar_visible(view_arch)
        return view_arch
