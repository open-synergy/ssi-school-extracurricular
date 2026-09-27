/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular_admission.school_extracurricular_participant_admission_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_participant/01-create.md (delta E1)
        // Delta-only tour: navigation Flow comes from the base IK
        // (ssi_school_extracurricular), the assertion below comes from the
        // delta IK of this module. Stops after the assertion -- it does not
        // continue to Save/Confirm/Approve.
        tour.register(
            "ssi_school_extracurricular_admission_school_extracurricular_participant_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the School app",
                    trigger: '.o_app[data-menu-xmlid="ssi_school.menu_school_root"]',
                },
                {
                    content: "Open the Extracurricular menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Extracurricular Participants menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_participant"]',
                },
                {
                    content: "Extracurricular Participants list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Participants)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 — Click the New button.
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

                // Delta assertion — set Billing Mode to Charged to Admission and
                // assert the Admission / Admission Allocation fields appear.
                {
                    content: "Set Billing Mode to Charged to Admission",
                    trigger: "select.o_field_widget[name='billing_mode']",
                    run: "text Charged to Admission",
                },
                {
                    content: "Admission field is now visible",
                    trigger: ".o_field_widget[name='admission_id']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Admission Allocation field is now visible",
                    trigger: ".o_field_widget[name='admission_allocation_ids']",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
