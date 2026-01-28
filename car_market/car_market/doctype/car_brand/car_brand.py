# Copyright (c) 2025, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class CarBrand(Document):
	pass

@frappe.whitelist()
def create_car_brand(brand_name, country=None):
    if frappe.db.exists("Car Brand", brand_name):
        return frappe.get_doc("Car Brand", brand_name).name

    try:
        brand_doc = frappe.get_doc({
            "doctype": "Car Brand",
            "brand_name": brand_name, 
            "country": country 
        })
        
        brand_doc.insert(ignore_permissions=True) 
        frappe.db.commit()

        return brand_doc.name 
        
    except Exception as e:
        frappe.log_error(title="Car Brand Creation Error", message=str(e))
        frappe.throw(_("Failed to create Car Brand: {0}").format(str(e)))