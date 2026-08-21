# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

# HttpSavepointCase -- NOT HttpCase. In 14.0 plain HttpCase does not set
# up ``cls.env`` in ``setUpClass``, so Pre-Condition fixtures below would
# fail before the browser even starts.
from odoo.tests import HttpSavepointCase, tagged


@tagged("post_install", "-at_install")
class TestUiSchoolExtracurricular(HttpSavepointCase):
    """Tour tests for the ``school_extracurricular`` work instructions."""

    @classmethod
    def setUpClass(cls):
        """Create the Category, School, and Extracurricular fixtures.

        The Category and School records are Pre-Condition data the create
        tour picks from the ``category_id``/``school_id`` many2one
        dropdowns; the two Extracurricular records are the records the
        edit and delete tours operate on. None of this is done by
        clicking through the UI.
        """
        super().setUpClass()
        cls.grade_type = cls.env["school_grade_type"].create(
            {
                "name": "TOUR-EXTRA-GRADE-TYPE",
                "code": "/",
            }
        )
        cls.school = cls.env["school"].create(
            {
                "name": "TOUR-EXTRA-SCHOOL",
                "code": "/",
                "grade_type_id": cls.grade_type.id,
            }
        )
        cls.category = cls.env["school_extracurricular_category"].create(
            {
                "name": "TOUR-EXTRA-CATEGORY",
                "code": "/",
            }
        )
        cls.extracurricular_edit = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-EXTRACURRICULAR-EDIT",
                "code": "/",
                "category_id": cls.category.id,
                "school_id": cls.school.id,
            }
        )
        cls.extracurricular_delete = cls.env["school_extracurricular"].create(
            {
                "name": "TOUR-EXTRACURRICULAR-DELETE",
                "code": "/",
                "category_id": cls.category.id,
                "school_id": cls.school.id,
            }
        )

    def test_create(self):
        """Run the create tour for ``school_extracurricular``.

        IK: docs/school_extracurricular/01-create.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_create",
            login="admin",
        )

    def test_edit(self):
        """Run the edit tour for ``school_extracurricular``.

        IK: docs/school_extracurricular/02-edit.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_edit",
            login="admin",
        )

    def test_delete(self):
        """Run the delete tour for ``school_extracurricular``.

        IK: docs/school_extracurricular/03-delete.md
        """
        self.start_tour(
            "/web",
            "ssi_school_extracurricular_school_extracurricular_delete",
            login="admin",
        )
