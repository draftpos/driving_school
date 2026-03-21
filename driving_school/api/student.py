# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import json
import random
from datetime import datetime


ANSWER_MAP = {
	"1": "A",
	"2": "B",
	"3": "C",
	"A": "A",
	"B": "B",
	"C": "C"
}


def _normalize_answer(value):
	"""Normalize answer values to A/B/C for consistent validation and scoring."""
	if value in (None, ""):
		return ""

	return ANSWER_MAP.get(str(value).strip().upper(), str(value).strip().upper())


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_settings():
	"""Get public driving school settings"""
	try:
		settings = frappe.get_single("Driving School Settings")
		return {
			"school_name": settings.school_name or "Driving School",
			"logo": settings.logo,
			"exam_duration": settings.exam_duration or 10,
			"pass_mark": settings.pass_mark or 67,
			"questions_per_exam": settings.questions_per_exam or 25,
			"allow_retake": settings.allow_retake if settings.allow_retake is not None else 1,
			"retake_wait_days": settings.retake_wait_days or 0
		}
	except Exception:
		# Return defaults if settings not configured
		return {
			"school_name": "Driving School",
			"logo": None,
			"exam_duration": 10,
			"pass_mark": 67,
			"questions_per_exam": 25,
			"allow_retake": 1,
			"retake_wait_days": 0
		}


@frappe.whitelist(allow_guest=True)
def register_student(first_name, last_name, id_number, license_class):
	"""Register or retrieve existing student"""
	try:
		# Validate inputs
		if not first_name or not last_name or not id_number:
			frappe.throw(_("First name, last name, and ID number are required"))

		# Check if student already exists
		existing = frappe.db.get_value(
			"Driving School Student",
			{"id_number": id_number},
			["name", "first_name", "last_name", "full_name", "license_class"],
			as_dict=True
		)

		if existing:
			# Update name and class if different
			if existing.first_name != first_name or existing.last_name != last_name or existing.license_class != license_class:
				student = frappe.get_doc("Driving School Student", existing.name)
				student.first_name = first_name
				student.last_name = last_name
				student.license_class = license_class
				student.save(ignore_permissions=True)
				frappe.db.commit()
				return {
					"student_id": student.name,
					"full_name": student.full_name,
					"id_number": id_number,
					"license_class": license_class,
					"is_new": False
				}
			return {
				"student_id": existing.name,
				"full_name": existing.full_name or f"{existing.first_name} {existing.last_name}",
				"id_number": id_number,
				"license_class": existing.license_class,
				"is_new": False
			}

		# Create new student
		student = frappe.get_doc({
			"doctype": "Driving School Student",
			"first_name": first_name,
			"last_name": last_name,
			"id_number": id_number,
			"license_class": license_class
		})
		student.insert(ignore_permissions=True)
		frappe.db.commit()

		return {
			"student_id": student.name,
			"full_name": student.full_name or f"{first_name} {last_name}",
			"id_number": id_number,
			"license_class": license_class,
			"is_new": True
		}
	except frappe.exceptions.ValidationError:
		raise
	except Exception as e:
		frappe.log_error(f"Student registration error: {str(e)}")
		frappe.throw(_("Failed to register student. Please try again."))


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_exams(student_id=None):
	"""Get list of available exams"""
	exams = frappe.get_all(
		"Driving School Exam",
		filters={"is_active": 1},
		fields=["name", "exam_name", "description", "license_class"]
	)

	settings = frappe.get_single("Driving School Settings")

	for exam in exams:
		# Get question count
		exam["question_count"] = frappe.db.count(
			"Driving School Question",
			{"exam": exam.name}
		)
		exam["duration"] = settings.exam_duration
		exam["pass_mark"] = settings.pass_mark

		# Check if student has attempted this exam
		if student_id:
			attempts = frappe.get_all(
				"Exam Attempt",
				filters={
					"student": student_id,
					"exam": exam.name,
					"status": "Completed"
				},
				fields=["name", "score_percentage", "passed", "end_time"],
				order_by="creation desc",
				limit=1
			)
			if attempts:
				exam["last_attempt"] = attempts[0]
				exam["has_attempted"] = True

				# Check if retake is allowed
				if settings.allow_retake and settings.retake_wait_days > 0:
					last_attempt_date = attempts[0].get("end_time")
					if last_attempt_date:
						from datetime import timedelta
						wait_until = last_attempt_date + timedelta(days=settings.retake_wait_days)
						exam["can_retake"] = datetime.now() >= wait_until
						exam["retake_available_date"] = wait_until
					else:
						exam["can_retake"] = True
				else:
					exam["can_retake"] = settings.allow_retake
			else:
				exam["has_attempted"] = False
				exam["can_retake"] = True

	return exams


@frappe.whitelist(allow_guest=True)
def start_exam(student_id, exam_name):
	"""Start a new exam attempt"""
	# Validate student
	if not frappe.db.exists("Driving School Student", student_id):
		frappe.throw(_("Invalid student"))

	# Validate exam
	exam = frappe.get_doc("Driving School Exam", exam_name)
	if not exam.is_active:
		frappe.throw(_("This exam is not active"))

	# Get settings
	settings = frappe.get_single("Driving School Settings")
	questions_per_exam = settings.questions_per_exam or 25

	# Get random questions for this exam
	all_questions = frappe.get_all(
		"Driving School Question",
		filters={"exam": exam_name},
		fields=[
			"name", "question_text", "question_image",
			"options_are_images",
			"option_1", "option_1_image", "option_1_label",
			"option_2", "option_2_image", "option_2_label",
			"option_3", "option_3_image", "option_3_label"
			# Note: correct_answer is NOT included - we don't send it to client
		]
	)

	if len(all_questions) < questions_per_exam:
		questions_per_exam = len(all_questions)

	if questions_per_exam == 0:
		frappe.throw(_("No questions available for this exam"))

	# Randomly select questions
	selected_questions = random.sample(all_questions, questions_per_exam)

	# Shuffle options for each question to prevent pattern memorization
	for q in selected_questions:
		q["question_number"] = selected_questions.index(q) + 1

	# Create exam attempt
	attempt = frappe.get_doc({
		"doctype": "Exam Attempt",
		"student": student_id,
		"exam": exam_name,
		"start_time": datetime.now(),
		"status": "In Progress",
		"total_questions": len(selected_questions),
		"questions_json": json.dumps([q["name"] for q in selected_questions])
	})
	attempt.insert(ignore_permissions=True)
	frappe.db.commit()

	return {
		"attempt_id": attempt.name,
		"exam_name": exam.exam_name,
		"questions": selected_questions,
		"duration_minutes": settings.exam_duration,
		"total_questions": len(selected_questions),
		"pass_mark": settings.pass_mark
	}


@frappe.whitelist(allow_guest=True)
def submit_exam(attempt_id, answers):
	"""Submit exam answers and calculate results"""
	# Validate attempt
	attempt = frappe.get_doc("Exam Attempt", attempt_id)

	if attempt.status != "In Progress":
		frappe.throw(_("This exam has already been submitted"))

	# Parse answers if string
	if isinstance(answers, str):
		answers = json.loads(answers)

	# Get correct answers and validate
	correct_count = 0
	for answer_data in answers:
		question_name = answer_data.get("question")
		selected_answer = _normalize_answer(answer_data.get("selected_answer"))

		if not question_name:
			continue

		# Get correct answer from database
		question = frappe.get_doc("Driving School Question", question_name)
		correct_answer = _normalize_answer(question.correct_answer)
		is_correct = selected_answer == correct_answer

		if is_correct:
			correct_count += 1

		# Add answer to attempt
		attempt.append("answers", {
			"question": question_name,
			"selected_answer": selected_answer,
			"correct_answer": correct_answer,
			"is_correct": is_correct
		})

	# Update attempt
	attempt.end_time = datetime.now()
	attempt.status = "Completed"
	attempt.calculate_results()
	attempt.save(ignore_permissions=True)
	frappe.db.commit()

	return {
		"attempt_id": attempt.name,
		"total_questions": attempt.total_questions,
		"correct_answers": attempt.correct_answers,
		"score_percentage": attempt.score_percentage,
		"passed": attempt.passed,
		"pass_mark": frappe.get_single("Driving School Settings").pass_mark
	}


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_results(attempt_id):
	"""Get exam results with detailed answers"""
	attempt = frappe.get_doc("Exam Attempt", attempt_id)

	if attempt.status != "Completed":
		frappe.throw(_("Exam is not completed yet"))

	settings = frappe.get_single("Driving School Settings")

	# Get detailed answers with question info
	detailed_answers = []
	for answer in attempt.answers:
		question = frappe.get_doc("Driving School Question", answer.question)
		detailed_answers.append({
			"question": answer.question,
			"question_text": question.question_text,
			"question_image": question.question_image,
			"options_are_images": question.options_are_images,
			"option_1": question.option_1,
			"option_1_image": question.option_1_image,
			"option_1_label": question.option_1_label,
			"option_2": question.option_2,
			"option_2_image": question.option_2_image,
			"option_2_label": question.option_2_label,
			"option_3": question.option_3,
			"option_3_image": question.option_3_image,
			"option_3_label": question.option_3_label,
			"selected_answer": answer.selected_answer,
			"correct_answer": answer.correct_answer,
			"is_correct": answer.is_correct
		})

	student = frappe.get_doc("Driving School Student", attempt.student)

	return {
		"attempt_id": attempt.name,
		"student_name": student.full_name,
		"student_id_number": student.id_number,
		"exam_name": attempt.exam,
		"start_time": attempt.start_time,
		"end_time": attempt.end_time,
		"total_questions": attempt.total_questions,
		"correct_answers": attempt.correct_answers,
		"score_percentage": attempt.score_percentage,
		"passed": attempt.passed,
		"pass_mark": settings.pass_mark,
		"school_name": settings.school_name,
		"answers": detailed_answers
	}


@frappe.whitelist(allow_guest=True)
def get_student_history(student_id):
	"""Get all exam attempts for a student"""
	attempts = frappe.get_all(
		"Exam Attempt",
		filters={
			"student": student_id,
			"status": "Completed"
		},
		fields=[
			"name", "exam", "start_time", "end_time",
			"total_questions", "correct_answers",
			"score_percentage", "passed"
		],
		order_by="creation desc"
	)

	settings = frappe.get_single("Driving School Settings")

	for attempt in attempts:
		attempt["pass_mark"] = settings.pass_mark

	return attempts
