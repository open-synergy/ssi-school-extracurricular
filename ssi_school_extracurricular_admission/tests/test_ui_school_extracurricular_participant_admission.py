# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularParticipantAdmission(HttpSavepointCase):
    """Tour test for the ``school_extracurricular_participant`` E1 delta.

    The tour is delta-only (create form, assert field visibility, then
    stop) and needs no Pre-Condition fixture beyond the default demo
    data, so no ``setUpClass`` override is needed here.
    """

    def test_create(self):
        """Run the create delta tour for the admission billing route.

        IK: docs/school_extracurricular_participant/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_admission_school_extracurricular_participant_create",
            login="admin",
        )
