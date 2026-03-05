# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DrivingSchoolExam(Document):
	def get_question_count(self):
		"""Get total number of questions for this exam"""
		return frappe.db.count("Driving School Question", {"exam": self.name})
