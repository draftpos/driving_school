# Copyright (c) 2024, Frappe and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import os


@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_file(file_url):
	"""
	Serve private files for the driving school test portal.
	Only serves files that are attached to Driving School doctypes.
	"""
	if not file_url:
		frappe.throw(_("File URL is required"))

	# Security: Only allow serving files from private/files
	if not file_url.startswith("/private/files/"):
		frappe.throw(_("Invalid file path"))

	# Get the file name from the URL
	file_name = file_url.replace("/private/files/", "")

	# Check if this file is used in Driving School doctypes
	is_valid_file = False

	# Check if file is used in Driving School Settings (logo)
	settings = frappe.get_single("Driving School Settings")
	if settings.logo and file_name in settings.logo:
		is_valid_file = True

	# Check if file is used in Driving School Question
	if not is_valid_file:
		question_with_file = frappe.db.exists(
			"Driving School Question",
			{
				"question_image": ["like", f"%{file_name}%"]
			}
		)
		if question_with_file:
			is_valid_file = True

	# Check option images
	if not is_valid_file:
		for field in ["option_1_image", "option_2_image", "option_3_image"]:
			question_with_file = frappe.db.exists(
				"Driving School Question",
				{
					field: ["like", f"%{file_name}%"]
				}
			)
			if question_with_file:
				is_valid_file = True
				break

	if not is_valid_file:
		frappe.throw(_("File not found or access denied"), frappe.PermissionError)

	# Get the actual file path
	site_path = frappe.get_site_path()
	file_path = os.path.join(site_path, "private", "files", file_name)

	if not os.path.exists(file_path):
		frappe.throw(_("File not found"), frappe.DoesNotExistError)

	# Read and return the file
	with open(file_path, "rb") as f:
		file_content = f.read()

	# Determine content type
	import mimetypes
	content_type, _ = mimetypes.guess_type(file_name)
	if not content_type:
		content_type = "application/octet-stream"

	# Set response headers
	frappe.local.response.filename = file_name
	frappe.local.response.filecontent = file_content
	frappe.local.response.type = "binary"

	return
