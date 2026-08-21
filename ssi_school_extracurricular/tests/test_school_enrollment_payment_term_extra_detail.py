# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermExtraDetail(YamlTransactionCase):
    """Scenario tests for Route A extracurricular billing (addendum).

    Covers the addendum fee line created on
    ``school_enrollment_payment_term`` from an extracurricular
    participant's ``allocation_ids`` -- totals, invoicing, cancel, and
    the allocation constraints.
    """

    def test_school_enrollment_payment_term_extra_detail(self):
        """Run the addendum billing positive and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_payment_term_extra_detail.yaml"
        )
