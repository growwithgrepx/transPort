import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import app
from extensions import db
from models import User, Role, Vehicle, Driver, Agent, Service, Job, Billing, Discount, Price, CustomerDiscount
from sqlalchemy import text
from flask_security.core import UserMixin  # Fixed import: import UserMixin from flask_security.core

def get_or_create(model, defaults=None, **kwargs):
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        db.session.add(instance)
        db.session.commit()
        return instance

# Properly create Flask app context using the factory pattern
from app import app, user_datastore

with app.app_context():
    # Wipe all data in the correct order to avoid FK issues
    db.session.query(Billing).delete()
    db.session.query(Job).delete()
    db.session.query(CustomerDiscount).delete()
    db.session.query(Price).delete()
    db.session.query(Service).delete()
    db.session.query(Agent).delete()
    db.session.query(Driver).delete()
    db.session.query(Vehicle).delete()
    db.session.query(Discount).delete()
    db.session.execute(text('DELETE FROM roles_users'))  # Association table, use raw SQL
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.commit()

    # Create roles using get_or_create to avoid self-dependency issues
    fleet_manager_role = get_or_create(Role, name='fleet_manager', defaults={'description': 'Fleet Manager'})
    system_admin_role = get_or_create(Role, name='system_admin', defaults={'description': 'System Administrator'})
    fleet_employee_role = get_or_create(Role, name='fleet_employee', defaults={'description': 'Fleet Company Employee'})
    accountant_role = get_or_create(Role, name='accountant', defaults={'description': 'Accountant'})
    customer_service_role = get_or_create(Role, name='customer_service', defaults={'description': 'Customer Service'})

    # Create users with Flask-Security's user_datastore (it handles password hashing automatically)
    fleet_manager = user_datastore.create_user(
        username='fleetmanager',
        email='fleetmanager@example.com',
        password='manager123',
        active=True,
        roles=[fleet_manager_role]
    )
    system_admin = user_datastore.create_user(
        username='sysadmin',
        email='sysadmin@example.com',
        password='sysadmin123',
        active=True,
        roles=[system_admin_role]
    )
    fleet_employee = user_datastore.create_user(
        username='employee1',
        email='employee1@example.com',
        password='employee123',
        active=True,
        roles=[fleet_employee_role]
    )
    accountant = user_datastore.create_user(
        username='accountant1',
        email='accountant1@example.com',
        password='accountant123',
        active=True,
        roles=[accountant_role]
    )
    customer_service = user_datastore.create_user(
        username='custservice1',
        email='custservice1@example.com',
        password='custservice123',
        active=True,
        roles=[customer_service_role]
    )
    db.session.commit()

    # Vehicles
    vehicle1 = get_or_create(Vehicle, number='SGX1234A', defaults={'name': 'Toyota Hiace', 'type': '13-Seater', 'status': 'Active'})
    vehicle2 = get_or_create(Vehicle, number='SGX5678B', defaults={'name': 'Mercedes Sprinter', 'type': '23-Seater', 'status': 'Active'})

    # Drivers
    driver1 = get_or_create(Driver, name='John Doe', defaults={'phone': '91234567'})
    driver2 = get_or_create(Driver, name='Jane Smith', defaults={'phone': '98765432'})

    # Agents
    agent1 = get_or_create(Agent, name='Alpha Agency', defaults={'email': 'alpha@agency.com', 'mobile': '90001111', 'type': 'Corporate', 'status': 'Active'})
    agent2 = get_or_create(Agent, name='Beta Agency', defaults={'email': 'beta@agency.com', 'mobile': '90002222', 'type': 'Travel', 'status': 'Active'})

    # Services
    service1 = get_or_create(Service, name='Airport Transfer', defaults={'description': 'Transfer to/from airport', 'status': 'Active'})
    service2 = get_or_create(Service, name='Corporate Charter', defaults={'description': 'Corporate transport', 'status': 'Active'})

    # Prices for services
    price1 = get_or_create(Price, service_id=service1.id, defaults={'amount': 50.0, 'currency': 'SGD'})
    price2 = get_or_create(Price, service_id=service2.id, defaults={'amount': 80.0, 'currency': 'SGD'})

    # Discounts
    discount1 = get_or_create(Discount, code='WELCOME10', defaults={'percent': 10})
    discount2 = get_or_create(Discount, code='CORP5', defaults={'percent': 5})

    # CustomerDiscounts for agents
    customer_discount1 = get_or_create(CustomerDiscount, customer_id=agent1.id, discount_id=discount1.id, defaults={'valid_from': None, 'valid_to': None})
    customer_discount2 = get_or_create(CustomerDiscount, customer_id=agent2.id, discount_id=discount2.id, defaults={'valid_from': None, 'valid_to': None})

    # Jobs
    job1 = get_or_create(Job, customer_reference='REF001', defaults={
        'customer_name': 'Alice', 'customer_email': 'alice@example.com', 'customer_mobile': '81234567',
        'passenger_name': 'Alice', 'passenger_email': 'alice@example.com', 'passenger_mobile': '81234567',
        'type_of_service': service1.name, 'pickup_date': '2024-07-08', 'pickup_time': '10:00',
        'pickup_location': 'Changi Airport', 'dropoff_location': 'Orchard Hotel',
        'vehicle_type': vehicle1.type, 'vehicle_number': vehicle1.number, 'driver_contact': driver1.name,
        'driver_id': driver1.id, 'agent_id': agent1.id, 'payment_mode': 'Cash', 'payment_status': 'Paid',
        'order_status': 'Completed', 'message': 'N/A', 'remarks': 'VIP', 'has_additional_stop': False,
        'has_request': False, 'reference': 'REF001', 'status': 'Completed', 'date': '2024-07-08'
    })
    job2 = get_or_create(Job, customer_reference='REF002', defaults={
        'customer_name': 'Bob', 'customer_email': 'bob@example.com', 'customer_mobile': '82345678',
        'passenger_name': 'Bob', 'passenger_email': 'bob@example.com', 'passenger_mobile': '82345678',
        'type_of_service': service2.name, 'pickup_date': '2024-07-09', 'pickup_time': '14:00',
        'pickup_location': 'Raffles Place', 'dropoff_location': 'Changi Airport',
        'vehicle_type': vehicle2.type, 'vehicle_number': vehicle2.number, 'driver_contact': driver2.name,
        'driver_id': driver2.id, 'agent_id': agent2.id, 'payment_mode': 'Card', 'payment_status': 'Unpaid',
        'order_status': 'New', 'message': 'N/A', 'remarks': '', 'has_additional_stop': False,
        'has_request': False, 'reference': 'REF002', 'status': 'New', 'date': '2024-07-09'
    })

    # Billings
    billing1 = get_or_create(Billing, job_id=job1.id, defaults={'amount': 100.0, 'discount_id': discount1.id})
    billing2 = get_or_create(Billing, job_id=job2.id, defaults={'amount': 200.0, 'discount_id': discount2.id})

    print('Sample data inserted successfully.')

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'change-this-salt-in-production')
    SECURITY_USER_IDENTITY_ATTRIBUTES = [
        {"username": {"mapper": "username", "case_insensitive": True}},
        {"email": {"mapper": "email", "case_insensitive": True}},
    ]