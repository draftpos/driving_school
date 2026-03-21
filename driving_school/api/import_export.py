# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json


ANSWER_MAP = {
	"1": "A",
	"2": "B",
	"3": "C",
	"A": "A",
	"B": "B",
	"C": "C"
}


def _normalize_answer(value):
	"""Normalize imported answer values to A/B/C."""
	if value in (None, ""):
		return "A"

	return ANSWER_MAP.get(str(value).strip().upper(), "A")


@frappe.whitelist()
def export_questions(exam=None):
	"""Export questions as JSON"""
	frappe.only_for("System Manager")

	filters = {}
	if exam:
		filters["exam"] = exam

	questions = frappe.get_all(
		"Driving School Question",
		filters=filters,
		fields=[
			"name", "question_text", "question_image",
			"exam", "options_are_images",
			"option_1", "option_1_image", "option_1_label",
			"option_2", "option_2_image", "option_2_label",
			"option_3", "option_3_image", "option_3_label",
			"correct_answer"
		]
	)

	return {
		"count": len(questions),
		"questions": questions
	}


@frappe.whitelist()
def import_questions(questions_json, exam=None):
	"""Import questions from JSON"""
	frappe.only_for("System Manager")

	if isinstance(questions_json, str):
		data = json.loads(questions_json)
	else:
		data = questions_json

	questions = data.get("questions", data) if isinstance(data, dict) else data

	imported = 0
	errors = []

	for q in questions:
		try:
			# Use provided exam or the one in the question data
			question_exam = exam or q.get("exam")

			if not question_exam:
				errors.append(f"Question '{q.get('question_text', 'Unknown')[:50]}' has no exam specified")
				continue

			# Check if exam exists
			if not frappe.db.exists("Driving School Exam", question_exam):
				# Create the exam if it doesn't exist
				frappe.get_doc({
					"doctype": "Driving School Exam",
					"exam_name": question_exam,
					"is_active": 1
				}).insert(ignore_permissions=True)

			# Create question
			question = frappe.get_doc({
				"doctype": "Driving School Question",
				"question_text": q.get("question_text") or q.get("question"),
				"question_image": q.get("question_image"),
				"exam": question_exam,
				"options_are_images": q.get("options_are_images", 0),
				"option_1": q.get("option_1") or (q.get("options", [None, None, None])[0] if q.get("options") else None),
				"option_1_image": q.get("option_1_image"),
				"option_1_label": q.get("option_1_label"),
				"option_2": q.get("option_2") or (q.get("options", [None, None, None])[1] if q.get("options") else None),
				"option_2_image": q.get("option_2_image"),
				"option_2_label": q.get("option_2_label"),
				"option_3": q.get("option_3") or (q.get("options", [None, None, None])[2] if q.get("options") else None),
				"option_3_image": q.get("option_3_image"),
				"option_3_label": q.get("option_3_label"),
				"correct_answer": _normalize_answer(q.get("correct_answer", "A"))
			})
			question.insert(ignore_permissions=True)
			imported += 1

		except Exception as e:
			errors.append(f"Error importing question: {str(e)}")

	frappe.db.commit()

	return {
		"imported": imported,
		"errors": errors
	}


@frappe.whitelist()
def export_exams():
	"""Export all exams with their questions"""
	frappe.only_for("System Manager")

	exams = frappe.get_all(
		"Driving School Exam",
		fields=["name", "exam_name", "description", "is_active", "license_class"]
	)

	for exam in exams:
		exam["questions"] = frappe.get_all(
			"Driving School Question",
			filters={"exam": exam.name},
			fields=[
				"question_text", "question_image",
				"options_are_images",
				"option_1", "option_1_image", "option_1_label",
				"option_2", "option_2_image", "option_2_label",
				"option_3", "option_3_image", "option_3_label",
				"correct_answer"
			]
		)

	return {
		"count": len(exams),
		"exams": exams
	}


@frappe.whitelist()
def import_exams(exams_json):
	"""Import exams with their questions from JSON"""
	frappe.only_for("System Manager")

	if isinstance(exams_json, str):
		data = json.loads(exams_json)
	else:
		data = exams_json

	exams = data.get("exams", data) if isinstance(data, dict) else data

	imported_exams = 0
	imported_questions = 0
	errors = []

	for e in exams:
		try:
			exam_name = e.get("exam_name") or e.get("name")

			# Check if exam already exists
			if frappe.db.exists("Driving School Exam", exam_name):
				exam = frappe.get_doc("Driving School Exam", exam_name)
			else:
				exam = frappe.get_doc({
					"doctype": "Driving School Exam",
					"exam_name": exam_name,
					"description": e.get("description"),
					"is_active": e.get("is_active", 1),
					"license_class": e.get("license_class")
				})
				exam.insert(ignore_permissions=True)
				imported_exams += 1

			# Import questions for this exam
			for q in e.get("questions", []):
				try:
					question = frappe.get_doc({
						"doctype": "Driving School Question",
						"question_text": q.get("question_text") or q.get("question"),
						"question_image": q.get("question_image"),
						"exam": exam.name,
						"options_are_images": q.get("options_are_images", 0),
						"option_1": q.get("option_1"),
						"option_1_image": q.get("option_1_image"),
						"option_1_label": q.get("option_1_label"),
						"option_2": q.get("option_2"),
						"option_2_image": q.get("option_2_image"),
						"option_2_label": q.get("option_2_label"),
						"option_3": q.get("option_3"),
						"option_3_image": q.get("option_3_image"),
						"option_3_label": q.get("option_3_label"),
						"correct_answer": _normalize_answer(q.get("correct_answer", "A"))
					})
					question.insert(ignore_permissions=True)
					imported_questions += 1
				except Exception as qe:
					errors.append(f"Error importing question in exam '{exam_name}': {str(qe)}")

		except Exception as ee:
			errors.append(f"Error importing exam: {str(ee)}")

	frappe.db.commit()

	return {
		"imported_exams": imported_exams,
		"imported_questions": imported_questions,
		"errors": errors
	}
