# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo_yaml_test import YamlTransactionCase

from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSchoolExtracurricularOperatingUnit(
    YamlTransactionCase
):  # pylint: disable=too-few-public-methods
    """Cover Operating Unit handling on the extracurricular documents.

    Includes propagation to the Route A addendum fee line, propagation
    to the Route B invoice, record rule visibility, and the wizard's
    rejection of a mixed-Operating-Unit consolidation.
    """

    def test_school_extracurricular_operating_unit(self):
        """Run every Operating Unit scenario for the extracurricular models."""
        self.run_yaml_scenario("test_data_school_extracurricular_operating_unit.yaml")
