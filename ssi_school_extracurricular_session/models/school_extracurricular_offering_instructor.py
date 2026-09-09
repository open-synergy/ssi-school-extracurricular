# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolExtracurricularOfferingInstructor(models.Model):
    """Represents one template line of an offering's instructor roster.

    An Offering may be staffed by more than one person -- a head
    instructor and one or more assistants -- and that roster is fixed
    once for the whole term rather than typed again on every session.
    This model is that per-term template; every
    ``school_extracurricular_session`` created under the Offering
    copies it via ``_prepare_session_instructor_data``, so it does not
    itself carry attendance.
    """

    _name = "school_extracurricular_offering_instructor"
    _description = "Extracurricular Offering Instructor"
    _order = "offering_id, sequence"

    offering_id = fields.Many2one(
        string="Offering",
        comodel_name="school_extracurricular_offering",
        required=True,
        ondelete="cascade",
        help="The term's offering this roster line belongs to.",
    )
    sequence = fields.Integer(
        string="Sequence",
        required=True,
        default=5,
        help="Used to order this offering's instructor roster.",
    )
    role = fields.Selection(
        string="Role",
        selection=[
            ("head", "Head Instructor"),
            ("assistant", "Assistant Instructor"),
        ],
        required=True,
        default="head",
        help=(
            "Whether this person is the head instructor or an "
            "assistant instructor for the Offering."
        ),
    )
    teacher_id = fields.Many2one(
        string="Teacher",
        comodel_name="school_teacher",
        required=False,
        help=(
            "The teacher identified by this roster line. Exactly one "
            "of Teacher or Contact must be filled."
        ),
    )
    partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
        ondelete="restrict",
        required=False,
        help=(
            "The person or institution identified by this roster "
            "line, when not a school Teacher (e.g. an external "
            "coach or assistant). Exactly one of Teacher or Contact "
            "must be filled."
        ),
    )

    @api.constrains("teacher_id", "partner_id")
    def _check_identity(self):
        """Validate that exactly one identity reference is filled.

        Rejects a line where both ``teacher_id`` and ``partner_id``
        are empty, and a line where both are filled -- exactly one of
        the two must identify the person on this roster line.

        :raises ValidationError: on zero or two identity references
            filled
        """
        for record in self.sudo():
            if not record.teacher_id and not record.partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular offering instructor
Database ID: %s
Problem: Neither Teacher nor Contact is filled
Solution: Select either a Teacher or a Contact
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
            if record.teacher_id and record.partner_id:
                error_message = (
                    _(
                        """
Context: Set extracurricular offering instructor
Database ID: %s
Problem: Both Teacher and Contact are filled
Solution: Select only one of Teacher or Contact
"""
                    )
                    % (record.id,)
                )
                raise ValidationError(error_message)
