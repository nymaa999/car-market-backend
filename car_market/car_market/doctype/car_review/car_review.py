# Copyright (c) 2025, Nyamdorj and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import flt
from frappe.query_builder.functions import Avg


class CarReview(Document):

    def on_update(self):
        self.update_listing_rating()

    def on_trash(self):
        self.update_listing_rating()

    def update_listing_rating(self):
        Review = frappe.qb.DocType("Car Review")
        
        query = (
            frappe.qb.from_(Review)
            .select(Avg(Review.rating))
            .where(Review.listing == self.listing)
        )
        
        result = query.run()
        
        avg_value = result[0][0] if result and result[0][0] else 0

        # Car Listing-ийн утгыг шинэчлэх
        frappe.db.set_value(
            "Car Listing", 
            self.listing, 
            "avg_rating", 
            flt(avg_value, 1)
        )
        frappe.publish_realtime(
            "listing_rate_updated",
            message={"listing_id": self.listing, "average_rating": flt(avg_value, 1)},
            after_commit=True
        )
