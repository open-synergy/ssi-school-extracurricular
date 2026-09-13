# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularSessionMonitoring(YamlTransactionCase):
    """Scenario tests for the session journal and Monitor approval.

    Covers ``action_confirm``, the ``mixin.multiple_approval``
    approve/reject flow raised on top of the session's own
    ``planned``/``done``/``cancelled`` state, the
    ``is_teacher_present``/``monitoring_note`` verification gate,
    and ``present_count``.
    """

    def test_school_extracurricular_session_monitoring(self):
        """Run the confirm, approve, present count, and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_extracurricular_session_monitoring.yaml"
        )
