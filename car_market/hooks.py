app_name = "car_market"
app_title = "Car Market"
app_publisher = "Nyamdorj"
app_description = "This is car market app"
app_email = "dorjderemnymdorj81@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "car_market",
# 		"logo": "/assets/car_market/logo.png",
# 		"title": "Car Market",
# 		"route": "/car_market",
# 		"has_permission": "car_market.api.permission.has_app_permission"
# 	}
# ]

fixtures = [
    {"dt": "Car Brand"},
    {"dt": "Car Model"},
    {"dt": "Car Condition"},
    {"dt": "Seller Profile"},
]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/car_market/css/car_market.css"
# app_include_js = "/assets/car_market/js/car_market.js"

# include js, css files in header of web template
# web_include_css = "/assets/car_market/css/car_market.css"
# web_include_js = "/assets/car_market/js/car_market.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "car_market/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "car_market/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "car_market.utils.jinja_methods",
# 	"filters": "car_market.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "car_market.install.before_install"
# after_install = "car_market.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "car_market.uninstall.before_uninstall"
# after_uninstall = "car_market.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "car_market.utils.before_app_install"
# after_app_install = "car_market.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "car_market.utils.before_app_uninstall"
# after_app_uninstall = "car_market.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "car_market.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Car Listing": "car_market.car_market.doctype.car_listing.car_listing.get_permission_query_conditions"
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"Car Listing": {
# 		"on_update": "car_market.car_market.doctype.car_listing.car_listing.on_update",
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"car_market.tasks.all"
# 	],
# 	"daily": [
# 		"car_market.tasks.daily"
# 	],
# 	"hourly": [
# 		"car_market.tasks.hourly"
# 	],
# 	"weekly": [
# 		"car_market.tasks.weekly"
# 	],
# 	"monthly": [
# 		"car_market.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "car_market.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "car_market.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "car_market.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "car_market.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["car_market.utils.before_request"]
# after_request = ["car_market.utils.after_request"]

# Job Events
# ----------
# before_job = ["car_market.utils.before_job"]
# after_job = ["car_market.utils.after_job"]

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
# 	"car_market.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

