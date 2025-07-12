from extensions import db

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(64))
    percent = db.Column(db.Float, nullable=False, default=0.0)
    amount = db.Column(db.Float, default=0.0)  # Fixed amount discount
    discount_type = db.Column(db.String(32), default='percentage')  # 'percentage' or 'fixed'
    is_base_discount = db.Column(db.Boolean, default=False)  # Base discount for all services
    is_active = db.Column(db.Boolean, default=True)
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)
    
    billings = db.relationship('Billing', backref='discount', lazy=True) 