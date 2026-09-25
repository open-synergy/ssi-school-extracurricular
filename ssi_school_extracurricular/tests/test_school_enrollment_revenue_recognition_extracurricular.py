# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentRevenueRecognitionExtracurricular(YamlTransactionCase):
    """Scenario tests for extracurricular Revenue Recognition."""

    def test_school_enrollment_revenue_recognition_extracurricular(self):
        """Run the onchange, positive, and negative path scenarios."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_revenue_recognition_extracurricular.yaml"
        )
