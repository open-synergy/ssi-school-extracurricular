# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularOfferingGroup(YamlTransactionCase):
    """Scenario tests for ``school_extracurricular_offering_group``."""

    def test_school_extracurricular_offering_group(self):
        """Run the quota, count, and negative scenarios for Groups."""
        self.run_yaml_scenario("test_data_school_extracurricular_offering_group.yaml")
