from extensions import db

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(32))
    type = db.Column(db.String(64))
    status = db.Column(db.String(32), default='Active')
    agent_discount_percent = db.Column(db.Float, default=0.0)  # Agent-specific discount percentage
    jobs = db.relationship('Job', backref='agent', lazy=True) 