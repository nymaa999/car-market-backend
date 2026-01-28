# Copyright (c) 2026, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils.data import flt



class PriceOffers(Document):

	def validate(self):
		car = frappe.get_doc("Car Listing", self.listing)        
		if car.owner == self.buyer:
			frappe.throw(_("Та өөрийнхөө заранд үнийн санал өгөх боломжгүй."))

		if flt(self.price_offer) <= 0:
			frappe.throw(_("Үнийн санал 0-ээс их байх ёстой."))
		if flt(self.price_offer) >= flt(car.price):
			frappe.throw(_("Санал болгож буй үнэ үндсэн үнээс бага байх ёстой."))

		if not self.is_new():
			self.check_permission_on_status_change(car)

		
	def after_insert(self):
		car = frappe.get_doc("Car Listing", self.listing)
		notification = frappe.get_doc({
			"doctype": "Car Listing Notification",
			"for_user": car.owner,
			"for_listing": self.listing,
			"type": "Price Offer",
			"subject": f"Худалдан авагчийн санал: {car.listing_title}",
			"message": f"{self.buyer} худалдан авагч таны заранд {self.price_offer}₮-ийн санал тавилаа."
		})
		notification.insert(ignore_permissions=True)
		target_event = f"new_price_offer_{car.owner}"
		print("!!!", target_event)
		frappe.publish_realtime(target_event, {
			"offer_id": self.name,
			"for_user": car.owner,
			"for_listing": self.listing,
			"buyer": self.buyer,
			"price": self.price_offer,
			"type": notification.type,
			"read": notification.read,
			"subject": notification.subject,
			"message": notification.message
		})
	
	def check_permission_on_status_change(self, car):
		if self.has_value_changed("status"):
			if frappe.session.user != car.owner:
				frappe.throw(_("Зөвхөн зарын эзэн саналыг зөвшөөрөх эсвэл татгалзах эрхтэй."))

	def on_update(self):
		listing_title = frappe.get_value("Car Listing", {"name": self.listing}, "listing_title")
		if self.status in ["Accepted", "Rejected"]:
			answer = ""
			if self.status == "Accepted":
				answer = f"Таны {listing_title}-д гаргасан санал зөвшөөрөгдлөө!"
			else:
				answer = f"Таны {listing_title}-д гаргасан санал татгалзлаа!"
			notification = frappe.get_doc({
				"doctype": "Car Listing Notification",
				"for_user": self.owner,
				"for_listing": self.listing,
				"type": "Offer Response",
				"subject": answer,
				"message": answer,
				"read": 0
			})
			notification.insert(ignore_permissions=True)
			target_event = f"price_offer_response_{self.owner}"
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