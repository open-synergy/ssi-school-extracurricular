# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class SchoolExtracurricularParticipant(models.Model):
    """Extends School Extracurricular Participant with single Operating Unit.

    Adds ``operating_unit_id`` (via ``mixin.single_operating_unit``). The
    field defaults to the current user's default Operating Unit like any
    other ``mixin.single_operating_unit`` consumer, but
    ``onchange_operating_unit_id`` overwrites that default with the
    selected Offering's own Operating Unit as soon as an Offering is
    picked in the form -- the user may still change it afterwards, since
    a participant's fee can be billed to an operating unit different
    from its Offering's. ``_10_create_extra_detail`` additionally
    propagates this participant's Operating Unit onto every addendum fee
    line (``school_enrollment_payment_term_extra_detail``) it creates on
    the enrollment's payment term (Route A), so the addendum line is
    never left on the creating user's default Operating Unit instead of
    the participant's own.
    """

    _name = "school_extracurricular_participant"
    _inherit = [
        "school_extracurricular_participant",
        "mixin.single_operating_unit",
    ]

    operating_unit_id = fields.Many2one(
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )

    @api.onchange(
        "offering_id",
    )
    def onchange_operating_unit_id(self):
        """Copy the Operating Unit from the selected Offering.

        Resets to ``False`` when no Offering is selected, so the field
        never carries a stale value from a previously selected
        Offering. Runs after the mixin's own create-time default, so
        the Offering's Operating Unit wins over the current user's
        default Operating Unit whenever an Offering is picked through
        the form; the user may still change it afterwards.
        """
        self.operating_unit_id = False
        if self.offering_id:
            self.operating_unit_id = self.offering_id.operating_unit_id

    @ssi_decorator.post_open_action()
    def _10_create_extra_detail(self):
        """Create the addendum fee lines, then stamp them with this OU.

        Extension point: no ``_prepare_*`` seam exists for the addendum
        fee line's create values in the base module (the dict is built
        inline), so this wraps ``super()`` -- which creates one
        ``school_enrollment_payment_term_extra_detail`` per
        ``allocation_ids`` line exactly as the base module does -- and
        writes ``operating_unit_id`` onto every line it just created,
        sourced from this participant's own Operating Unit. Skipped
        entirely when this participant has no Operating Unit, so an
        empty value is not force-written over whatever default the
        addendum line's own ``mixin.single_operating_unit`` gave it.

        :return: None
        """
        super()._10_create_extra_detail()
        self.ensure_one()
        if self.operating_unit_id:
            self.allocation_ids.mapped("extra_detail_id").write(
                {"operating_unit_id": self.operating_unit_id.id}
            )
