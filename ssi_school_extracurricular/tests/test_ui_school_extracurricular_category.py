# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricularCategory(HttpSavepointCase):
    """Tour tests for the ``school_extracurricular_category`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the records the edit and delete tours operate on."""
        super().setUpClass()
        # IK Pre-Condition is prepared here, NOT by clicking through the UI.
        cls.category_edit = cls.env["school_extracurricular_category"].create(
            {
                "name": "TOUR-CATEGORY-EDIT",
                "code": "/",
            }
        )
        cls.category_delete = cls.env["school_extracurricular_category"].create(
            {
                "name": "TOUR-CATEGORY-DELETE",
                "code": "/",
            }
        )

    def test_create(self):
        """Run the create tour for ``school_extracurricular_category``.

        IK: docs/school_extracurricular_category/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_category_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_extracurricular_category``.

        IK: docs/school_extracurricular_category/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_category_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_extracurricular_category``.

        IK: docs/school_extracurricular_category/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_category_delete",
            login="admin",
        )
