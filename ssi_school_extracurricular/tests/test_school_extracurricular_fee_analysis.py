# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularFeeAnalysis(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Scenario tests for ``school_extracurricular_fee_analysis``."""

    def test_school_extracurricular_fee_analysis(self):
        """Run the Route A, Route B, and access-restriction scenarios."""
        self.run_yaml_scenario("test_data_school_extracurricular_fee_analysis.yaml")
