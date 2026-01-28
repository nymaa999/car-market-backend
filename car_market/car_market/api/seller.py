import frappe
from car_market.car_market.api.cars import  linked_doc_helper
from frappe.model.workflow import apply_workflow
from frappe.utils.translations import _

@frappe.whitelist(allow_guest=True)
def submit_for_approval(listing_id):
    doc = frappe.get_doc("Car Listing", listing_id)
    # if doc.owner != frappe.session.user:
    #     frappe.throw(_("Permission denied"), frappe.PermissionError)
    if doc.workflow_state != "Draft":
        frappe.throw(_("Only draft listings can be submitted for approval."))
    if doc.payment_state != "PAID":
        frappe.throw(_("Only paid listings can be submitted for approval."))
    doc.save(ignore_permissions=True)
    apply_workflow(doc, "Submit for Approval")
    frappe.db.commit()

    return doc.workflow_state

@frappe.whitelist()
def cancel_request_for_admin(listing_id):
    try:
        doc = frappe.get_doc("Car Listing", listing_id)
        if doc.owner != frappe.session.user:
            frappe.throw(_("Permission denied"), frappe.PermissionError)
        if doc.workflow_state != "Approved":
            frappe.throw(_("Only approved listings can be canceled."))
        doc.save(ignore_permissions=True)
        apply_workflow(doc, "Request Removal")
        frappe.db.commit()
        return doc.workflow_state
    except:
        frappe.log_error(_("Cancel Request for Admin Error"),frappe.get_traceback())
        return

@frappe.whitelist()
def resubmit_for_approval(listing_id, data):
    print("god damn it!!", data)
    doc = frappe.get_doc("Car Listing", listing_id)
    if doc.owner != frappe.session.user:
        frappe.throw(_("Permission denied"), frappe.PermissionError)
    try:
        if isinstance(data, str):
            data = frappe.parse_json(data)
        for f in ("produced_year", "entered_year", "mileage"):
            if f in data:
                data[f] = int(data[f])
        if "price" in data:
            data["price"] = float(data["price"])
        if "gallery" in data:
            doc.set("gallery", data.pop("gallery"))
        
        if doc.workflow_state == "Approved" or doc.docstatus == 1:
            doc.db_set("workflow_state", "Draft")
            doc.db_set("docstatus", 0)
            doc.update(data)
            doc.save(ignore_permissions=True)
            apply_workflow(doc, "Submit for Approval")

        if doc.workflow_state == "Rejected":
            doc.update(data)
            apply_workflow(doc, "Resubmit")
            doc.save(ignore_permissions=True)
            frappe.db.commit()
        return doc.workflow_state

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Resubmit for Approval Error"))
        frappe.throw(_("An internal error occurred: {0}").format(str(e)))

@frappe.whitelist()
def get_my_listings(workflow_state=None, listing_id=None):
    print("!!!", listing_id)
    user_email = frappe.session.user
    seller_id = frappe.db.get_value("Seller", {"user": user_email}, "name")
    filters = {"docstatus": ["!=", 2], "seller": seller_id}
    if workflow_state:
        filters["workflow_state"] = workflow_state
    if listing_id:
        filters["name"] = listing_id
    try:
        response = []

        listings = frappe.get_all(
            "Car Listing",
            fields=[
                "name",
                "listing_title",
                "produced_year",
                "entered_year",
                "mileage",
                "main_image",
                "description",
                "condition",
                "avg_rating",
                "price",
                "creation",
                "color",
                "rejected_reason",
                "type"
            ],
            filters=filters,
            order_by="creation desc"
        )

        for listing in listings:
            data = {}   

            linked_data = linked_doc_helper(listing)  

            # Listing fields
            data.update({
                "name": listing.name,
                "title": listing.listing_title,
                "produced_year": listing.produced_year,
                "entered_year": listing.entered_year,
                "mileage": listing.mileage,
                "main_image": listing.main_image,
                "description": listing.description,
                "avg_rating": listing.avg_rating,
                "price": listing.price,
                "created_date": listing.creation,
                "color": listing.color,
                "rejected_reason": listing.rejected_reason,
                "brand_name": linked_data['brand_name'],
                "model_name": linked_data['model_name'],
                "seller_info": linked_data['seller_info'],
                "condition": linked_data['condition'],
                "gallery": linked_data['gallery'],
                "type": listing.type
            })
            response.append(data)
        # rejected = count_rejected_listings(seller_id)

        return response

    except Exception as e:
        frappe.log_error(f"Error in get_listings: {str(e)}")
        return []
@frappe.whitelist()
def count_rejected_listings():
    try:
        seller_id = frappe.db.get_value("Seller", {"user": frappe.session.user}, "name")
        return frappe.db.count("Car Listing", {"docstatus": ["!=", 2], "seller": seller_id, "workflow_state": "Rejected"})
    except Exception as e:
        frappe.log_error(f"Error in count_rejected_listings: {str(e)}")
        return 0

@frappe.whitelist()
def get_notifications():
    # print("!!!",frappe.session.user)
    try:
        notifications = frappe.get_all(
            "Car Listing Notification",
            fields=["name", "for_user", "for_listing", "subject", "creation", "read", "type", "message"],
            filters={
                "for_user": frappe.session.user,
                "type": ["in", ["Approved", "Rejected", "Price Offer", "Offer Response"]] 
            },
            order_by="creation desc"
        )
        return {"notifications": notifications}
    except Exception as e:
        frappe.log_error(f"Error in get_notifications: {str(e)}")
        return {"notifications": []}

@frappe.whitelist()
def mark_notification_as_read(notification_id):
    try:
        frappe.db.set_value("Car Listing Notification", {"name": notification_id}, "read", 1)
        return {"status": "success"}
    except Exception as e:
        frappe.log_error(f"Error in mark_notification_as_read: {str(e)}")
        return {"status": "error"}
    
@frappe.whitelist()
def get_price_offers(listing_id):
    try:
        user_email = frappe.session.user
        seller_id = frappe.db.get_value("Seller", {"user": user_email}, "name")

        price_offers = frappe.get_all(
            "Price Offers",
            fields=["name", "buyer", "price_offer", "status"],
            filters={"seller": seller_id, "listing": listing_id}
        )

        return {"price_offers": price_offers}
    except Exception as e:
        frappe.log_error(f"Error in get_price_offers: {str(e)}")
        return {"price_offers": []}

@frappe.whitelist()
def approve_price_offer(offer_id, status):
    print("!!!", offer_id, status)
    try:
        if offer_id is None or status not in ["Accepted", "Rejected"]:
            frappe.throw(_("Invalid parameters"))

        price_offer = frappe.get_doc("Price Offers", offer_id)
        if not price_offer:
            frappe.throw(_("Price Offer not found"))

        price_offer.status = status
        price_offer.save(ignore_permissions=True)
        print("@@@@@@@", price_offer.status, price_offer.listing)
        return {"status": "success"}
    except Exception as e:
        frappe.log_error(f"Error in approve_price_offer: {str(e)}")
        return {"status": "error"}
