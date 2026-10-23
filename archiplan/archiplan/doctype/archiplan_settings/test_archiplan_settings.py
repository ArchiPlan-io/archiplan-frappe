import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import get_url

from archiplan.archiplan.doctype.archiplan_settings.archiplan_settings import (
    create_archiplan_access,
    revoke_archiplan_access,
)


class TestArchiPlanSettings(FrappeTestCase):
    def test_schedule_link_requires_embed_path_prefix(self):
        settings = frappe.get_single("ArchiPlan Settings")
        settings.archiplan_url = "https://app.archiplan.io"
        settings.schedule_link = "https://app.archiplan.io/embed/schedule/abc"
        settings.validate()
        for invalid in ("https://elsewhere.invalid/embed/schedule/abc", "https://app.archiplan.io/other"):
            settings.schedule_link = invalid
            with self.assertRaises(frappe.ValidationError):
                settings.validate()

    def test_non_system_manager_cannot_manage_access(self):
        frappe.set_user("Administrator")
        create_archiplan_access()
        try:
            frappe.set_user("archiplan@archiplan.io")
            with self.assertRaises(frappe.PermissionError):
                create_archiplan_access()
            with self.assertRaises(frappe.PermissionError):
                revoke_archiplan_access()
        finally:
            frappe.set_user("Administrator")
            revoke_archiplan_access()

    def test_reader_role_has_read_only_sales_order_permission(self):
        frappe.set_user("Administrator")
        create_archiplan_access()
        try:
            frappe.set_user("archiplan@archiplan.io")
            self.assertTrue(frappe.has_permission("Sales Order", "read"))
            self.assertFalse(frappe.has_permission("Sales Order", "write"))
            self.assertFalse(frappe.has_permission("Sales Order", "create"))
            self.assertFalse(frappe.has_permission("Sales Order", "delete"))
        finally:
            frappe.set_user("Administrator")
            revoke_archiplan_access()

    def test_create_and_revoke_access(self):
        frappe.set_user("Administrator")
        credentials = create_archiplan_access()
        self.assertEqual(credentials["site_url"], get_url())
        self.assertTrue(credentials["api_key"])
        self.assertTrue(credentials["api_secret"])
        user = frappe.get_doc("User", "archiplan@archiplan.io")
        self.assertEqual(user.enabled, 1)
        self.assertEqual([row.role for row in user.roles], ["ArchiPlan Reader"])
        user.enabled = 0
        user.save(ignore_permissions=True)
        create_archiplan_access()
        user.reload()
        self.assertEqual(user.enabled, 1)
        self.assertEqual([row.role for row in user.roles], ["ArchiPlan Reader"])
        revoke_archiplan_access()
        user.reload()
        self.assertEqual(user.enabled, 0)
        self.assertFalse(user.api_key)
        self.assertFalse(user.api_secret)
