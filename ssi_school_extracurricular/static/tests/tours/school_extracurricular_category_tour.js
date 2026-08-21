/* Copyright 2026 OpenSynergy Indonesia */
/* Copyright 2026 PT. Simetri Sinergi Indonesia */
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */
odoo.define(
    "ssi_school_extracurricular.school_extracurricular_category_tour",
    function (require) {
        "use strict";

        var tour = require("web_tour.tour");

        // IK: docs/school_extracurricular_category/01-create.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_category_create",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Configuration > Categories menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_configuration"]',
                },
                {
                    content: "Open the Categories menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.school_extracurricular_category_menu"]',
                },
                {
                    // Gate: wait for the Categories action itself, not the app
                    // landing action still visible while it loads.
                    content: "Extracurricular Categories list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Categories)",
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

                // Flow 3 — Fill in the required fields (Name, Code).
                {
                    content: "Fill in Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-CATEGORY-CREATE",
                },
                {
                    content: "Fill in Code",
                    trigger: ".o_field_widget[name='code']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text /",
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

        // IK: docs/school_extracurricular_category/02-edit.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_category_edit",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Configuration > Categories menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_configuration"]',
                },
                {
                    content: "Open the Categories menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.school_extracurricular_category_menu"]',
                },
                {
                    content: "Extracurricular Categories list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Categories)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 — Find and open the record to edit.
                {
                    content: "Open the record to edit",
                    trigger:
                        ".o_data_row:contains(TOUR-CATEGORY-EDIT) .o_data_cell:first",
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
                    content: "Change Name",
                    trigger: ".o_field_widget[name='name']",
                    extra_trigger: ".o_form_view.o_form_editable",
                    run: "text TOUR-CATEGORY-EDIT-DONE",
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

        // IK: docs/school_extracurricular_category/03-delete.md
        tour.register(
            "ssi_school_extracurricular_school_extracurricular_category_delete",
            {
                test: true,
                url: "/web",
            },
            [
                // Flow 1 — Open the Extracurricular > Configuration > Categories menu.
                tour.stepUtils.showAppsMenuItem(),
                {
                    content: "Open the Extracurricular app",
                    trigger:
                        '.o_app[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_root"]',
                },
                {
                    content: "Open the Configuration menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.menu_extracurricular_configuration"]',
                },
                {
                    content: "Open the Categories menu",
                    trigger:
                        ".o_menu_sections " +
                        '[data-menu-xmlid="ssi_school_extracurricular.school_extracurricular_category_menu"]',
                },
                {
                    content: "Extracurricular Categories list is displayed",
                    trigger:
                        ".o_control_panel .breadcrumb-item.active:contains(Extracurricular Categories)",
                    extra_trigger: ".o_list_view",
                    run: function () {
                        // Assertion only; do not trigger the default click action.
                    },
                },

                // Flow 2 — Open the record to delete.
                {
                    content: "Open the record to delete",
                    trigger:
                        ".o_data_row:contains(TOUR-CATEGORY-DELETE) .o_data_cell:first",
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
                    // Item Action menu adalah komponen Owl; cocokkan LABEL PERSIS,
                    // bukan substring (bisa keliru menunjuk "Archive").
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
                        ".breadcrumb-item.o_back_button a:contains(Extracurricular Categories)",
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
    }
);
