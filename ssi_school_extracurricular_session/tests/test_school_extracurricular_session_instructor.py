# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularSessionInstructor(YamlTransactionCase):
    """Scenario tests for the instructor roster and the Done gate.

    Covers ``school_extracurricular_offering_instructor``,
    ``school_extracurricular_session_instructor``, roster copying on
    ``school_extracurricular_session``, and the conditional Done gate
    on the two tracking switches.
    """

    def test_school_extracurricular_session_instructor(self):
        """Run the roster copy, conditional Done, and negative scenarios."""
        self.run_yaml_scenario(
            "test_data_school_extracurricular_session_instructor.yaml"
        )
