import json

import frappe
from frappe.permissions import add_permission

ROLE = "ArchiPlan Reader"


def after_install():
    ensure_role_permissions()
    make_workspace()


def after_migrate():
    ensure_role_permissions()
    make_workspace()


def ensure_role_permissions():
    if not frappe.db.exists("Role", ROLE):
        frappe.get_doc({"doctype": "Role", "role_name": ROLE, "desk_access": 0}).insert(
            ignore_permissions=True
        )
    for doctype in ("Sales Order", "Sales Order Item", "Item"):
        add_permission(doctype, ROLE, 0)
        name = frappe.db.get_value(
            "Custom DocPerm", {"parent": doctype, "role": ROLE, "permlevel": 0}, "name"
        )
        doc = frappe.get_doc("Custom DocPerm", name)
        doc.read = 1
        doc.write = 0
        doc.create = 0
        doc.delete = 0
        doc.submit = 0
        doc.cancel = 0
        doc.amend = 0
        doc.report = 0
        doc.export = 0
        doc.share = 0
        doc.print = 0
        doc.email = 0
        doc.save(ignore_permissions=True)


def make_workspace():
    workspace = frappe.db.exists("Workspace", "ArchiPlan")
    doc = (
        frappe.get_doc("Workspace", "ArchiPlan")
        if workspace
        else frappe.get_doc({"doctype": "Workspace", "name": "ArchiPlan"})
    )
    doc.update(
        {
            "label": "ArchiPlan",
            "title": "ArchiPlan",
            "module": "ArchiPlan",
            "public": 1,
            "is_hidden": 0,
            "type": "Workspace",
            "content": json.dumps(
                [
                    {
                        "id": "archiplan-schedule",
                        "type": "shortcut",
                        "data": {"shortcut_name": "Schedule", "col": 6},
                    },
                    {
                        "id": "archiplan-settings",
                        "type": "shortcut",
                        "data": {"shortcut_name": "Settings", "col": 6},
                    },
                ]
            ),
        }
    )
    doc.set("shortcuts", [])
    doc.append(
        "shortcuts",
        {"label": "Schedule", "type": "Page", "link_to": "archiplan-schedule"},
    )
    doc.append(
        "shortcuts",
        {"label": "Settings", "type": "DocType", "link_to": "ArchiPlan Settings"},
    )
    doc.set("links", [])
    doc.append(
        "links",
        {
            "type": "Link",
            "label": "Schedule",
            "link_type": "Page",
            "link_to": "archiplan-schedule",
        },
    )
    doc.append(
        "links",
        {
            "type": "Link",
            "label": "Settings",
            "link_type": "DocType",
            "link_to": "ArchiPlan Settings",
        },
    )
    doc.save(ignore_permissions=True)
