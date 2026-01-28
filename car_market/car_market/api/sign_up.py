import frappe
from frappe.utils.password import update_password
from frappe import _


@frappe.whitelist(allow_guest=True)
def sign_up():
    try:
        data = frappe.local.form_dict  
        parts = data.name.strip().split()
        first_name = parts[0]
        last_name = " ".join(parts[1:])
        
        email = data.get('email')
        password = data.get('password')
        first_name = first_name
        last_name = last_name
        phone = data.get('phone', '')
        role = data.get('role', 'buyer')  
        bio = data.get('bio', '')
        location = data.get('location', '')
        if not email or not password or not first_name:
            frappe.throw(_("Email, Password and First Name are required"))
        
        if frappe.db.exists("User", email):
            frappe.throw(_("User with this email already exists"))
        
        if len(password) < 8:
            frappe.throw(_("Password must be at least 8 characters"))
        
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "enabled": 1,
            "send_welcome_email": 0,
            "user_type": "Website User"
        })
        
        if role == "buyer":
            user.append("roles", {
                "role": "Car Buyer"
            })
        elif role == "seller":
            user.append("roles", {
                "role": "Car Seller"
            })
        
        user.insert(ignore_permissions=True)
        update_password(user.name, password)
        
        if role == "buyer":
            buyer = frappe.get_doc({
                "doctype": "Buyer",
                "user": email,  
                "phone": phone
            })
            buyer.insert(ignore_permissions=True)
            
        elif role == "seller":
            seller = frappe.get_doc({
                "doctype": "Seller",
                "user": email,  
                "full_name": f"{first_name} {last_name}".strip(),
                "phone": phone,
                "bio": bio,
                "location": location
            })
            seller.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Account created successfully! Please sign in.",
            "data": {
                "email": email,
                "role": role
            }
        }
        
    except frappe.exceptions.ValidationError as e:
        frappe.db.rollback()
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist(allow_guest=True)
def check_email_exists(email):
    exists = frappe.db.exists("User", email)
    return {
        "exists": bool(exists)
    }