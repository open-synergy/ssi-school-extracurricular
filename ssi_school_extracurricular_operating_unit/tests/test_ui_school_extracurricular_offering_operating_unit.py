# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so any fixture would fail before the
# browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularOfferingOperatingUnit(HttpSavepointCase):
    """Tour test for the Operating Unit delta of the Offering create form."""

    def test_create(self):
        """Run the delta create tour for ``school_extracurricular_offering``.

        IK: docs/school_extracurricular_offering/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_operating_unit_offering_create",
            login="admin",
        )
