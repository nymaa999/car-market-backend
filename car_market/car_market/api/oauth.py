import frappe
from frappe import _
from frappe.utils.password import check_password
import frappe.utils
from oauthlib.oauth2.rfc6749.tokens import random_token_generator 

def generate_token(client_id, user_id, scopes=None):
    access_token = random_token_generator(None)
    refresh_token = random_token_generator(None)
    expires_in = 3600  
    # expiration_time = frappe.utils.add_to_date(frappe.utils.now_datetime(), seconds=expires_in)

    token_doc = frappe.new_doc("OAuth Bearer Token")
    token_doc.update({
        "client": client_id,
        "user": user_id,
        "scopes": "\n".join(scopes or []), 
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "status": "Active"
    })
    token_doc.insert(ignore_permissions=True)
    frappe.db.commit() 

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": expires_in,
        "token_type": "Bearer"
    }

@frappe.whitelist(allow_guest=True)
def login(email=None, password=None):
    if not email or not password:
        frappe.throw(_("Email and password are required"))

    if not frappe.db.exists("User", email):
        frappe.throw(_("Invalid email or password"))

    try:
        check_password(email, password)
    except frappe.AuthenticationError:
        frappe.throw(_("Invalid email or password"))

    try:
        client = frappe.get_doc("OAuth Client", {"app_name": "Car Market"}) 
    except frappe.DoesNotExistError:
        frappe.throw(_("OAuth Client 'Car Market' not found. Check setup."))

    scopes = client.scopes.split('\n') if client.scopes else []
    token_data = generate_token(client.name, email, scopes) 

    return {
        "status": "success",
        "user": email,
        "access_token": token_data.get("access_token"),
        "refresh_token": token_data.get("refresh_token"),
        "expires_in": token_data.get("expires_in"),
        "token_type": "Bearer"
    }

def get_token_from_header():
    auth_header = frappe.get_request_header("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "").strip()
    return None

@frappe.whitelist()
def get_user_info():
    
    user_email = frappe.session.user
    try:
        user = frappe.get_doc("User", user_email)
        roles = frappe.get_roles(user_email)

        role = roles[0]

        token_name = frappe.db.get_value("OAuth Bearer Token", {"user": user_email}, "scopes")
        scopes = None
        if token_name:
            scopes = token_name
        return {
            "valid": True,
            "user": user_email,
            "email": user.email,
            "full_name": user.full_name,
            "user_image": user.user_image,
            "role": role,
            "scopes": scopes  
        }
    except Exception as e:
        frappe.log_error(title="Get User Info Error", message=str(e))
        frappe.throw(f"Failed to get user info: {str(e)}")

@frappe.whitelist(allow_guest=True)
def refresh(refresh_token=None):
    if not refresh_token:
        frappe.throw("Refresh token is required")

    try:
        token_name = frappe.db.get_value("OAuth Bearer Token", {"refresh_token": refresh_token}, "name")

        if not token_name:
            frappe.throw("Invalid refresh token")

        current_status = frappe.db.get_value("OAuth Bearer Token", token_name, "status")

        if current_status != "Active":
            frappe.throw("Token is not active")

        token_doc = frappe.get_doc("OAuth Bearer Token", token_name)
        frappe.db.set_value("OAuth Bearer Token", token_name, "status", "Revoked")

        scopes = token_doc.scopes.split('\n') if token_doc.scopes else []
        new_token_data = generate_token(token_doc.client, token_doc.user, scopes)

        frappe.db.commit()

        return {
            "status": "success",
            # "access_token": new_token_data.get("access_token"),
            # "refresh_token": new_token_data.get("refresh_token"),
            # "expires_in": new_token_data.get("expires_in"),
            # "token_type": "Bearer"
        }

    except frappe.DoesNotExistError:
        frappe.throw("Invalid refresh token")
    except Exception as e:
        frappe.log_error(title="Token Refresh Error", message=frappe.get_traceback())
        frappe.throw(f"Token refresh failed: {str(e)}")
