# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermExtraDetailForceDelete(YamlTransactionCase):
    """Scenario tests for force deleting a term with addendum lines.

    Covers the ``_clear_invoice_links_for_force_delete`` override on
    the payment term: force deleting a draft or open invoice that
    carries an extracurricular addendum line succeeds and leaves the
    addendum line without ``customer_invoice_line_id``, and a user
    without the force delete policy is rejected.
    """

    def test_school_enrollment_payment_term_extra_detail_force_delete(self):
        """Run the force delete positive and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_enrollment_payment_term_extra_detail_force_delete.yaml"
        )
