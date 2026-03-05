# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe


def after_install():
	"""Setup after app installation"""
	create_student_role()
	create_role_profile()
	setup_default_settings()


def create_student_role():
	"""Create Driving School Student role if it doesn't exist"""
	if not frappe.db.exists("Role", "Driving School Student"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Driving School Student",
			"desk_access": 0,  # No desk access
			"is_custom": 1,
			"home_page": "/assets/driving_school/driving-test/index.html"
		})
		role.insert(ignore_permissions=True)
		frappe.db.commit()
		print("Created Driving School Student role")


def create_role_profile():
	"""Create Driving School Student role profile"""
	if not frappe.db.exists("Role Profile", "Driving School Student"):
		role_profile = frappe.get_doc({
			"doctype": "Role Profile",
			"role_profile": "Driving School Student",
			"roles": [
				{"role": "Driving School Student"}
			]
		})
		role_profile.insert(ignore_permissions=True)
		frappe.db.commit()
		print("Created Driving School Student role profile")


def setup_default_settings():
	"""Setup default driving school settings"""
	settings = frappe.get_single("Driving School Settings")
	if not settings.school_name:
		settings.school_name = "Driving School"
		settings.exam_duration = 10
		settings.pass_mark = 67
		settings.questions_per_exam = 25
		settings.allow_retake = 1
		settings.retake_wait_days = 0
		settings.save(ignore_permissions=True)
		frappe.db.commit()
		print("Setup default settings")
