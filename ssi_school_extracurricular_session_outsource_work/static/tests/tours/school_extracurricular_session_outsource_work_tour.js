/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular_session_outsource_work" +
        ".school_extracurricular_session_outsource_work_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_session/05-done.md (extension)
        // Flow 1-3 are the base module's own Done flow (unchanged);
        // the steps after Done are this module's delta.
        tour.register(
            "ssi_school_extracurricular_session_outsource_work_" +
                "school_extracurricular_session_done",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the School > Extracurricular >
                // Extracurricular Session > Extracurricular Sessions menu.
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
                // "Extracurricular Session" is a level-3 grouping menuitem
                // with no action= -- 14.0 renders it as a non-clickable
                // dropdown header without data-menu-xmlid, so there is no
                // step for it. Go straight to the leaf below.
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

                // Flow 2 — Open the session to mark as done.
                {
                    content: "Open the session to mark as done",
                    trigger:
                        ".o_data_row:contains(TOUR-OW-OFFERING-TEACHER) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Done button.
                {
                    content: "Click the Done button",
                    trigger: ".o_statusbar_buttons button[name='action_done']",
                    extra_trigger: ".o_form_view",
                },
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Additional Post-Condition — one honor document was
                // created for the present external instructor, visible
                // on the new Outsource Work Logs tab.
                {
                    content: "Open the Outsource Work tab",
                    trigger: ".o_notebook .nav-link:contains(Outsource Work)",
                    extra_trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                },
                {
                    content: "One honor row is shown for the present instructor",
                    trigger:
                        ".o_notebook .tab-pane.active " +
                        ".o_field_widget[name='outsource_work_ids'] " +
                        ".o_data_row:contains(TOUR-OW-INSTRUCTOR)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
