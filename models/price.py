from extensions import db

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(8), default='SGD')

    service = db.relationship('Service', backref=db.backref('prices', lazy=True)) 