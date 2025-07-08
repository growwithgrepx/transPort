from extensions import db

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64))
    status = db.Column(db.String(32), default='Active') 