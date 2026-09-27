# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

REJECTED_TERM_STATES = ("invoiced", "paid", "voided", "cancelled")


class SchoolExtracurricularParticipantAdmissionAllocation(models.Model):
    """Represents one admission payment term a participant's fee is
    pinned to.

    Twin of ``school_extracurricular_participant_allocation``, but
    pointing at a ``school_admission_payment_term`` instead of an
    enrollment payment term -- used when the participant's Billing
    Mode is ``admission``. Each allocation line becomes one
    ``school_admission_payment_term_extra_detail`` row on its payment
    term once the participant is opened; ``extra_detail_id`` traces
    that row back here.
    """

    _name = "school_extracurricular_participant_admission_allocation"
    _description = "Extracurricular Participant Admission Allocation"
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
        comodel_name="school_admission_payment_term",
        required=True,
        ondelete="restrict",
        help=("The admission payment term this participant's fee is " "allocated to."),
    )
    extra_detail_id = fields.Many2one(
        string="Payment Term Extra Detail",
        comodel_name="school_admission_payment_term_extra_detail",
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
    def _check_payment_term_admission(self):
        """Validate that the payment term belongs to the same admission.

        Rejects an allocation whose ``payment_term_id.admission_id``
        differs from ``participant_id.admission_id``; records where
        either field is still empty pass.

        :raises ValidationError: on admission mismatch
        :return: None
        """
        for record in self:
            if (
                record.payment_term_id
                and record.participant_id
                and record.payment_term_id.admission_id
                != record.participant_id.admission_id
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant admission allocation
Database ID: %s
Problem: Payment term '%s' does not belong to the same admission as
Participant '%s'
Solution: Select a Payment Term that belongs to the Participant's
Admission
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
    def _check_payment_term_not_billed(self):
        """Validate that the payment term is not already billed.

        Rejects an allocation whose ``payment_term_id.state`` is
        ``invoiced``, ``paid``, ``voided`` or ``cancelled``; a record
        without a payment term passes.

        :raises ValidationError: when the payment term is already
            billed, voided or cancelled
        :return: None
        """
        for record in self:
            if (
                record.payment_term_id
                and record.payment_term_id.state in REJECTED_TERM_STATES
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant admission allocation
Database ID: %s
Problem: Payment term '%s' is already %s
Solution: Select a Payment Term that is not invoiced, paid, voided or
cancelled
"""
                    )
                    % (
                        record.id,
                        record.payment_term_id.name,
                        record.payment_term_id.state,
                    )
                )
                raise ValidationError(error_message)

    @api.constrains("price_subtotal", "participant_id")
    def _check_allocation_total(self):
        """Validate the allocated total matches the participant's fee.

        Skipped for a participant with no allocation lines at all --
        only enforced once ``admission_allocation_ids`` starts being
        filled. Compares the sum of ``price_subtotal`` of every
        allocation of the participant against
        ``participant_id.amount_untaxed``.

        :raises ValidationError: on total mismatch
        :return: None
        """
        participants = self.mapped("participant_id")
        for participant in participants:
            if not participant.admission_allocation_ids:
                continue
            allocated = sum(
                participant.admission_allocation_ids.mapped("price_subtotal")
            )
            if (
                participant.currency_id.compare_amounts(
                    allocated, participant.amount_untaxed
                )
                != 0
            ):
                error_message = (
                    _(
                        """
Context: Set extracurricular participant admission allocation
Database ID: %s
Problem: Total allocation %s does not match Participant fee %s
Solution: Adjust the allocation lines so their total matches the
Participant's Untaxed Amount
"""
                    )
                    % (participant.id, allocated, participant.amount_untaxed)
                )
                raise ValidationError(error_message)
