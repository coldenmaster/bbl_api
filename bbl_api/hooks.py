from . import __version__ as app_version

app_name = "bbl_api"
app_title = "Bbl Api"
app_publisher = "BBL"
app_description = "Iot and other machine API"
app_email = "wangtao@hbbbl.top"
app_license = "MIT"

# from mqtt.mqtt_rt import bbl_mqtt_client
# bbl_mqtt_client.message_callback_add('testtopic/#', mqtt_testtopic_message)

# print("我是 bbl_api hooks")
# mqtt_register()

# Includes in <head>
# ------------------

sounds = [
	{"name": "email", "src": "/assets/frappe/sounds/email.mp3", "volume": 0.8},
	{"name": "submit", "src": "/assets/frappe/sounds/submit.mp3", "volume": 0.8},
	{"name": "cancel", "src": "/assets/frappe/sounds/cancel.mp3", "volume": 0.8},
	{"name": "delete", "src": "/assets/frappe/sounds/delete.mp3", "volume": 0.75},
	{"name": "click", "src": "/assets/frappe/sounds/click.mp3", "volume": 0.75},
	{"name": "error", "src": "/assets/frappe/sounds/error.mp3", "volume": 0.8},
	{"name": "alert", "src": "/assets/frappe/sounds/alert.mp3", "volume": 0.9},
	# {"name": "chime", "src": "/assets/frappe/sounds/chime.mp3"},
]


# include js, css files in header of desk.html
# app_include_css = "/assets/bbl_api/css/bbl_api.css"
# app_include_js = "/assets/bbl_api/js/bbl_api.js"

# include js, css files in header of web template
# web_include_css = "/assets/bbl_api/css/bbl_api.css"
# web_include_js = "/assets/bbl_api/js/bbl_api.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "bbl_api/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "bbl_api.utils.jinja_methods",
#	"filters": "bbl_api.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "bbl_api.install.before_install"
# after_install = "bbl_api.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "bbl_api.uninstall.before_uninstall"
# after_uninstall = "bbl_api.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "bbl_api.utils.before_app_install"
# after_app_install = "bbl_api.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "bbl_api.utils.before_app_uninstall"
# after_app_uninstall = "bbl_api.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "bbl_api.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    # commen_site_config.json 中配置（现在是600s）
	"all": [ 
		"bbl_api.tasks.all"
	],
	"daily": [
		"bbl_api.tasks.daily"
	],
	"hourly": [
		"bbl_api.tasks.hourly"
	],
	"weekly": [
		"bbl_api.tasks.weekly"
	],
	"monthly": [
		"bbl_api.tasks.monthly"
	],
 
    # "annual": [
    #     "bbl_api.tasks.annual"
    # ],
	"cron": {
		# "0/15 * * * *": [
		# 	"erpnext.manufacturing.doctype.bom_update_log.bom_update_log.resume_bom_cost_update_jobs",
		# 	"erpnext.accounts.doctype.process_payment_reconciliation.process_payment_reconciliation.trigger_reconciliation_for_queued_docs",
		# ],
		"0/30 * * * *": [
            "bbl_api.tasks.minute_per30"
		],
		# # Hourly but offset by 30 minutes
		"0/5 * * * *": [
            "bbl_api.tasks.minute_per5"
		],
		# # Daily but offset by 30 minutes
		"30 * * * *": [
            "bbl_api.tasks.minute_30"
		],
		# # Daily but offset by 30 minutes
		"10 1 * * *": [
            "bbl_api.tasks.daily_00_10m"
		],
  
	},
}

# Testing
# -------

# before_tests = "bbl_api.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "bbl_api.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "bbl_api.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["bbl_api.utils.before_request"]
# after_request = ["bbl_api.utils.after_request"]

# Job Events
# ----------
# before_job = ["bbl_api.utils.before_job"]
# after_job = ["bbl_api.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"bbl_api.auth.validate"
# ]
