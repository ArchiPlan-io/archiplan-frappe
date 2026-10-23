frappe.ui.form.on("ArchiPlan Settings", {
    refresh(frm) {
        frm.add_custom_button(__("Create ArchiPlan access"), () => {
            frappe.call({
                method: "archiplan.archiplan.doctype.archiplan_settings.archiplan_settings.create_archiplan_access",
                freeze: true,
                callback: ({ message }) => {
                    const dialog = new frappe.ui.Dialog({
                        title: __("ArchiPlan API access"),
                        fields: [
                            { fieldtype: "Data", fieldname: "site_url", label: __("Site URL"), read_only: 1, default: message.site_url },
                            { fieldtype: "Data", fieldname: "api_key", label: __("API key"), read_only: 1, default: message.api_key },
                            { fieldtype: "Data", fieldname: "api_secret", label: __("API secret (shown once)"), read_only: 1, default: message.api_secret },
                        ],
                    });
                    dialog.set_primary_action(__("Close"), () => dialog.hide());
                    dialog.show();
                    dialog.$wrapper.find(".modal-body input").each(function () {
                        const button = $("<button class='btn btn-xs btn-default' type='button'>" + __("Copy") + "</button>");
                        button.on("click", () => navigator.clipboard.writeText(this.value));
                        $(this).after(button);
                    });
                },
            });
        });
        frm.add_custom_button(__("Revoke access"), () => {
            frappe.call({ method: "archiplan.archiplan.doctype.archiplan_settings.archiplan_settings.revoke_archiplan_access", freeze: true, callback: () => frappe.show_alert(__("ArchiPlan access revoked")) });
        });
    },
});
