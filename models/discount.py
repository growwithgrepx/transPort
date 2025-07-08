from extensions import db

class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64))
    percent = db.Column(db.Float)
    billings = db.relationship('Billing', backref='discount', lazy=True) 