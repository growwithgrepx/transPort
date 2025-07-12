from extensions import db


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    jobs = db.relationship('Job', backref='driver', lazy=True)
