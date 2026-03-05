# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe


def on_login(login_manager):
	"""Redirect Driving School Students to test page after login"""
	user = login_manager.user

	if user == "Administrator" or user == "Guest":
		return

	# Check if user has Driving School Student role
	user_roles = frappe.get_roles(user)

	if "Driving School Student" in user_roles:
		# Set redirect to test page
		frappe.local.response["home_page"] = "/student-test"
		frappe.cache.hset("home_page", user, "/student-test")
