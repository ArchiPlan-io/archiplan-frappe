import frappe
from frappe import _
from frappe.core.doctype.user.user import generate_keys
from frappe.model.document import Document
from frappe.utils import get_url

USER_EMAIL = "archiplan@archiplan.io"
ROLE = "ArchiPlan Reader"


class ArchiPlanSettings(Document):
    def validate(self):
        link = (self.schedule_link or "").strip()
        base = (self.archiplan_url or "").rstrip("/")
        if link and (not base or not link.startswith(base + "/embed/schedule/")):
            frappe.throw(_("Schedule link must start with the ArchiPlan URL followed by /embed/schedule/."))


@frappe.whitelist(methods=["POST"])
def create_archiplan_access():
    _require_system_manager()
    user = frappe.db.get_value("User", USER_EMAIL, "name")
    if user:
        account = frappe.get_doc("User", user)
        account.enabled = 1
        account.user_type = "System User"
    else:
        account = frappe.get_doc(
            {
                "doctype": "User",
                "email": USER_EMAIL,
                "first_name": "ArchiPlan",
                "full_name": "ArchiPlan",
                "user_type": "System User",
                "send_welcome_email": 0,
            }
        )
    account.set("roles", [])
    account.append("roles", {"role": ROLE})
    account.save(ignore_permissions=True)
    account.api_key = ""
    account.api_secret = ""
    account.save(ignore_permissions=True)
    credentials = generate_keys(account.name)
    return {"site_url": get_url(), **credentials}


@frappe.whitelist(methods=["POST"])
def revoke_archiplan_access():
    _require_system_manager()
    user = frappe.db.get_value("User", USER_EMAIL, "name")
    if user:
        account = frappe.get_doc("User", user)
        account.api_key = ""
        account.api_secret = ""
        account.enabled = 0
        account.save(ignore_permissions=True)
    return True


def _require_system_manager():
    if not frappe.has_permission("ArchiPlan Settings", "write"):
        frappe.throw(_("System Manager permission is required."), frappe.PermissionError)
