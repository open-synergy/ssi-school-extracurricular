# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date as datetime_date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolExtracurricularOffering(models.Model):
    """Represents one semester's opening of an extracurricular activity.

    The ``school_extracurricular`` catalog only states which
    extracurricular activities a school knows about; it cannot record
    who coaches it this term, how many students may join, or what fee
    applies, because the same activity reopens every academic term
    with a different teacher, quota, and price. This document is that
    per-term opening: it fixes the teacher, quota, period, and fee for
    one extracurricular activity in one school for one academic term.
    The approval workflow uses the standard multi-approval mixins:
    Draft -> Confirm -> Approve -> Open -> Done / Cancel.
    """

    _name = "school_extracurricular_offering"
    _inherit = [
        "mixin.transaction_cancel",
        "mixin.transaction_done",
        "mixin.transaction_open",
        "mixin.transaction_confirm",
    ]
    _description = "Extracurricular Offering"

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

    date = fields.Date(
        string="Date",
        default=lambda r: datetime_date.today(),
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date this extracurricular offering document was created.",
    )
    extracurricular_id = fields.Many2one(
        string="Extracurricular",
        comodel_name="school_extracurricular",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The extracurricular activity being opened this term.",
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="school_extracurricular_category",
        related="extracurricular_id.category_id",
        store=True,
        readonly=True,
        help=(
            "The category of the extracurricular activity, automatically "
            "populated from the selected Extracurricular."
        ),
    )
    school_id = fields.Many2one(
        string="School",
        comodel_name="school",
        related="extracurricular_id.school_id",
        store=True,
        readonly=True,
        help=(
            "The school offering this extracurricular activity, "
            "automatically populated from the selected Extracurricular."
        ),
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="school_academic_year",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The academic year this offering is opened for.",
    )
    academic_term_id = fields.Many2one(
        string="Academic Term",
        comodel_name="school_academic_term",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The academic term this offering is opened for. Must belong "
            "to the selected Academic Year."
        ),
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The coach/teacher in charge of this term's offering.",
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The date this term's offering starts running.",
    )
    date_end = fields.Date(
        string="End Date",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The date this term's offering ends running. Must not be "
            "earlier than the Start Date."
        ),
    )
    quota_min = fields.Integer(
        string="Minimum Quota",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The minimum number of students required to run this offering.",
    )
    quota_max = fields.Integer(
        string="Maximum Quota",
        default=0,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "The maximum number of students allowed to join this "
            "offering. A value of 0 means there is no upper limit."
        ),
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        default=lambda self: self.env.company.currency_id,
        help="The currency used for this offering's fee.",
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        comodel_name="product.pricelist",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The pricelist that may be used to derive this offering's fee.",
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
            "The product used to bill this offering's fee. Defaults to "
            "the Extracurricular's default Product when the "
            "Extracurricular is selected, but may be changed."
        ),
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
        help="The fee charged per student for this offering, before tax.",
    )
    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name="account.tax",
        relation="rel_school_extracurricular_offering_2_tax",
        column1="offering_id",
        column2="tax_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help="The taxes applied on top of the Price Unit of this offering.",
    )
    billing_mode = fields.Selection(
        string="Billing Mode",
        selection=[
            ("enrollment", "Charged to Enrollment"),
            ("standalone", "Separate Invoice"),
            ("free", "Free of Charge"),
        ],
        default="enrollment",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "How this offering's fee is billed: charged to the "
            "student's enrollment, invoiced separately, or free of "
            "charge."
        ),
    )
    billing_frequency = fields.Selection(
        string="Billing Frequency",
        selection=[
            ("one_time", "One Time"),
            ("recurring", "Every Payment Term"),
        ],
        default="one_time",
        required=True,
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
        help=(
            "How often this offering's fee is billed: once, or on "
            "every payment term."
        ),
    )

    participant_ids = fields.One2many(
        string="Participants",
        comodel_name="school_extracurricular_participant",
        inverse_name="offering_id",
        help="The students who have joined this offering.",
    )
    participant_count = fields.Integer(
        string="Participant Count",
        compute="_compute_participant_count",
        store=True,
        compute_sudo=True,
        help="Number of participants currently in ``open`` state.",
    )

    @api.depends(
        "participant_ids.state",
    )
    def _compute_participant_count(self):
        """Count this offering's participants currently in ``open`` state.

        :return: nothing; assigns ``participant_count``
        """
        for record in self:
            result = len(
                record.participant_ids.filtered(
                    lambda participant: participant.state == "open"
                )
            )
            record.participant_count = result

    @api.onchange(
        "extracurricular_id",
    )
    def onchange_product_id(self):
        self.product_id = False
        if self.extracurricular_id:
            self.product_id = self.extracurricular_id.product_id

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        """Validate that the offering does not end before it starts.

        Rejects a record whose ``date_end`` is earlier than its
        ``date_start``; records where either field is still empty
        pass.

        :raises ValidationError: on end date earlier than start date
        :return: None
        """
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end < record.date_start
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular offering period
Database ID: %s
Problem: End Date '%s' is earlier than Start Date '%s'
Solution: Select an End Date that is not earlier than the Start Date
"""
                    )
                    % (record.id, record.date_end, record.date_start)
                )
                raise ValidationError(error_message)

    @api.constrains("academic_term_id", "academic_year_id")
    def _check_term_year_match(self):
        """Validate that the academic term belongs to the year.

        Rejects a record whose ``academic_term_id.year_id`` differs
        from its ``academic_year_id``; records where either field is
        still empty pass.

        :raises ValidationError: on academic term/year mismatch
        :return: None
        """
        for record in self:
            if (
                record.academic_term_id
                and record.academic_year_id
                and record.academic_term_id.year_id != record.academic_year_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular offering academic term
Database ID: %s
Problem: Academic Term '%s' does not belong to Academic Year '%s'
Solution: Select an Academic Term that belongs to the selected Academic
Year
"""
                    )
                    % (
                        record.id,
                        record.academic_term_id.name,
                        record.academic_year_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("quota_min", "quota_max")
    def _check_quota_min_max(self):
        """Validate that the maximum quota is not below the minimum.

        Rejects a record whose ``quota_max`` is lower than its
        ``quota_min`` while ``quota_max`` is greater than 0; a
        ``quota_max`` of 0 means unlimited and is always allowed.

        :raises ValidationError: on maximum quota below minimum quota
        :return: None
        """
        for record in self:
            if record.quota_max > 0 and record.quota_max < record.quota_min:
                error_message = (
                    _(
                        """
Context: Set extracurricular offering quota
Database ID: %s
Problem: Maximum Quota '%s' is lower than Minimum Quota '%s'
Solution: Set a Maximum Quota that is not lower than the Minimum Quota,
or leave it at 0 for no upper limit
"""
                    )
                    % (record.id, record.quota_max, record.quota_min)
                )
                raise ValidationError(error_message)

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
