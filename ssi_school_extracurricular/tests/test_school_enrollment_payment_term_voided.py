# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolEnrollmentPaymentTermVoided(YamlTransactionCase):
    """Scenario tests for the ``voided`` marker on the payment term.

    Covers ``_compute_total`` filtering ``detail_ids`` marked
    ``voided`` while still summing every ``extra_detail_ids`` line,
    and the ``_is_fully_voided()`` override that keeps a term
    invoiceable while it still carries an extracurricular addendum
    line, even when every regular detail line has been voided.
    """

    def test_school_enrollment_payment_term_voided(self):
        """Run the voided-marker positive and negative scenarios."""
        self.run_yaml_scenario("test_data_school_enrollment_payment_term_voided.yaml")
