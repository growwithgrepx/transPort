from extensions import db
from datetime import datetime

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    invoice_number = db.Column(db.String(128), unique=True)
    invoice_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    
    # Pricing breakdown
    base_price = db.Column(db.Float, default=0.0)
    base_discount_amount = db.Column(db.Float, default=0.0)
    agent_discount_amount = db.Column(db.Float, default=0.0)
    additional_discount_amount = db.Column(db.Float, default=0.0)
    additional_charges = db.Column(db.Float, default=0.0)
    subtotal = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Payment information
    payment_status = db.Column(db.String(32), default='Pending')
    payment_date = db.Column(db.DateTime)
    payment_method = db.Column(db.String(64))
    
    # Discount references
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))
    
    # Additional fields
    notes = db.Column(db.Text)
    terms_conditions = db.Column(db.Text)
    
    def calculate_total(self):
        """Calculate the total amount including all discounts and charges"""
        self.subtotal = self.base_price - self.base_discount_amount - self.agent_discount_amount - self.additional_discount_amount
        self.total_amount = self.subtotal + self.additional_charges + self.tax_amount
        return self.total_amount 