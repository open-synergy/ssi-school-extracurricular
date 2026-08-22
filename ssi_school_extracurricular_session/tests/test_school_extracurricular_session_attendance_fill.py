# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularSessionAttendanceFill(YamlTransactionCase):
    """Scenario tests for ``action_fill_attendance``."""

    def test_school_extracurricular_session_attendance_fill(self):
        """Run the fill, idempotency, exclusion, and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_extracurricular_session_attendance_fill.yaml"
        )
