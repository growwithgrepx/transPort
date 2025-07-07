from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(32), default='Active')


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    number = db.Column(db.String(64), unique=True, nullable=False)
    type = db.Column(db.String(64))
    status = db.Column(db.String(32), default='Active')


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(128))
    customer_email = db.Column(db.String(128))
    customer_mobile = db.Column(db.String(32))
    customer_reference = db.Column(db.String(128))
    passenger_name = db.Column(db.String(128))
    passenger_email = db.Column(db.String(128))
    passenger_mobile = db.Column(db.String(32))
    type_of_service = db.Column(db.String(128))
    pickup_date = db.Column(db.String(32))
    pickup_time = db.Column(db.String(32))
    pickup_location = db.Column(db.String(256))
    dropoff_location = db.Column(db.String(256))
    vehicle_type = db.Column(db.String(64))
    vehicle_number = db.Column(db.String(64))
    driver_contact = db.Column(db.String(128))
    payment_mode = db.Column(db.String(64))
    payment_status = db.Column(db.String(64))
    order_status = db.Column(db.String(64))
    message = db.Column(db.Text)
    remarks = db.Column(db.Text)
    has_additional_stop = db.Column(db.Boolean, default=False)
    additional_stops = db.Column(db.Text)
    has_request = db.Column(db.Boolean, default=False)
    reference = db.Column(db.String(128))
    status = db.Column(db.String(32), default='Inactive')
    date = db.Column(db.String(64))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'))


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    phone = db.Column(db.String(64))
    jobs = db.relationship('Job', backref='driver', lazy=True)


class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(32))
    type = db.Column(db.String(64))
    status = db.Column(db.String(32), default='Active')
    jobs = db.relationship('Job', backref='agent', lazy=True)


class Billing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    amount = db.Column(db.Float)
    discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'))


class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64))
    percent = db.Column(db.Float)
    billings = db.relationship('Billing', backref='discount', lazy=True)
