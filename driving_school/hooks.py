app_name = "driving_school"
app_title = "Driving School"
app_publisher = "Frappe"
app_description = "Driving School Test Application"
app_email = "developers@frappe.io"
app_license = "MIT"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "driving_school",
# 		"logo": "/assets/driving_school/logo.png",
# 		"title": "Driving School",
# 		"route": "/driving_school",
# 		"has_permission": "driving_school.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/driving_school/css/driving_school.css"
# app_include_js = "/assets/driving_school/js/driving_school.js"

# include js, css files in header of web template
# web_include_css = "/assets/driving_school/css/driving_school.css"
# web_include_js = "/assets/driving_school/js/driving_school.js"

# include custom scss in every website theme (without signing in)
# website_theme_scss = "driving_school/public/scss/website"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "driving_school/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
role_home_page = {
	"Driving School Student": "/student-test"
}

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from path
# fixtures = ["Custom Field", "Custom Doctype"]

fixtures = [
	{
		"doctype": "Role",
		"filters": [["name", "in", ["Driving School Student"]]]
	},
	{
		"doctype": "Role Profile",
		"filters": [["name", "in", ["Driving School Student"]]]
	}
]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "driving_school.utils.jinja_methods",
# 	"filters": "driving_school.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "driving_school.install.before_install"
after_install = "driving_school.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "driving_school.uninstall.before_uninstall"
# after_uninstall = "driving_school.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "driving_school.utils.before_app_install"
# after_app_install = "driving_school.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "driving_school.utils.before_app_uninstall"
# after_app_uninstall = "driving_school.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "driving_school.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"driving_school.tasks.all"
# 	],
# 	"daily": [
# 		"driving_school.tasks.daily"
# 	],
# 	"hourly": [
# 		"driving_school.tasks.hourly"
# 	],
# 	"weekly": [
# 		"driving_school.tasks.weekly"
# 	],
# 	"monthly": [
# 		"driving_school.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "driving_school.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "driving_school.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "driving_school.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["driving_school.utils.before_request"]
# after_request = ["driving_school.utils.after_request"]

# Job Events
# ----------
# before_job = ["driving_school.utils.before_job"]
# after_job = ["driving_school.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"driving_school.auth.validate"
# ]

# Login hooks
on_login = "driving_school.api.auth.on_login"

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Website Route Rules - removed, using static file in public folder instead
# Access the test at: /assets/driving_school/driving-test/index.html

# Guest access for test taking
guest_allowed_doctypes = []
