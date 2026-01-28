import frappe
import stripe
from frappe import _

@frappe.whitelist()
def create_stripe_checkout(listing_id):

    doc = frappe.get_doc("Car Listing", listing_id)
    if doc.payment_state == "PAID":
        frappe.throw(_("This listing has already been paid for."))
    amount = 5.00 if doc.type == "Featured" else 2.00
    stripe.api_key = frappe.conf.get("STRIPE_SECRET_KEY")
    try:
        payment = frappe.get_doc({
            "doctype": "Listing Payment",
            "seller": doc.seller,
            "listing_id": listing_id,
            "payment_for": doc.type,
            "amount": amount,
            "currency": "usd",
            "payment_method": "Stripe",
            "status": "Pending"
        }).insert(ignore_permissions=True)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            success_url=f"{frappe.conf.get('Redirect_to_Vue')}/payment-success?payment_id={payment.name}&listing_id={doc.name}",
            client_reference_id=payment.name,
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(payment.amount * 100),
                    "product_data": {
                        "name": payment.payment_for,
                    }
                },
                "quantity": 1
            }]
        )
        payment.transition_id = session.id
        payment.save(ignore_permissions=True)
        return {"checkout_url": session.url}
    except Exception as e:
        frappe.log_error("Payment failed", e)



@frappe.whitelist(allow_guest=True)
def stripe_webhook():
    payload = frappe.request.get_data()
    sig_header = frappe.request.headers.get('Stripe-Signature')
    webhook_secret = frappe.conf.get("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError as e:
        frappe.log_error("Invalid payload", e)
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        frappe.log_error("Invalid signature", e)
        return "Invalid signature", 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        handle_successful_payment(session)

    return {"status": 200}

def handle_successful_payment(session):
    try:
        payment_name = session.get("client_reference_id")
        if not payment_name:
            return

        payment = frappe.get_doc("Listing Payment", payment_name)

        if payment.status == "Paid":
            return
        frappe.set_user("Administrator")
        payment.status = "Paid"
        payment.save(ignore_permissions=True)

        listing = frappe.get_doc("Car Listing", payment.listing_id) 
        listing.payment_state = "PAID" 
        listing.save(ignore_permissions=True)
        frappe.db.commit() 
        listing.reload()
        from car_market.car_market.api.seller import submit_for_approval
        submit_for_approval(listing.name)
        
    except Exception as e:
        frappe.log_error("Stripe Webhook Error", frappe.get_traceback())

    finally:
        frappe.set_user("Guest")
