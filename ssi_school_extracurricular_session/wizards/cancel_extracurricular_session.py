# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class CancelExtracurricularSession(models.TransientModel):
    """Collect the reason before cancelling an extracurricular session.

    Opened from ``school_extracurricular_session.action_cancel``. The
    session itself is not cancelled until this wizard's
    ``action_confirm`` is called with a non-empty reason.
    """

    _name = "cancel_extracurricular_session"
    _description = "Cancel Extracurricular Session"

    session_id = fields.Many2one(
        string="Session",
        comodel_name="school_extracurricular_session",
        required=True,
        help="The extracurricular session being cancelled.",
    )
    cancel_reason = fields.Text(
        string="Cancel Reason",
        help="Why this session's meeting is being cancelled.",
    )

    def action_confirm(self):
        """Cancel the linked session with the given reason.

        :return: nothing; rejected when ``cancel_reason`` is empty
        """
        for record in self.sudo():
            record._cancel_session()

    def _cancel_session(self):
        """Move the linked session to ``cancelled`` with the reason.

        Side effect: writes ``state`` and ``cancel_reason`` on the
        linked ``school_extracurricular_session``.

        :raises UserError: when ``cancel_reason`` is empty
        """
        self.ensure_one()
        if not self.cancel_reason:
            error_message = (
                _(
                    """
Context: Cancel extracurricular session
Database ID: %s
Problem: Cancel Reason is empty
Solution: Fill in a Cancel Reason before cancelling the session
"""
                )
                % (self.session_id.id,)
            )
            raise UserError(error_message)
        self.session_id.write(
            {
                "state": "cancelled",
                "cancel_reason": self.cancel_reason,
            }
        )
