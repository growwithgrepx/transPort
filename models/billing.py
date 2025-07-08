from extensions import db

class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    amount = db.Column(db.Float)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id')) 