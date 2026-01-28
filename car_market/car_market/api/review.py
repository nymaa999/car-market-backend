import frappe
from frappe import _ 

@frappe.whitelist()
def submit_review(review_data):
    try:
        if frappe.session.user == "Guest":
            frappe.throw(_("Сэтгэгдэл бичихийн тулд нэвтэрнэ үү"), frappe.PermissionError)
        review_data = frappe._dict(frappe.parse_json(review_data))

        review = frappe.get_doc({
            "doctype": "Car Review",
            "user": frappe.session.user,
            "comment": review_data.get("comment"),
            "rating": review_data.get("rating"),
            "listing": review_data.get("listing_id")
        })

        if review_data.get("images"):
            images_list = frappe.parse_json(review_data.get("images"))  
            for image in images_list:
                review.append("rev_img", {
                    "image": image
                })
        review.insert(ignore_permissions=True)
        return {"message": _("Таны сэтгэгдэл амжилттай илгээгдлээ")}
    except:
        frappe.log_error( _("Submit Review Error"), frappe.get_traceback())  

@frappe.whitelist(allow_guest=True)
def get_reviews(listing_id):
    names = frappe.get_all(
        "Car Review",
        filters = {"listing": listing_id},
        pluck = "name"
    )
    reviews = []
    for name in names:
        doc = frappe.get_doc("Car Review", name)
        user = frappe.db.get_value("User", doc.user, ["full_name"], as_dict=True)
        reviews.append({
            "id": doc.name,
            "user": user.full_name,
            "comment": doc.comment,
            "rating": doc.rating,
            "creation": doc.creation,
            "images": [{"image": img.image, "caption": img.caption} for img in doc.rev_img]
        })
    reviews = sorted(reviews, key=lambda x: x['creation'], reverse=True)

    return {"reviews": reviews}