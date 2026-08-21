# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolExtracurricularParticipantAllocation(models.Model):
    """Represents one payment term a participant's fee is pinned to.

    Route A billing (charged to enrollment) needs the participant to
    say *which* payment term(s) of the student's enrollment absorb its
    fee, and in what amount -- a fee may be split across more than one
    term. Each allocation line becomes one
    ``school_enrollment_payment_term_extra_detail`` row on its payment
    term once the participant is opened; ``extra_detail_id`` traces
    that row back here.
    """

    _name = "school_extracurricular_participant_allocation"
    _description = "Extracurricular Participant Allocation"
    _order = "sequence, id"
    _inherit = [
        "mixin.product_line_account",
    ]

    participant_id = fields.Many2one(
        string="Extracurricular Participant",
        comodel_name="school_extracurricular_participant",
        required=True,
        ondelete="cascade",
        help="The extracurricular participant this allocation belongs to.",
    )
    payment_term_id = fields.Many2one(
        string="Payment Term",
        comodel_name="school_enrollment_payment_term",
        required=True,
        ondelete="restrict",
        help=("The enrollment payment term this participant's fee is " "allocated to."),
    )
    extra_detail_id = fields.Many2one(
        string="Payment Term Extra Detail",
        comodel_name="school_enrollment_payment_term_extra_detail",
        readonly=True,
        ondelete="set null",
        help=(
            "The addendum fee line created on the payment term from "
            "this allocation, automatically populated when the "
            "participant is opened."
        ),
    )
    product_id = fields.Many2one(required=True)
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="participant_id.currency_id",
        store=True,
        required=False,
        help="The billing currency, automatically taken from the participant.",
    )

    @api.constrains("payment_term_id", "participant_id")
    def _check_payment_term_enrollment(self):
        """Validate that the payment term belongs to the same enrollment.

        Rejects an allocation whose ``payment_term_id.enrollment_id``
        differs from ``participant_id.enrollment_id``; records where
        either field is still empty pass.

        :raises ValidationError: on enrollment mismatch
        :return: None
        """
        for record in self:
            if (
                record.payment_term_id
                and record.participant_id
                and record.payment_term_id.enrollment_id
                != record.participant_id.enrollment_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant allocation
Database ID: %s
Problem: Payment term '%s' does not belong to the same enrollment as
Participant '%s'
Solution: Select a Payment Term that belongs to the Participant's
Enrollment
"""
                    )
                    % (
                        record.id,
                        record.payment_term_id.name,
                        record.participant_id.name,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("payment_term_id")
    def _check_payment_term_not_invoiced(self):
        """Validate that the payment term is not already invoiced.

        Rejects an allocation whose ``payment_term_id.state`` is
        ``invoiced``; a record without a payment term passes.

        :raises ValidationError: when the payment term is invoiced
        :return: None
        """
        for record in self:
            if record.payment_term_id and record.payment_term_id.state == "invoiced":
                error_message = (
                    _(
                        """
Context: Set extracurricular participant allocation
Database ID: %s
Problem: Payment term '%s' is already invoiced
Solution: Select a Payment Term that has not been invoiced yet
"""
                    )
                    % (record.id, record.payment_term_id.name)
                )
                raise ValidationError(error_message)

    @api.constrains("price_subtotal", "participant_id")
    def _check_allocation_total(self):
        """Validate the allocated total matches the participant's fee.

        Skipped for a participant with no allocation lines at all --
        only enforced once ``allocation_ids`` starts being filled.
        Compares the sum of ``price_subtotal`` of every allocation of
        the participant against ``participant_id.amount_untaxed``.

        :raises ValidationError: on total mismatch
        :return: None
        """
        participants = self.mapped("participant_id")
        for participant in participants:
            if not participant.allocation_ids:
                continue
            allocated = sum(participant.allocation_ids.mapped("price_subtotal"))
            if (
                participant.currency_id.compare_amounts(
                    allocated, participant.amount_untaxed
                )
                != 0
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant allocation
Database ID: %s
Problem: Total allocation %s does not match Participant fee %s
Solution: Adjust the allocation lines so their total matches the
Participant's Untaxed Amount
"""
                    )
                    % (participant.id, allocated, participant.amount_untaxed)
                )
                raise ValidationError(error_message)
