/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular_session_operating_unit.school_extracurricular_session_ou_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_session/01-create.md
        // Delta-only tour (E1): asserts the Operating Unit label added by
        // this module is rendered on the create form. The field itself is
        // readonly and empty until an Offering is selected -- a readonly
        // field with no value is a zero-pixel box invisible to the tour
        // runner, so this anchors on the field LABEL, which is always
        // rendered with text, instead of the field widget itself. It does
        // not fill in or save the base module's own required fields --
        // that is already covered by the base module's own create tour.
        tour.register(
            "ssi_school_extracurricular_session_operating_unit_create",
            {
                test: true,
                url: "/web",
            },
            [
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular Session app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular_session.menu_extracurricular_session_root"]',
                },
                {
                    content: "Open the Extracurricular Sessions menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular_session.menu_extracurricular_session"]',
                },
                {
                    content: "Extracurricular Sessions list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Sessions)",
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
                    content: "Operating Unit label is displayed on the create form",
                    trigger: ".o_form_label:contains(Operating Unit)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
