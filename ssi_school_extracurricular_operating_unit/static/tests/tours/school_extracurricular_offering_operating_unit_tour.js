/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular_operating_unit.school_extracurricular_offering_ou_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_offering/01-create.md
        // Delta-only tour (E1): asserts the Operating Unit field added by
        // this module is present on the create form. It does not fill in
        // or save the base module's own required fields -- that is
        // already covered by the base module's own create tour.
        tour.register(
            "ssi_school_extracurricular_operating_unit_offering_create",
            {
                test: true,
                url: "/web",
            },
            [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Extracurricular Offerings menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_offering"]',
                },
                {
                    content: "Extracurricular Offerings list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Offerings)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Click New",
                    trigger: ".o_list_button_add",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Form is open in edit mode",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Operating Unit field is present on the create form",
                    trigger: ".o_field_many2one[name='operating_unit_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
