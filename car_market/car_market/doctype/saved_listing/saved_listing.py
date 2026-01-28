import frappe
from frappe import _
from frappe.model.document import Document

class SavedListing(Document):
    def validate(self):
        
        if self.is_new():
            exists = frappe.db.exists("Saved Listing", {
                "user": frappe.session.user,
                "car_listing": self.car_listing
            })
            if exists:
                frappe.throw(_("Энэ зарыг аль хэдийн хадгалсан байна."))

    def before_delete(self):
        """
        Устгах эрхийг энд шалгана.
        """
        user_email = frappe.session.user
        roles = frappe.get_roles(user_email)

        if "System Manager" in roles or "Administrator" in roles:
            return

        if "Car Buyer" in roles:
            if self.owner == user_email:
                return
            else:
                frappe.throw(_("Та зөвхөн өөрийн хадгалсан зарыг устгах боломжтой."), frappe.PermissionError)
        
        frappe.throw(_("Танд энэ үйлдлийг хийх эрх байхгүй."), frappe.PermissionError)