# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Extracurricular + Operating Unit",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_extracurricular",
        "ssi_operating_unit_mixin",
        "ssi_customer_invoice_operating_unit",
        "web_tour",
    ],
    "data": [
        "security/ir_module_category/school_extracurricular_operating_unit.xml",
        "security/res_group/school_extracurricular.xml",
        "security/ir_model_access/school_extracurricular_create_due_invoice.xml",
        "security/ir_rule/school_extracurricular_offering.xml",
        "security/ir_rule/school_extracurricular_participant.xml",
        "views/school_extracurricular_offering.xml",
        "views/school_extracurricular_participant.xml",
        "views/assets.xml",
    ],
}
