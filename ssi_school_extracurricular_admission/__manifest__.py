# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "School Extracurricular - Admission",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, "
    "Odoo Community Association (OCA)",
    "contributors": [
        "Andhitia Rama <andhitia.r@gmail.com>",
    ],
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_extracurricular",
        "ssi_school_admission",
        "web_tour",
    ],
    "data": [
        "security/ir_model_access/school_extracurricular_participant_admission_allocation.xml",
        "security/ir_model_access/school_admission_payment_term_extra_detail.xml",
        "views/school_extracurricular_participant.xml",
        "views/school_admission_payment_term.xml",
        "views/assets.xml",
    ],
    "demo": [],
}
