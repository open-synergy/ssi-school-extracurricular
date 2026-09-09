# Copyright 2026 OpenSynergy Indonesia
# Copyright 2026 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "School Extracurricular Session - Outsource Work Integration",
    "version": "14.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia, "
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "application": False,
    "depends": [
        "ssi_school_extracurricular_session",
        "ssi_outsource_work",
        "ssi_outsource_work_rate",
        "web_tour",
    ],
    "data": [
        "views/school_extracurricular_offering.xml",
        "views/school_extracurricular_session.xml",
        "views/assets.xml",
    ],
}
