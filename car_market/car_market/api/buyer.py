import frappe
from frappe import _ 
from car_market.car_market.api.cars import linked_doc_helper

@frappe.whitelist()
def save_listing(listing):
    
    user_email = frappe.session.user

    buyer_id = frappe.db.get_value("Buyer", {"user": user_email}, "name")
    if not buyer_id:
        frappe.throw("Buyer profile not found")

    buyer = frappe.get_doc("Buyer", buyer_id)
    for row in buyer.saved_listing:
        if row.listing == listing:
            return "already saved"
    buyer.append("saved_listing",{
        "listing": listing,
        "saved_on": frappe.utils.now_datetime()
    })

    buyer.save(ignore_permissions=True)
    frappe.db.commit()

    return "success"

@frappe.whitelist()
def get_saved_listings():
    user_email = frappe.session.user    
    buyer_id = frappe.db.get_value("Buyer", {"user": user_email}, "name")
    
    if not buyer_id:
        return []

    try:
        saved_rows = frappe.get_all(
            "Saved Listing",
            fields=["name", "listing", "saved_on"], 
            filters={
                "parent": buyer_id,
                "parenttype": "Buyer"
            },
            order_by="saved_on desc",
            ignore_permissions=True 
        )

        if not saved_rows:
            return []
        
        response = []
        for row in saved_rows:
            if not frappe.db.exists("Car Listing", row.listing):
                continue

            listing = frappe.get_doc("Car Listing", row.listing)
            linked_data = linked_doc_helper(listing)  
            
            response.append({
                "row_id": row.name, 
                "saved_on": row.saved_on,
                "name": listing.name,
                "title": listing.listing_title or listing.title,
                "produced_year": listing.produced_year,
                "entered_year": listing.entered_year,
                "mileage": listing.mileage,
                "main_image": listing.main_image if hasattr(listing, 'main_image') else listing.main_image,
                "description": listing.description,
                "avg_rating": listing.avg_rating,
                "price": listing.price,
                "color": listing.color,
                "created_date": listing.creation,
                "brand_name": linked_data.get('brand_name'),
                "model_name": linked_data.get('model_name'),
                "seller_info": linked_data.get('seller_info'),
                "condition": linked_data.get('condition'),
                "gallery": linked_data.get('gallery')
            })

        return response

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Saved Listings Error")
        return []
    
@frappe.whitelist()
def delete_saved_listing(id):
    try:
        parent_info = frappe.db.get_value("Saved Listing", id, ["parent", "parenttype"], as_dict=True)

        if not parent_info:
            frappe.throw("Record not fount")
        buyer_doc = frappe.get_doc(parent_info.parenttype, parent_info.parent)

        if buyer_doc.user != frappe.session.user:
            frappe.throw("Unauthorized", frappe.PermissionError)

        for row in buyer_doc.get("saved_listing"):
            if row.name == id:
                buyer_doc.remove(row)
                break
        
        buyer_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {"status": "success"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Delete Saved Listing Error")
        frappe.throw(_("Устгахад алдаа гарлаа: {0}").format(str(e)))

@frappe.whitelist()
def submit_price_offer(listing_id, price):
    try:
        if not listing_id or not price:
            frappe.throw(_("Listing ID and price are required"))

        listing = frappe.get_doc("Car Listing", listing_id)
        if not listing:
            frappe.throw(_("Car Listing not found"))

        price_offer = frappe.get_doc({
            "doctype": "Price Offers",
            "listing": listing_id,
            "seller": listing.seller,
            "buyer": frappe.session.user,
            "price_offer": int(price)
        })
        price_offer.insert(ignore_permissions=True)

        return {"status": "success"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Submit Price Offer Error")
