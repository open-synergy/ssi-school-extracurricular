/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular_session.school_extracurricular_session_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_session/01-create.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 3 — Fill in the required fields (Offering, Date, Start
                // Time, End Time).
                {
                    content: "Select the Offering",
                    trigger: ".o_field_many2one[name='offering_id'] input",
                    run: "text TOUR-SESSION-OFFERING",
                },
                {
                    content: "Pick the Offering from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-SESSION-OFFERING)",
                    in_modal: false,
                },
                {
                    content: "Fill in Date",
                    trigger: ".o_field_widget[name='date'] input",
                    run: "text 07/15/2026",
                },
                {
                    content: "Fill in Start Time",
                    trigger: ".o_field_widget[name='time_start']",
                    run: "text 09:00",
                },
                {
                    content: "Fill in End Time",
                    trigger: ".o_field_widget[name='time_end']",
                    run: "text 10:00",
                },

                // Flow 4 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/02-edit.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record to edit",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-EDIT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Click the Edit button",
                    trigger: ".o_form_button_edit",
                },
                {
                    content: "Form is now editable",
                    trigger: ".o_form_view.o_form_editable",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Change the required fields.
                {
                    content: "Change the Topic",
                    trigger: ".o_field_widget[name='topic']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-SESSION-EDITED-TOPIC",
                },

                // Flow 4 — Click Save.
                {
                    content: "Save the record",
                    trigger: ".o_form_button_save",
                },
                {
                    content: "Record is saved",
                    trigger: ".o_form_view.o_form_readonly",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/03-delete.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Select one or more records to delete.
                {
                    content: "Open the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-DELETE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click Action > Delete.
                {
                    content: "Open the Action menu",
                    trigger: ".o_cp_action_menus button:contains(Action)",
                },
                {
                    content: "Click Delete",
                    trigger: ".o_cp_action_menus .o_menu_item a",
                    run: function () {
                        var $delete = $(".o_cp_action_menus .o_menu_item a").filter(
                            function () {
                                return $(this).text().trim() === "Delete";
                            }
                        );
                        $delete[0].click();
                    },
                },

                // Flow 4 — Click OK to confirm.
                {
                    content: "Confirm deletion",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Click the list breadcrumb to return to the list",
                    trigger:
                        ".breadcrumb-item.o_back_button a:contains(Extracurricular Sessions)",
                },
                {
                    content: "Back to the list",
                    trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/04-fill-attendance.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_fill_attendance",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Open the session to fill attendance for.
                {
                    content: "Open the session to fill attendance for",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-FILL) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Open the Attendance tab",
                    trigger: ".o_notebook .nav-link:contains(Attendance)",
                    extra_trigger: ".o_form_view",
                },

                // Flow 3 — Click the Fill Attendance button.
                {
                    content: "Click the Fill Attendance button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_fill_attendance']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition — an attendance line is created for the
                // active Participant.
                {
                    content: "An attendance line is created for the Participant",
                    trigger:
                        ".o_field_widget[name='attendance_ids'] .o_data_row:contains(TOUR-SESSION-STUDENT)",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/05-done.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_done",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Open the session to mark as done.
                {
                    content: "Open the session to mark as done",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-DONE) .o_data_cell:first",
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

                // Post-Condition — status changes to Done.
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/06-cancel.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_cancel",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Open the session to cancel.
                {
                    content: "Open the session to cancel",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-CANCEL) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Cancel button.
                {
                    content: "Click the Cancel button",
                    trigger: ".o_statusbar_buttons button[name='action_cancel']",
                    extra_trigger: ".o_form_view",
                },
                {
                    // 14.0: no ".modal" prefix — the wizard's own trigger is
                    // searched INSIDE the modal, see odoo-development-ui-test
                    // skill patterns-dialogs-and-wizards.md §H.
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 4 — Fill in the Cancel Reason.
                {
                    content: "Fill in the Cancel Reason",
                    trigger: ".o_field_widget[name='cancel_reason']",
                    run: "text TOUR-SESSION-CANCEL-REASON",
                },

                // Flow 5 — Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Post-Condition — status changes to Cancelled.
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancelled'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/07-restart.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_restart",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Extracurricular
                // Sessions menu.
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

                // Flow 2 — Open the session to restart.
                {
                    content: "Open the session to restart",
                    trigger:
                        ".o_data_row:contains(TOUR-SESSION-RESTART) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Restart button.
                {
                    content: "Click the Restart button",
                    trigger: ".o_statusbar_buttons button[name='action_restart']",
                    extra_trigger: ".o_form_view",
                },

                // Post-Condition — status returns to Planned.
                {
                    content: "Status is Planned",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='planned'].btn-primary",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_session/08-generate.md
        tour.register(
            "ssi_school_extracurricular_session_school_extracurricular_session_generate",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular Session > Generate Sessions
                // menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular Session app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular_session.menu_extracurricular_session_root"]',
                },
                {
                    content: "Open the Generate Sessions menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular_session.menu_extracurricular_session_generate"]',
                },
                {
                    content: "The Generate Sessions wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 — Fill in the required fields (Offering, Start Time,
                // End Time).
                {
                    content: "Select the Offering",
                    trigger: ".o_field_many2one[name='offering_id'] input",
                    run: "text TOUR-SESSION-OFFERING",
                },
                {
                    content: "Pick the Offering from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-SESSION-OFFERING)",
                    in_modal: false,
                },
                {
                    content: "Fill in Start Time",
                    trigger: ".o_field_widget[name='time_start']",
                    run: "text 09:00",
                },
                {
                    content: "Fill in End Time",
                    trigger: ".o_field_widget[name='time_end']",
                    run: "text 10:00",
                },

                // Flow 3 — Check at least one weekday.
                {
                    content: "Check Monday",
                    trigger: ".o_field_widget[name='mon'] input",
                    run: "click",
                },

                // Flow 4 — Click the Generate button.
                {
                    content: "Click Generate",
                    trigger: ".modal-footer button[name='action_generate']",
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
