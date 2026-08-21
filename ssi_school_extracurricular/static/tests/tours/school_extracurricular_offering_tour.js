/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular.school_extracurricular_offering_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_offering/01-create.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 3 — Fill in the required fields (Extracurricular, Academic Year,
                // Academic Term, Teacher, Start Date, End Date, Price Unit).
                {
                    content: "Select the Extracurricular",
                    trigger: ".o_field_many2one[name='extracurricular_id'] input",
                    run: "text TOUR-OFFERING-EXTRACURRICULAR",
                },
                {
                    content: "Pick the Extracurricular from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-OFFERING-EXTRACURRICULAR)",
                    in_modal: false,
                },
                {
                    content: "Select the Academic Year",
                    trigger: ".o_field_many2one[name='academic_year_id'] input",
                    run: "text TOUR-OFFERING-YEAR",
                },
                {
                    content: "Pick the Academic Year from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-OFFERING-YEAR)",
                    in_modal: false,
                },
                {
                    content: "Select the Academic Term",
                    trigger: ".o_field_many2one[name='academic_term_id'] input",
                    run: "text TOUR-OFFERING-TERM",
                },
                {
                    content: "Pick the Academic Term from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-OFFERING-TERM)",
                    in_modal: false,
                },
                {
                    content: "Select the Teacher",
                    trigger: ".o_field_many2one[name='teacher_id'] input",
                    run: "text TOUR-OFFERING-TEACHER",
                },
                {
                    content: "Pick the Teacher from the dropdown",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-OFFERING-TEACHER)",
                    in_modal: false,
                },
                {
                    content: "Fill in Start Date",
                    trigger: ".o_field_widget[name='date_start'] input",
                    run: "text 07/01/2026",
                },
                {
                    content: "Fill in End Date",
                    trigger: ".o_field_widget[name='date_end'] input",
                    run: "text 12/31/2026",
                },
                {
                    content: "Fill in Price Unit",
                    trigger: "input.o_field_widget[name='price_unit']",
                    run: "text 150000.0",
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

        // IK: docs/school_extracurricular_offering/02-edit.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record to edit",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-EDIT) .o_data_cell:first",
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
                    trigger: "input.o_field_widget[name='price_unit']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text 175000.0",
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

        // IK: docs/school_extracurricular_offering/03-delete.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to delete.
                {
                    content: "Open the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-DELETE) .o_data_cell:first",
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
                        ".breadcrumb-item.o_back_button a:contains(Extracurricular Offerings)",
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

        // IK: docs/school_extracurricular_offering/04-confirm.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_confirm",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to confirm.
                {
                    content: "Open the record to confirm",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-CONFIRM) .o_data_cell:first",
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

        // IK: docs/school_extracurricular_offering/05-approve.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_approve",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to approve.
                {
                    content: "Open the record to approve",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-APPROVE) .o_data_cell:first",
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

        // IK: docs/school_extracurricular_offering/06-reject.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_reject",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to reject.
                {
                    content: "Open the record to reject",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-REJECT) .o_data_cell:first",
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

        // IK: docs/school_extracurricular_offering/09-finish.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_finish",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to finish.
                {
                    content: "Open the record to finish",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-FINISH) .o_data_cell:first",
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

        // IK: docs/school_extracurricular_offering/10-cancel.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_cancel",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to cancel.
                {
                    content: "Open the record to cancel",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-CANCEL) .o_data_cell:first",
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
                    trigger: ".o_statusbar_buttons button:contains(Cancel)",
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
                    run: "text TOUR-OFFERING-CANCEL-REASON",
                },
                {
                    content: "Pick the reason",
                    trigger:
                        ".ui-autocomplete .ui-menu-item a:contains(TOUR-OFFERING-CANCEL-REASON)",
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

        // IK: docs/school_extracurricular_offering/12-restart.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_offering_restart",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Extracurricular Offerings menu.
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

                // Flow 2 — Open the record to restart.
                {
                    content: "Open the record to restart",
                    trigger:
                        ".o_data_row:contains(TOUR-OFFERING-RESTART) .o_data_cell:first",
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
