# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so any fixture would fail before the
# browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularParticipantOperatingUnit(HttpSavepointCase):
    """Tour test for the Operating Unit delta of the Participant create
    form.
    """

    def test_create(self):
        """Run the delta create tour for the Participant create form.

        IK: docs/school_extracurricular_participant/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_operating_unit_participant_create",
            login="admin",
        )
