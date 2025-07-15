from extensions import db

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='Active')
    base_price = db.Column(db.Float, nullable=False, default=0.0)  # Base price for the service 