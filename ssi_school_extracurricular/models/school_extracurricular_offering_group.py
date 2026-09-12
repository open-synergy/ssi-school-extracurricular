# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolExtracurricularOfferingGroup(models.Model):
    """Represents one batch of participants within an Offering.

    A single ``school_extracurricular_offering`` term opening is
    sometimes too large to run as one class -- a school opening one
    extracurricular activity for dozens of students often splits them
    into several batches, each with its own quota and coach(es),
    while still billing under the same term Offering. This model is
    that batch: a plain detail line of the Offering, not a document
    of its own -- its whole life cycle depends on the Offering that
    owns it. Every ``school_extracurricular_participant`` may
    optionally be placed into one Group belonging to the same
    Offering.
    """

    _name = "school_extracurricular_offering_group"
    _description = "Extracurricular Offering Group"
    _order = "sequence, id"

    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        required=True,
        ondelete="cascade",
        help="The term's offering this group is a batch of.",
    )
    name = fields.Char(
        string="Name",
        required=True,
        help="The label of this group, e.g. 'Mini Soccer 1'.",
    )
    code = fields.Char(
        string="Code",
        help=(
            "Optional short code for this group. When filled, it "
            "must be unique among the groups of the same Offering."
        ),
    )
    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Determines the display order of an Offering's groups.",
    )
    quota_max = fields.Integer(
        string="Maximum Quota",
        default=0,
        help=(
            "The maximum number of participants allowed to join this "
            "group. A value of 0 means there is no upper limit."
        ),
    )
    teacher_ids = fields.Many2many(
        string="Teachers",
        comodel_name="school_teacher",
        relation="rel_school_extracurricular_offering_group_2_teacher",
        column1="group_id",
        column2="teacher_id",
        help=(
            "The teacher(s) coaching this group. Left empty, this "
            "does NOT mean the group has no coach -- it means the "
            "group is coached by the Offering's own Teacher."
        ),
    )
    participant_ids = fields.One2many(
        string="Participants",
        comodel_name="school_extracurricular_participant",
        inverse_name="group_id",
        help="The participants currently placed in this group.",
    )
    participant_count = fields.Integer(
        string="Participant Count",
        compute="_compute_participant_count",
        store=True,
        compute_sudo=True,
        help="Number of participants currently in ``open`` state.",
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="Set to false to archive this group without deleting it.",
    )

    @api.depends(
        "participant_ids.state",
    )
    def _compute_participant_count(self):
        """Count this group's participants currently in ``open`` state.

        :return: nothing; assigns ``participant_count``
        """
        for record in self:
            result = len(
                record.participant_ids.filtered(
                    lambda participant: participant.state == "open"
                )
            )
            record.participant_count = result

    @api.constrains("code", "offering_id")
    def _check_code_unique_per_offering(self):
        """Reject a group whose Code duplicates another in the Offering.

        :raises ValidationError: when the condition method returns
            False
        :return: None
        """
        for record in self.sudo():
            if not record._check_code_unique_per_offering_condition():
                error_message = (
                    _(
                        """
Context: Set extracurricular offering group
Database ID: %s
Problem: Code '%s' is already used by another group on the same
Offering
Solution: Use a different Code, or leave it empty
"""
                    )
                    % (record.id, record.code)
                )
                raise ValidationError(error_message)

    def _check_code_unique_per_offering_condition(self):
        """Tell whether ``code`` is unique among this offering's groups.

        Extension point: override to relax or tighten the rule
        without touching the error message. A record without a code
        is always valid -- an empty code is not required to be
        unique.

        :return: True when valid; never raises
        :rtype: bool
        """
        self.ensure_one()
        if not self.code:
            return True
        duplicate = self.search(
            [
                ("id", "!=", self.id),
                ("offering_id", "=", self.offering_id.id),
                ("code", "=", self.code),
            ]
        )
        return not duplicate
