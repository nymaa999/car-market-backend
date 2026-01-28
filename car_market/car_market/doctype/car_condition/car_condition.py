# Copyright (c) 2025, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CarCondition(Document):
	pass

@frappe.whitelist()
def create_car_condition(condition):
	if frappe.db.exists("Car Condition", condition):
		return frappe.get_doc("Car Condition", condition).name

	try:
		condition_doc = frappe.get_doc({
			"doctype": "Car Condition",
			"condition": condition, 
			
		})
		
		condition_doc.insert(ignore_permissions=True) 
		frappe.db.commit()

		return condition_doc.name 
		
	except Exception as e:
		frappe.log_error(title="Car Condition Creation Error", message=str(e))
		frappe.throw(_("Failed to create Car Condition: {0}").format(str(e)))
