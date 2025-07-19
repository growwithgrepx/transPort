from extensions import db

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
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))  # Link to service
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
    
    # Billing fields
    base_price = db.Column(db.Float, default=0.0)
    base_discount_percent = db.Column(db.Float, default=0.0)
    agent_discount_percent = db.Column(db.Float, default=0.0)
    additional_discount_percent = db.Column(db.Float, default=0.0)
    additional_charges = db.Column(db.Float, default=0.0)
    final_price = db.Column(db.Float, default=0.0)
    invoice_number = db.Column(db.String(128))
    
    # Relationships
    service = db.relationship('Service', backref='jobs')
    billing = db.relationship('Billing', backref='job', uselist=False, cascade='all, delete-orphan') 

    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'customer_email': self.customer_email,
            'customer_mobile': self.customer_mobile,
            'customer_reference': self.customer_reference,
            'passenger_name': self.passenger_name,
            'passenger_email': self.passenger_email,
            'passenger_mobile': self.passenger_mobile,
            'type_of_service': self.type_of_service,
            'service_id': self.service_id,
            'pickup_date': self.pickup_date,
            'pickup_time': self.pickup_time,
            'pickup_location': self.pickup_location,
            'dropoff_location': self.dropoff_location,
            'vehicle_type': self.vehicle_type,
            'vehicle_number': self.vehicle_number,
            'driver_contact': self.driver_contact,
            'payment_mode': self.payment_mode,
            'payment_status': self.payment_status,
            'order_status': self.order_status,
            'message': self.message,
            'remarks': self.remarks,
            'has_additional_stop': self.has_additional_stop,
            'additional_stops': self.additional_stops,
            'has_request': self.has_request,
            'reference': self.reference,
            'status': self.status,
            'date': self.date,
            'driver_id': self.driver_id,
            'agent_id': self.agent_id,
            'base_price': self.base_price,
            'base_discount_percent': self.base_discount_percent,
            'agent_discount_percent': self.agent_discount_percent,
            'additional_discount_percent': self.additional_discount_percent,
            'additional_charges': self.additional_charges,
            'final_price': self.final_price,
            'invoice_number': self.invoice_number
        } 