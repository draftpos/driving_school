# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe


# def on_login(login_manager):
# 	"""Redirect Driving School Students to test page after login"""
# 	user = login_manager.user

# 	if user == "Administrator" or user == "Guest":
# 		return

# 	# Check if user has Driving School Student role
# 	user_roles = frappe.get_roles(user)

# 	if "Driving School Student" in user_roles:
# 		# Set redirect to test page
# 		frappe.local.response["home_page"] = "/student-test"
# 		frappe.cache.hset("home_page", user, "/student-test")



def on_login(login_manager):
    """Redirect Driving School Students to test page after login"""
    user = login_manager.user

    if user in ("Administrator", "Guest"):
        return

    user_roles = frappe.get_roles(user)
    if "Driving School Student" in user_roles:
        frappe.local.response["type"] = "redirect"
        frappe.local.response["location"] = "/student-test"

@frappe.whitelist(allow_guest=True)
def logout():
    """Custom logout endpoint"""
    frappe.local.login_manager.logout()

    frappe.local.response["message"] = "Logged out"
    frappe.local.response["type"] = "redirect"
    frappe.local.response["location"] = "/login"   # change if needed