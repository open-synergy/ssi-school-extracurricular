# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class SchoolExtracurricularOffering(models.Model):
    """Cleans up honor logs before an offering is hard-deleted.

    ``school_extracurricular_session.offering_id`` uses
    ``ondelete="cascade"``, so deleting an offering deletes its
    sessions at the PostgreSQL level -- ``mixin.outsource_work_object
    .unlink()`` on the session is never called, and every honor
    document it logged would be left pointing at a session that no
    longer exists.
    """

    _name = "school_extracurricular_offering"
    _inherit = [
        "school_extracurricular_offering",
    ]

    def unlink(self):
        """Delete the honor logs of every session before cascading.

        Side effect: force-unlinks every ``outsource_work`` record
        logged against this offering's sessions, regardless of its
        state, since the whole document tree is about to be
        destroyed and none of it will remain to be settled.

        :return: result of the ``super().unlink()`` call
        """
        works = self.mapped("session_ids").mapped("outsource_work_ids")
        works.with_context(force_unlink=True).unlink()
        return super().unlink()
