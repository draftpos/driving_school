# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExamAttempt(Document):
	def calculate_results(self):
		"""Calculate exam results based on answers"""
		if not self.answers:
			return

		correct = 0
		total = len(self.answers)

		for answer in self.answers:
			if answer.is_correct:
				correct += 1

		self.total_questions = total
		self.correct_answers = correct
		self.score_percentage = (correct / total * 100) if total > 0 else 0

		# Get pass mark from settings
		settings = frappe.get_single("Driving School Settings")
		pass_mark = settings.pass_mark or 67

		self.passed = 1 if self.score_percentage >= pass_mark else 0
