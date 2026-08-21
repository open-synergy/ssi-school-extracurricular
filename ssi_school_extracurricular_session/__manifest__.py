# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Extracurricular Session",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, "
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "application": True,
    "depends": [
        "ssi_school_extracurricular",
    ],
    "data": [
        "security/ir_module_category/school_extracurricular_session.xml",
        "security/res_groups/school_extracurricular_session.xml",
        "security/ir_model_access/school_extracurricular_session.xml",
        "security/ir_model_access/cancel_extracurricular_session.xml",
        "menu.xml",
        "views/school_extracurricular_session.xml",
        "wizards/cancel_extracurricular_session.xml",
    ],
}
