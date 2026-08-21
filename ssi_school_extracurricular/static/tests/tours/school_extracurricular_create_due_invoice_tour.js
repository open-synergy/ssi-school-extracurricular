/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular.school_extracurricular_create_due_invoice_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_create_due_invoice/01-create-invoice.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_create_due_invoice_create_invoice",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Create Due Invoice menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Create Due Invoice menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_create_due_invoice"]',
                },
                {
                    content: "The Create Due Invoice wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 — Fill in the required fields (Student, Due Date Until).
                {
                    content: "Select the Student",
                    trigger: ".o_field_many2one[name='student_id'] input",
                    run: "text TOUR-WIZARD-STUDENT",
                },
                {
                    content: "Pick the Student from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-WIZARD-STUDENT)",
                    in_modal: false,
                },
                {
                    content: "Fill in Due Date Until",
                    trigger: ".o_field_widget[name='date_due_max'] input",
                    run: "text 06/30/2026",
                },

                // Flow 3 — The Payment Terms field automatically lists the due,
                // uninvoiced payment terms of the selected Student.
                {
                    content: "The due payment term is listed",
                    trigger:
                        ".o_field_widget[name='term_ids'] .o_badge_text:contains(TOUR-WIZARD-TERM)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 4 — Click the Create Due Invoice button.
                {
                    content: "Click Create Due Invoice",
                    trigger: ".modal-footer button[name='action_create_invoice']",
                },
                {
                    content: "The wizard dialog closes",
                    trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
