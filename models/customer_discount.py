from extensions import db

class CustomerDiscount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)
    valid_from = db.Column(db.Date)
    valid_to = db.Column(db.Date)

    customer = db.relationship('Agent', backref=db.backref('discounts', lazy=True))
    discount = db.relationship('Discount', backref=db.backref('customer_discounts', lazy=True)) 