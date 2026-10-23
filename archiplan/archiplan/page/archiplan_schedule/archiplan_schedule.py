import frappe
from frappe import _


@frappe.whitelist()
def get_schedule_link():
    if frappe.session.user == "Guest":
        frappe.throw(_("Not permitted"), frappe.PermissionError)
    return frappe.db.get_single_value("ArchiPlan Settings", "schedule_link") or ""
