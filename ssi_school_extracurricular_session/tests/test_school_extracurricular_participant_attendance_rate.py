# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularParticipantAttendanceRate(YamlTransactionCase):
    """Scenario tests for the participant's session attendance recap."""

    def test_school_extracurricular_participant_attendance_rate(self):
        """Run the attendance rate scenario across two Done sessions."""
        self.run_yaml_scenario(
            "test_data_school_extracurricular_participant_attendance_rate.yaml"
        )
