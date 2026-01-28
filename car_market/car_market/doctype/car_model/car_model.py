# Copyright (c) 2025, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CarModel(Document):
	pass

@frappe.whitelist()
def create_car_model(model_name, brand):
    # 1. 'brand_name' талбараар хайлт хийж, Car Brand-ийн 'name' ID-г олох
    brand_name_id = frappe.db.get_value("Car Brand", {"brand_name": brand}, "name")

    if not brand_name_id:
        # Хэрэв брэнд олохгүй бол алдаа үүсгэнэ
        frappe.throw(f"Car Brand '{brand}' not found.")
    
    # 2. Car Model үүсгэхдээ Link талбарт 'name' ID-г ашиглах
    model_doc = frappe.get_doc({
        "doctype": "Car Model",
        "model_name": model_name,
        "brand": brand_name_id # Энд p96pi3dcio гэх мэт ID орно
    })
    
    model_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return model_doc.name