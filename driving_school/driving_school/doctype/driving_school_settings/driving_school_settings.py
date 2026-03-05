# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DrivingSchoolSettings(Document):
	pass


def get_settings():
	"""Get driving school settings"""
	return frappe.get_single("Driving School Settings")
