# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Extracurricular Session + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_extracurricular_session",
        "ssi_school_extracurricular_operating_unit",
        "ssi_operating_unit_mixin",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/school_extracurricular_session_operating_unit.xml",
        "security/res_group/school_extracurricular_session.xml",
        "security/ir_rule/school_extracurricular_session.xml",
        "views/school_extracurricular_session.xml",
        "views/assets.xml",
    ],
}
