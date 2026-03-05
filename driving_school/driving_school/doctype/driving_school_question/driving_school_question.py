# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class DrivingSchoolQuestion(Document):
	def before_save(self):
		"""Validate options only before actual save, not during form interactions"""
		if self.options_are_images:
			if not self.option_1_image or not self.option_2_image or not self.option_3_image:
				frappe.throw("All option images are required when 'Options are Images' is checked")
		else:
			if not self.option_1 or not self.option_2 or not self.option_3:
				frappe.throw("All options are required")
