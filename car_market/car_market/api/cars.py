import frappe
import json
from frappe import _

@frappe.whitelist()
def add_listing(**kwargs):
    data = kwargs
    print("Adding listing:", data)

    if isinstance(data, str):
        data = json.loads(data)
    user_email = frappe.session.user

    if "Car Seller" not in frappe.get_roles(user_email):
        frappe.throw(_("Permission denied"), frappe.PermissionError)

    if data.get("car_number") and frappe.db.exists(
        "Car Listing", {"car_number": data["car_number"]}
    ):
        frappe.throw(_("Car number already exists"))

    seller_id = frappe.db.get_value("Seller", {"user": user_email}, "name")
    if not seller_id:
        frappe.throw(_("Seller profile not found"))


    main_image = data.get("main_image")
    gallery = data.get("gallery", [])
    if isinstance(gallery, str):
        gallery = json.loads(gallery)
    
    if not gallery or len(gallery) == 0:
        gallery = [{"image": main_image, "caption": "Main Image"}] if main_image else []
    print("!!!", "main:", main_image, "gallery:", gallery)

    try:
        produced_year = int(data.get("produced_year", 0))
        entered_year = int(data.get("entered_year", 0))
        price = float(data.get("price", 0))
        mileage = int(data.get("mileage", 0)) if data.get("mileage") else 0
    except (ValueError, TypeError):
        frappe.throw(_("Invalid numeric values for year, price, or mileage"))

    car = frappe.get_doc({
        "doctype": "Car Listing",
        "listing_title": data.get("title"),
        "brand": data.get("brand"),
        "model": data.get("model"),
        "produced_year": produced_year,
        "entered_year": entered_year,
        "price": price,
        "condition": data.get("condition"),
        "mileage": mileage,
        "main_image": main_image,
        "description": data.get("description"),
        "seller": seller_id,
        "gallery": gallery,
        "color": data.get("color"),
        "type": data.get("type"),
    })

    car.insert(ignore_permissions=True)
    frappe.db.commit()

    return {
        "name": car.name,
    }



def get_or_create_brand(brand_name):

    """Get brand ID by name, or create if it doesn't exist"""
    if not brand_name:
        frappe.throw(_("Brand name is required"))
    
    brand_id = frappe.db.get_value(
        "Car Brand", 
        {"brand_name": ["like", f"%{brand_name}%"]}, 
        "name"
    )
    
    if brand_id:
        return brand_id
    
    brand = frappe.get_doc({
        "doctype": "Car Brand",
        "brand_name": brand_name,
        "country": "Unknown"  
    })
    brand.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return brand.name

def get_or_create_model(model_name, brand_id=None):

    """Get model ID by name and brand, or create if it doesn't exist"""
    if not model_name:
        frappe.throw(_("Model name is required"))
    
    if not brand_id:
        frappe.throw(_("Brand is required to create model"))
    
    model_id = frappe.db.get_value(
        "Car Model",
        {
            "model_name": ["like", f"%{model_name}%"],
        },
        "name"
    )
    
    if model_id:
        return model_id
    
    # Create new model if not found
    model = frappe.get_doc({
        "doctype": "Car Model",
        "model_name": model_name,
        "brand": brand_id
    })
    model.insert(ignore_permissions=True)
    frappe.db.commit()
    
    return model.name

def get_brand_id_by_name(brand_name):
    """Зөвхөн хайх зориулалттай, шинээр үүсгэхгүй"""
    if not brand_name:
        return None
    
    filters = {"brand_name": ["like", f"%{brand_name}%"]}

    return frappe.db.get_value("Car Brand", filters, "name")
def get_model_id_by_name(model_name):
    """Зөвхөн хайх зориулалттай, шинээр үүсгэхгүй"""
    if not model_name:
        return None
    
    filters = {"model_name": ["like", f"%{model_name}%"]}

    return frappe.db.get_value("Car Model", filters, "name")

@frappe.whitelist(allow_guest=True)
def get_listings(filters=None, start=0, page_length=20):
    """Get all car listings with brand and model names"""
    print("Filters received:", filters)
    try:
        if isinstance(filters, str):
            filters = frappe.parse_json(filters)
        db_filters = {"docstatus": ["!=", 2], "workflow_state": "Approved"}

        if filters:
            if filters.get("brand"): 
                db_filters["brand"] = filters.get("brand")
            if filters.get("model"): 
                db_filters["model"] = filters.get("model")
            if filters.get("condition"): 
                db_filters["condition"] = filters.get("condition")
            if filters.get("min_price") or filters.get("max_price"):
                min_p = filters.get("min_price") or 0
                max_p = filters.get("max_price") or 100000000
                db_filters["price"] = ["between", [min_p, max_p]]
            if filters.get("mileage"):
                db_filters["mileage"] = ["<=", filters.get("mileage")]
            if filters.get("produced_year"):
                db_filters["produced_year"] = ["<=", filters.get("produced_year")]
            if filters.get("entered_year"):
                db_filters["entered_year"] = ["<=", filters.get("entered_year")]
            if filters.get("type"):
                db_filters["type"] = filters.get("type")
        response = []
        order_by = "type, avg_rating desc, creation desc"
        listings = frappe.get_list(
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
                "owner", 
                "brand",
                "model",
                "seller",
                "color",
                "type"
            ],
            filters=db_filters,
            order_by=order_by,
            start=start,
            page_length=page_length
        )
        for listing in listings:
            data = {}   
            linked_data = linked_doc_helper(listing)

            data.update({
                "name": listing.name,
                "title": listing.listing_title,
                "produced_year": listing.produced_year,
                "entered_year": listing.entered_year,
                "mileage": listing.mileage,
                "main_image": listing.main_image,
                "description": listing.description,
                "condition": listing.condition,
                "avg_rating": listing.avg_rating,
                "price": listing.price,
                "created_date": listing.creation,
                "owner": listing.owner,
                "color": listing.color,
                "brand_name": linked_data['brand_name'],
                "model_name": linked_data['model_name'],
                "seller_info": linked_data['seller_info'],
                "condition": linked_data['condition'],
                "gallery": linked_data['gallery'],
                "type": listing.type
            })

            response.append(data)

        return response

    except Exception as e:
        frappe.log_error(f"Error in get_listings: {str(e)}")
        return []
    
@frappe.whitelist(allow_guest=True)
def get_avg_rate(listing_id):
    try:
        avg_rating = frappe.db.get_value("Car Listing", {"listing": listing_id}, "avg_rating")
        return {"average_rating": avg_rating}
    except Exception as e:
        frappe.log_error(f"Error in get_avg_rate: {str(e)}")
        return {"average_rating": 0}


@frappe.whitelist()
def delete_car(car_id):
    print("Deleting car:", car_id)
    if not car_id:
        frappe.throw(_("Car not found: {0}").format(car_id))

    frappe.delete_doc("Car Listing", car_id, ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": f"Car {car_id} deleted successfully"}



@frappe.whitelist(allow_guest=True)
def get_conditions():
    return frappe.get_all("Car Condition", 
        fields=["name", "condition"],
        order_by="condition asc"
    )
@frappe.whitelist(allow_guest=True)
def get_brands():
    return frappe.get_all("Car Brand",
                          fields=["name", "brand_name"],
                          order_by="brand_name asc"
                          )

@frappe.whitelist(allow_guest=True)
def get_models(brand=None):
    filters = {}
    if brand:
        filters["brand"] = brand
    return frappe.get_all("Car Model",
                          fields=["name", "model_name"],
                          filters=filters,
                          order_by="model_name asc"
                          )

def linked_doc_helper(listing):
    data = {}   
    # Brand
    data["brand_name"] = (
        frappe.db.get_value("Car Brand", listing.brand, "brand_name")
        if listing.get("brand") else "Unknown"
    ) or "Unknown"

    # Model
    data["model_name"] = (
        frappe.db.get_value("Car Model", listing.model, "model_name")
        if listing.get("model") else "Unknown"
    ) or "Unknown"

    # Seller info
    seller_info = {}
    if listing.get("seller"):
        try:
            seller_id = listing.seller
            seller = frappe.get_doc("Seller", seller_id)
            seller_info = {
                "full_name": seller.full_name,
                "phone": seller.phone,
                "location": seller.location
            }
        except Exception:
            pass

    data["seller_info"] = seller_info

    condition_label = None
    if listing.condition:
        condition_label = frappe.db.get_value(
            "Car Condition",
            listing.condition,
            "condition"
        )

    data["condition"] = condition_label
    data["gallery"] = frappe.get_all(
        "Car Image",
        fields=["image", "caption"],
        filters={
            "parent": listing.name,
            "parenttype": "Car Listing"
        },
        order_by="idx"
    )
    return data

@frappe.whitelist(allow_guest=True)
def filters(filters=None):
    if isinstance(filters, str):
        filters = frappe.parse_json(filters)

    db_filters = {"status": "Active"}
    
    if filters:
        if filters.get("brand"):
            db_filters["brand"] = filters.get("brand")
        if filters.get("model"):
            db_filters["model"] = filters.get("model")
        if filters.get("condition"):
            db_filters["condition"] = filters.get("condition")