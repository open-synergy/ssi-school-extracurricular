# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class SchoolExtracurricularSession(models.Model):
    """Extends School Extracurricular Session with single Operating Unit.

    Adds ``operating_unit_id`` (via ``mixin.single_operating_unit``),
    but overrides it as a stored ``related`` field on
    ``offering_id.operating_unit_id`` instead of keeping the mixin's
    own user-default field: a session is one meeting of its Offering,
    so it always carries the same Operating Unit as the Offering it
    belongs to, and never the acting user's default. Because the
    field is ``related`` + ``store=True``, every session created by
    the Generate Sessions wizard
    (``school_extracurricular_session_generate``) picks up its
    Offering's Operating Unit automatically, with no change needed in
    the wizard itself -- Odoo recomputes/flushes the stored value
    directly, bypassing ``write()`` entirely (see ``write()`` below).
    """

    _name = "school_extracurricular_session"
    _inherit = [
        "school_extracurricular_session",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        related="offering_id.operating_unit_id",
        store=True,
        readonly=True,
        compute_sudo=True,
        default=False,
    )

    def write(self, vals):
        """Reject writing ``operating_unit_id`` directly.

        ``operating_unit_id`` is a stored ``related`` field mirroring
        ``offering_id.operating_unit_id``. Odoo marks ``related``
        fields readonly for the UI only -- a direct ``write()`` call
        (server action, import, RPC) still tunnels straight to the
        stored column regardless of that UI attribute, because no
        ``inverse`` method is generated for a field declared
        ``readonly=True``. This guard enforces the design's intent at
        the ORM level too: a session's Operating Unit must always
        follow its Offering, never be set independently. It does not
        interfere with the Offering-driven recompute described above,
        since that recompute assigns the field through Odoo's compute
        machinery, not through this model's ``write()``.

        :param vals: values to write, as passed to ``write()``.
        :raises UserError: when ``vals`` includes
            ``operating_unit_id``.
        :return: result of ``super().write()``.
        """
        if "operating_unit_id" in vals:
            error_message = _(
                """
Context: Change extracurricular session operating unit
Problem: Operating Unit cannot be written directly
Solution: Operating Unit is inherited from the session's Offering;
change the Offering's Operating Unit instead
"""
            )
            raise UserError(error_message)
        return super().write(vals)
