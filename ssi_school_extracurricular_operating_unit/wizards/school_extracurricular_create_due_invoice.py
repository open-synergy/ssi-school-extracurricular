# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, models
from odoo.exceptions import UserError


class SchoolExtracurricularCreateDueInvoice(models.TransientModel):
    """Propagates Operating Unit onto the consolidated Route B invoice.

    ``_prepare_invoice_data`` is the base module's own documented
    extension point for exactly this purpose (see its docstring:
    "override in a glue module (Operating Unit, for instance)").
    ``_check_offering_consistency`` is not documented as an extension
    point, but is a plain method already called by ``_create_invoice``
    before anything is created, so it is extended the same way to add
    an Operating Unit guard alongside the base module's own
    Journal/Account/Type guard.
    """

    _name = "school_extracurricular_create_due_invoice"
    _inherit = "school_extracurricular_create_due_invoice"

    def _check_offering_consistency(self):
        """Validate the base guard, then Operating Unit consistency.

        Extension point: after the base module's own Journal/Account/
        Type guard passes, rejects this run when the due terms'
        participants do not all share the same Operating Unit -- the
        header this wizard builds can only carry one Operating Unit,
        so a mismatch is rejected instead of picking one silently.

        :raises UserError: propagated from ``super()``, or when the
            due terms' participants disagree on Operating Unit
        """
        super()._check_offering_consistency()
        self.ensure_one()
        participants = self.term_ids.mapped("participant_id")
        operating_units = participants.mapped("operating_unit_id")
        if len(operating_units) > 1:
            error_message = (
                _(
                    """
Context: Create due invoice for extracurricular payment terms
Database ID: %s
Problem: The due payment terms' participants do not share the same
Operating Unit
Solution: Invoice the disagreeing participants' payment terms
separately, or align their Operating Unit first
"""
                )
                % (self.id,)
            )
            raise UserError(error_message)

    def _prepare_invoice_data(self, first_term):
        """Add this run's Operating Unit to the invoice header values.

        Extension point documented by the base module. Sourced from
        the first term's participant rather than from the Offering
        used for the rest of the header, since ``operating_unit_id``
        lives on ``school_extracurricular_participant`` in this
        module, not on ``school_extracurricular_offering`` alone --
        ``_check_offering_consistency`` above already guarantees every
        involved participant agrees, so any one of them is
        equivalent.

        :param first_term: the payment term (sequence, then id) whose
            participant supplies the Operating Unit
        :return: dict of ``customer_invoice`` values
        """
        self.ensure_one()
        result = super()._prepare_invoice_data(first_term)
        participant = first_term.participant_id
        result["operating_unit_id"] = participant.operating_unit_id.id
        return result
