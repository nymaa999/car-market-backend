# Copyright (c) 2025, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CarListing(Document):


	def validate(self):
		if self.is_new() and not getattr(self, "main_image", None):
			frappe.throw(_("Main image is required for a new listing"))

		if self.price <= 0:
			frappe.throw(_("Price must be a positive value"))
		
		current_year = frappe.utils.now_datetime().year
		if self.produced_year > current_year + 1 or self.produced_year < 1900:
			frappe.throw(_("Please enter a valid year for the car"))
		
		
		# Make gallery optional - comment out if you want to require it
		if not self.gallery or len(self.gallery) == 0:
			frappe.throw(_("Car gallery must contain at least one image"))
		if self.workflow_state == "Rejected" and not self.rejected_reason:
			frappe.throw(
				msg="Зар татгалзаж байгаа бол заавал 'Rejected Reason' талбарт шалтгааныг бичнэ үү.",
				title="Шалтгаан шаардлагатай"
			)
	
	def before_insert(self):
		self.avg_rating = 0.0
		self.review_count = 0

		if not self.docstatus:
			self.docstatus = 0  
		
		if not self.seller:
			self.seller = frappe.session.user
			seller_id = frappe.db.get_value("Car Seller", {"user": self.seller}, "name")
			if not seller_id:
				frappe.throw(_("Current user is not registered as a Seller"))
			self.seller = seller_id

	def before_delete(self):
		current_user = frappe.session.user
		user_roles = frappe.get_roles(current_user)

		if "Marketplace Admin" in user_roles or "Administrator" in user_roles:
			return
		
		frappe.throw(_("Та энэ бичлэгийг шууд устгах эрхгүй байна. 'Request Cancel' товчийг ашиглана уу."), frappe.PermissionError)
		
		frappe.throw(_("You don't have permission to delete this record.", frappe.PermissionError))
	def before_update(self):
		# Workflow update бол зөвшөөрнө
		if frappe.flags.in_workflow:
			return

		current_user = frappe.session.user
		user_roles = frappe.get_roles(current_user)

		if "Marketplace Admin" in user_roles or "Administrator" in user_roles:
			return

		if "Car Seller" in user_roles:
			if self.owner == current_user:
				return
			else:
				frappe.throw(_("You can only update your own listings"), frappe.PermissionError)

		frappe.throw(_("You don't have permission to update this record."), frappe.PermissionError)

	def on_update(self):
		if self.workflow_state in ["Approved", "Rejected"]:
			answer = ""
			message = ""
			if self.workflow_state == "Approved":
				answer = f"Таны {self.listing_title} зар батлагдлаа!"
			else:
				answer = f"Таны {self.listing_title} зар татгалзлаа!"
				message = f"Татгалзсан шалтгаан: {self.rejected_reason}"
			notification = frappe.get_doc({
				"doctype": "Car Listing Notification",
				"for_user": self.owner,
				"for_listing": self.name,
				"type": self.workflow_state,
				"subject": answer,
				"message": message,
				"read": 0 
			})

			notification.insert(ignore_permissions=True)
			target_event = f"car_listing_{self.workflow_state.lower()}_{self.owner}"
			frappe.publish_realtime(
				target_event,
				message={
					"name": self.name,
					"for_user": self.owner,
					"for_listing": self.name,
					"type": notification.type,
					"read": notification.read,
					"subject": notification.subject,
					"message": notification.message
				}
			)

# def get_permission_query_conditions(user):
#     if not user:
#         user = frappe.session.user

#     # Хэрэв Admin бол бүх машиныг харна
#     roles = frappe.get_roles(user)
#     if "System Manager" in roles or "Administrator" in roles or "Marketplace Admin" in roles:
#         return ""

#     # Хэрэв Seller бол зөвхөн өөрийнхөө үүсгэсэн (owner) машиныг харна
#     if "Car Seller" in roles:
#         return f"`tabCar Listing`.owner = {frappe.db.escape(user)}"

#     return ""