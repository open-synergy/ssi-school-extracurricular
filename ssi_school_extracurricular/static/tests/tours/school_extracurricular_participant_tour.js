/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular.school_extracurricular_participant_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_participant/01-create.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 3 — Fill in the required fields (Offering, Student, Enrollment,
                // Join Date).
                {
                    content: "Select the Offering",
                    trigger: ".o_field_many2one[name='offering_id'] input",
                    run: "text TOUR-PARTICIPANT-OFFERING",
                },
                {
                    content: "Pick the Offering from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-PARTICIPANT-OFFERING)",
                    in_modal: false,
                },
                {
                    content: "Select the Student",
                    trigger: ".o_field_many2one[name='student_id'] input",
                    run: "text TOUR-PARTICIPANT-CREATE-STUDENT",
                },
                {
                    content: "Pick the Student from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-PARTICIPANT-CREATE-STUDENT)",
                    in_modal: false,
                },
                {
                    content: "Select the Enrollment",
                    trigger: ".o_field_many2one[name='enrollment_id'] input",
                    run: "text TOUR-PARTICIPANT-ENROLLMENT",
                },
                {
                    content: "Pick the Enrollment from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-PARTICIPANT-ENROLLMENT)",
                    in_modal: false,
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

        // IK: docs/school_extracurricular_participant/02-edit.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record to edit",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-EDIT) .o_data_cell:first",
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
                    content: "Change Price Unit",
                    trigger: ".o_field_widget[name='price_unit'] input",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 250000.0",
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

        // IK: docs/school_extracurricular_participant/03-delete.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to delete.
                {
                    content: "Open the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-DELETE) .o_data_cell:first",
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
                        ".breadcrumb-item.o_back_button a:contains(Extracurricular Participants)",
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

        // IK: docs/school_extracurricular_participant/04-confirm.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_confirm",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to confirm.
                {
                    content: "Open the record to confirm",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-CONFIRM) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Confirm button.
                {
                    content: "Click the Confirm button",
                    trigger: ".o_statusbar_buttons button[name='action_confirm']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Waiting for Approval",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='confirm'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_participant/05-approve.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to approve.
                {
                    content: "Open the record to approve",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-APPROVE) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Approve button.
                {
                    content: "Click the Approve button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_approve_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Open",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='open'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_participant/06-reject.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_reject",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to reject.
                {
                    content: "Open the record to reject",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-REJECT) .o_data_cell:first",
                    extra_trigger: ".o_list_view",
                },
                {
                    content: "Record form is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 3 — Click the Reject button.
                {
                    content: "Click the Reject button",
                    trigger:
                        ".o_statusbar_buttons button[name='action_reject_approval']",
                    extra_trigger: ".o_form_view",
                },

                // Flow 4 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Rejected",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='reject'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_participant/09-finish.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_finish",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to finish.
                {
                    content: "Open the record to finish",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-FINISH) .o_data_cell:first",
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

                // Flow 4 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Done",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='done'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_participant/10-cancel.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_cancel",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to cancel.
                {
                    content: "Open the record to cancel",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-CANCEL) .o_data_cell:first",
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

                // Flow 4 — In the wizard that appears, select the Cancellation Reason.
                {
                    content: "Wizard is open",
                    trigger: ".o_form_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
                {
                    content: "Select the cancellation reason",
                    trigger: ".o_field_many2one[name='cancel_reason_id'] input",
                    run: "text TOUR-PARTICIPANT-CANCEL-REASON",
                },
                {
                    content: "Pick the reason",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-PARTICIPANT-CANCEL-REASON)",
                    in_modal: false,
                },

                // Flow 5 — Click Confirm.
                {
                    content: "Confirm the wizard",
                    trigger: ".modal-footer button[name='action_confirm']",
                },

                // Flow 6 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Cancelled",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='cancel'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );

        // IK: docs/school_extracurricular_participant/12-restart.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_participant_restart",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Participants menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
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

                // Flow 2 — Open the record to restart.
                {
                    content: "Open the record to restart",
                    trigger:
                        ".o_data_row:contains(TOUR-PARTICIPANT-RESTART) .o_data_cell:first",
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

                // Flow 4 — Click OK on the confirmation dialog.
                {
                    content: "Confirm the dialog",
                    trigger: ".modal-footer button.btn-primary",
                    in_modal: true,
                },
                {
                    content: "Status is Draft",
                    trigger:
                        ".o_statusbar_status .o_arrow_button[data-value='draft'].btn-primary",
                    extra_trigger: "body:not(:has(.modal))",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },
            ]
        );
    }
);
