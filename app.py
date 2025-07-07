from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import json
from datetime import datetime

app = Flask(__name__)

# Configuration for production deployment
if os.environ.get('DATABASE_URL'):
    # Production database (PostgreSQL on Heroku)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace('postgres://', 'postgresql://')
else:
    # Development database (SQLite)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transport.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

db.init_app(app)

with app.app_context():
    from models import User, Job, Driver, Agent, Billing, Discount, Service, Vehicle

    if not os.path.exists('database.db'):
        db.create_all()


    # Create default admin user if not exists
    def create_default_admin():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()


    create_default_admin()


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            new_password = request.form['new_password']
            user.set_password(new_password)
            db.session.commit()
            flash('Password reset successful. Please login.')
            return redirect(url_for('login'))
        else:
            flash('Email not found.')
    return render_template('reset_password.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


# JOBS CRUD
@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # Advanced search fields
    search_fields = [
        'customer_name', 'customer_email', 'customer_mobile', 'customer_reference',
        'passenger_name', 'passenger_email', 'passenger_mobile', 'type_of_service',
        'pickup_date', 'pickup_time', 'pickup_location', 'dropoff_location',
        'vehicle_type', 'vehicle_number', 'driver_contact', 'payment_mode',
        'payment_status', 'order_status', 'message', 'remarks', 'reference', 'status'
    ]
    filters = []
    advanced = False
    for field in search_fields:
        value = request.args.get(field)
        if value:
            advanced = True
            filters.append(getattr(Job, field).ilike(f'%{value}%'))
    search_query = request.args.get('search', '')
    if advanced:
        jobs = Job.query.filter(*filters).all()
    elif search_query:
        jobs = Job.query.filter(
            (Job.customer_name.ilike(f'%{search_query}%')) |
            (Job.customer_email.ilike(f'%{search_query}%')) |
            (Job.customer_mobile.ilike(f'%{search_query}%')) |
            (Job.customer_reference.ilike(f'%{search_query}%')) |
            (Job.passenger_name.ilike(f'%{search_query}%')) |
            (Job.passenger_email.ilike(f'%{search_query}%')) |
            (Job.passenger_mobile.ilike(f'%{search_query}%')) |
            (Job.type_of_service.ilike(f'%{search_query}%')) |
            (Job.pickup_date.ilike(f'%{search_query}%')) |
            (Job.pickup_time.ilike(f'%{search_query}%')) |
            (Job.pickup_location.ilike(f'%{search_query}%')) |
            (Job.dropoff_location.ilike(f'%{search_query}%')) |
            (Job.vehicle_type.ilike(f'%{search_query}%')) |
            (Job.vehicle_number.ilike(f'%{search_query}%')) |
            (Job.driver_contact.ilike(f'%{search_query}%')) |
            (Job.payment_mode.ilike(f'%{search_query}%')) |
            (Job.payment_status.ilike(f'%{search_query}%')) |
            (Job.order_status.ilike(f'%{search_query}%')) |
            (Job.message.ilike(f'%{search_query}%')) |
            (Job.remarks.ilike(f'%{search_query}%')) |
            (Job.reference.ilike(f'%{search_query}%')) |
            (Job.status.ilike(f'%{search_query}%'))
        ).all()
    else:
        jobs = Job.query.all()
    return render_template('jobs.html', jobs=jobs, search_query=search_query)


@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    from models import Agent, Service, Vehicle, Driver
    agents = Agent.query.filter_by(status='Active').all()
    services = Service.query.filter_by(status='Active').all()
    vehicles = Vehicle.query.filter_by(status='Active').all()
    drivers = Driver.query.all()
    if request.method == 'POST':
        agent_id = request.form.get('agent_id')
        agent = Agent.query.get(agent_id) if agent_id else None
        service_id = request.form.get('service_id')
        service = Service.query.get(service_id) if service_id else None
        vehicle_id = request.form.get('vehicle_id')
        vehicle = Vehicle.query.get(vehicle_id) if vehicle_id else None
        driver_id = request.form.get('driver_id')
        driver = Driver.query.get(driver_id) if driver_id else None
        stops = request.form.getlist('additional_stops[]')
        job = Job(
            customer_name=agent.name if agent else request.form.get('customer_name'),
            customer_email=agent.email if agent else request.form.get('customer_email'),
            customer_mobile=agent.mobile if agent else request.form.get('customer_mobile'),
            agent_id=agent.id if agent else None,
            type_of_service=service.name if service else request.form.get('type_of_service'),
            vehicle_type=vehicle.type if vehicle else request.form.get('vehicle_type'),
            vehicle_number=vehicle.number if vehicle else request.form.get('vehicle_number'),
            driver_contact=driver.name if driver else request.form.get('driver_contact'),
            driver_id=driver.id if driver else None,
            customer_reference=request.form.get('customer_reference'),
            passenger_name=request.form.get('passenger_name'),
            passenger_email=request.form.get('passenger_email'),
            passenger_mobile=request.form.get('passenger_mobile'),
            pickup_date=request.form.get('pickup_date'),
            pickup_time=request.form.get('pickup_time'),
            pickup_location=request.form.get('pickup_location'),
            dropoff_location=request.form.get('dropoff_location'),
            payment_mode=request.form.get('payment_mode'),
            payment_status=request.form.get('payment_status'),
            order_status=request.form.get('order_status'),
            message=request.form.get('message'),
            remarks=request.form.get('remarks'),
            has_additional_stop=bool(request.form.get('has_additional_stop')),
            additional_stops=json.dumps(stops) if stops else None,
            has_request=bool(request.form.get('has_request')),
            reference=request.form.get('reference'),
            status=request.form.get('status'),
            date=request.form.get('pickup_date')
        )
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs'))
    return render_template('job_form.html', action='Add', job=None, agents=agents, services=services, vehicles=vehicles, drivers=drivers, stops=[])


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    from models import Agent, Service, Vehicle, Driver
    agents = Agent.query.filter_by(status='Active').all()
    services = Service.query.filter_by(status='Active').all()
    vehicles = Vehicle.query.filter_by(status='Active').all()
    drivers = Driver.query.all()
    job = Job.query.get_or_404(job_id)
    stops = json.loads(job.additional_stops) if job.additional_stops else []
    if request.method == 'POST':
        agent_id = request.form.get('agent_id')
        agent = Agent.query.get(agent_id) if agent_id else None
        service_id = request.form.get('service_id')
        service = Service.query.get(service_id) if service_id else None
        vehicle_id = request.form.get('vehicle_id')
        vehicle = Vehicle.query.get(vehicle_id) if vehicle_id else None
        driver_id = request.form.get('driver_id')
        driver = Driver.query.get(driver_id) if driver_id else None
        stops = request.form.getlist('additional_stops[]')
        job.customer_name = agent.name if agent else request.form.get('customer_name')
        job.customer_email = agent.email if agent else request.form.get('customer_email')
        job.customer_mobile = agent.mobile if agent else request.form.get('customer_mobile')
        job.agent_id = agent.id if agent else None
        job.type_of_service = service.name if service else request.form.get('type_of_service')
        job.vehicle_type = vehicle.type if vehicle else request.form.get('vehicle_type')
        job.vehicle_number = vehicle.number if vehicle else request.form.get('vehicle_number')
        job.driver_contact = driver.name if driver else request.form.get('driver_contact')
        job.driver_id = driver.id if driver else None
        job.customer_reference = request.form.get('customer_reference')
        job.passenger_name = request.form.get('passenger_name')
        job.passenger_email = request.form.get('passenger_email')
        job.passenger_mobile = request.form.get('passenger_mobile')
        job.pickup_date = request.form.get('pickup_date')
        job.pickup_time = request.form.get('pickup_time')
        job.pickup_location = request.form.get('pickup_location')
        job.dropoff_location = request.form.get('dropoff_location')
        job.payment_mode = request.form.get('payment_mode')
        job.payment_status = request.form.get('payment_status')
        job.order_status = request.form.get('order_status')
        job.message = request.form.get('message')
        job.remarks = request.form.get('remarks')
        job.has_additional_stop = bool(request.form.get('has_additional_stop'))
        job.additional_stops = json.dumps(stops) if stops else None
        job.has_request = bool(request.form.get('has_request'))
        job.reference = request.form.get('reference')
        job.status = request.form.get('status')
        job.date = request.form.get('pickup_date')
        db.session.commit()
        return redirect(url_for('jobs'))
    return render_template('job_form.html', action='Edit', job=job, agents=agents, services=services, vehicles=vehicles, drivers=drivers, stops=stops)


@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('jobs'))


@app.route('/jobs/smart_add', methods=['GET', 'POST'])
def smart_add_job():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    parsed_data = None
    if request.method == 'POST':
        message = request.form.get('message')
        parsed_data = parse_job_message(message)
        return render_template('job_form.html', action='Add', job=parsed_data, smart_add=True, pasted_message=message)
    return render_template('smart_add.html')


def parse_job_message(message):
    # Try to parse as field: value pairs
    data = {}
    lines = message.splitlines()
    for line in lines:
        if ':' in line:
            field, value = line.split(':', 1)
            field = field.strip().lower().replace(' ', '_')
            value = value.strip()
            # Map common aliases to job fields
            field_map = {
                'agent': 'customer_name',
                'agent_email': 'customer_email',
                'agent_mobile': 'customer_mobile',
                'service': 'type_of_service',
                'vehicle': 'vehicle_type',
                'vehicle_number': 'vehicle_number',
                'pickup': 'pickup_location',
                'drop': 'dropoff_location',
                'date': 'pickup_date',
                'time': 'pickup_time',
                'status': 'status',
                'passenger': 'passenger_name',
                'passenger_email': 'passenger_email',
                'passenger_mobile': 'passenger_mobile',
                'reference': 'reference',
                'remarks': 'remarks',
                'message': 'message',
            }
            mapped_field = field_map.get(field, field)
            data[mapped_field] = value
    # Fallback to regex for common fields if not found
    if not data:
        patterns = {
            'customer_name': r'Customer[:\-]?\s*([\w\s]+)',
            'customer_email': r'Email[:\-]?\s*([\w\.-]+@[\w\.-]+)',
            'customer_mobile': r'Mobile[:\-]?\s*(\d+)',
            'type_of_service': r'Service[:\-]?\s*([\w\s]+)',
            'pickup_date': r'Date[:\-]?\s*([\d\-/]+)',
            'pickup_time': r'Time[:\-]?\s*([\d:apmAPM\s]+)',
            'pickup_location': r'Pickup[:\-]?\s*([\w\s]+)',
            'dropoff_location': r'Drop[:\-]?\s*([\w\s]+)',
            'vehicle_type': r'Vehicle[:\-]?\s*([\w\s]+)',
            'driver_contact': r'Driver[:\-]?\s*([\w\s]+)',
            'payment_status': r'Payment[:\-]?\s*([\w\s]+)',
            'order_status': r'Status[:\-]?\s*([\w\s]+)',
        }
        for field, pattern in patterns.items():
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                data[field] = match.group(1).strip()
    return data


# DRIVERS CRUD
@app.route('/drivers')
def drivers():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name', '')
    phone = request.args.get('phone', '')
    query = Driver.query
    if name:
        query = query.filter(Driver.name.ilike(f'%{name}%'))
    if phone:
        query = query.filter(Driver.phone.ilike(f'%{phone}%'))
    drivers = query.all()
    return render_template('drivers.html', drivers=drivers)


@app.route('/drivers/add', methods=['GET', 'POST'])
def add_driver():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        driver = Driver(name=name, phone=phone)
        db.session.add(driver)
        db.session.commit()
        return redirect(url_for('drivers'))
    return render_template('driver_form.html', action='Add')


@app.route('/drivers/edit/<int:driver_id>', methods=['GET', 'POST'])
def edit_driver(driver_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    driver = Driver.query.get_or_404(driver_id)
    if request.method == 'POST':
        driver.name = request.form['name']
        driver.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('drivers'))
    return render_template('driver_form.html', action='Edit', driver=driver)


@app.route('/drivers/delete/<int:driver_id>', methods=['POST'])
def delete_driver(driver_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('drivers'))


# AGENTS CRUD
@app.route('/agents')
def agents():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name', '')
    email = request.args.get('email', '')
    mobile = request.args.get('mobile', '')
    type_ = request.args.get('type', '')
    status = request.args.get('status', '')
    query = Agent.query
    if name:
        query = query.filter(Agent.name.ilike(f'%{name}%'))
    if email:
        query = query.filter(Agent.email.ilike(f'%{email}%'))
    if mobile:
        query = query.filter(Agent.mobile.ilike(f'%{mobile}%'))
    if type_:
        query = query.filter(Agent.type.ilike(f'%{type_}%'))
    if status:
        query = query.filter(Agent.status == status)
    agents = query.all()
    return render_template('agents.html', agents=agents)


@app.route('/agents/add', methods=['GET', 'POST'])
def add_agent():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        type_ = request.form['type']
        status = request.form['status']
        agent = Agent(name=name, email=email, mobile=mobile, type=type_, status=status)
        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('agents'))
    return render_template('agent_form.html', action='Add', agent=None)


@app.route('/agents/edit/<int:agent_id>', methods=['GET', 'POST'])
def edit_agent(agent_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    agent = Agent.query.get_or_404(agent_id)
    if request.method == 'POST':
        agent.name = request.form['name']
        agent.email = request.form['email']
        agent.mobile = request.form['mobile']
        agent.type = request.form['type']
        agent.status = request.form['status']
        db.session.commit()
        return redirect(url_for('agents'))
    return render_template('agent_form.html', action='Edit', agent=agent)


@app.route('/agents/delete/<int:agent_id>', methods=['POST'])
def delete_agent(agent_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('agents'))


# BILLING CRUD
@app.route('/billing')
def billing():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    billings = Billing.query.all()
    return render_template('billing.html', billings=billings)


@app.route('/billing/add', methods=['GET', 'POST'])
def add_billing():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        job_id = request.form['job_id']
        amount = request.form['amount']
        discount_id = request.form['discount_id']
        billing = Billing(job_id=job_id, amount=amount, discount_id=discount_id)
        db.session.add(billing)
        db.session.commit()
        return redirect(url_for('billing'))
    return render_template('billing_form.html', action='Add')


@app.route('/billing/edit/<int:billing_id>', methods=['GET', 'POST'])
def edit_billing(billing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    billing = Billing.query.get_or_404(billing_id)
    if request.method == 'POST':
        billing.job_id = request.form['job_id']
        billing.amount = request.form['amount']
        billing.discount_id = request.form['discount_id']
        db.session.commit()
        return redirect(url_for('billing'))
    return render_template('billing_form.html', action='Edit', billing=billing)


@app.route('/billing/delete/<int:billing_id>', methods=['POST'])
def delete_billing(billing_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    billing = Billing.query.get_or_404(billing_id)
    db.session.delete(billing)
    db.session.commit()
    return redirect(url_for('billing'))


# DISCOUNTS CRUD
@app.route('/discounts')
def discounts():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    discounts = Discount.query.all()
    return render_template('discounts.html', discounts=discounts)


@app.route('/discounts/add', methods=['GET', 'POST'])
def add_discount():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        code = request.form['code']
        percent = request.form['percent']
        discount = Discount(code=code, percent=percent)
        db.session.add(discount)
        db.session.commit()
        return redirect(url_for('discounts'))
    return render_template('discount_form.html', action='Add')


@app.route('/discounts/edit/<int:discount_id>', methods=['GET', 'POST'])
def edit_discount(discount_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    discount = Discount.query.get_or_404(discount_id)
    if request.method == 'POST':
        discount.code = request.form['code']
        discount.percent = request.form['percent']
        db.session.commit()
        return redirect(url_for('discounts'))
    return render_template('discount_form.html', action='Edit', discount=discount)


@app.route('/discounts/delete/<int:discount_id>', methods=['POST'])
def delete_discount(discount_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    discount = Discount.query.get_or_404(discount_id)
    db.session.delete(discount)
    db.session.commit()
    return redirect(url_for('discounts'))


# SERVICES CRUD
@app.route('/services')
def services():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name', '')
    status = request.args.get('status', '')
    query = Service.query
    if name:
        query = query.filter(Service.name.ilike(f'%{name}%'))
    if status:
        query = query.filter(Service.status == status)
    services = query.all()
    return render_template('services.html', services=services)


@app.route('/services/add', methods=['GET', 'POST'])
def add_service():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        status = request.form['status']
        service = Service(name=name, description=description, status=status)
        db.session.add(service)
        db.session.commit()
        return redirect(url_for('services'))
    return render_template('service_form.html', action='Add', service=None)


@app.route('/services/edit/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.status = request.form['status']
        db.session.commit()
        return redirect(url_for('services'))
    return render_template('service_form.html', action='Edit', service=service)


@app.route('/services/delete/<int:service_id>', methods=['POST'])
def delete_service(service_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('services'))


# VEHICLES CRUD
@app.route('/vehicles')
def vehicles():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    name = request.args.get('name', '')
    number = request.args.get('number', '')
    type_ = request.args.get('type', '')
    status = request.args.get('status', '')
    query = Vehicle.query
    if name:
        query = query.filter(Vehicle.name.ilike(f'%{name}%'))
    if number:
        query = query.filter(Vehicle.number.ilike(f'%{number}%'))
    if type_:
        query = query.filter(Vehicle.type.ilike(f'%{type_}%'))
    if status:
        query = query.filter(Vehicle.status == status)
    vehicles = query.all()
    return render_template('vehicles.html', vehicles=vehicles)


@app.route('/vehicles/add', methods=['GET', 'POST'])
def add_vehicle():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        type_ = request.form['type']
        status = request.form['status']
        vehicle = Vehicle(name=name, number=number, type=type_, status=status)
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))
    return render_template('vehicle_form.html', action='Add', vehicle=None)


@app.route('/vehicles/edit/<int:vehicle_id>', methods=['GET', 'POST'])
def edit_vehicle(vehicle_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == 'POST':
        vehicle.name = request.form['name']
        vehicle.number = request.form['number']
        vehicle.type = request.form['type']
        vehicle.status = request.form['status']
        db.session.commit()
        return redirect(url_for('vehicles'))
    return render_template('vehicle_form.html', action='Edit', vehicle=vehicle)


@app.route('/vehicles/delete/<int:vehicle_id>', methods=['POST'])
def delete_vehicle(vehicle_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('vehicles'))


@app.route('/api/quick_add/agent', methods=['POST'])
def api_quick_add_agent():
    data = request.json
    from models import Agent
    agent = Agent(
        name=data.get('name'),
        email=data.get('email'),
        mobile=data.get('mobile'),
        type=data.get('type'),
        status=data.get('status', 'Active')
    )
    db.session.add(agent)
    db.session.commit()
    return jsonify({
        'id': agent.id,
        'name': agent.name,
        'email': agent.email,
        'mobile': agent.mobile
    })

@app.route('/api/quick_add/service', methods=['POST'])
def api_quick_add_service():
    data = request.json
    from models import Service
    service = Service(
        name=data.get('name'),
        description=data.get('description'),
        status=data.get('status', 'Active')
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({
        'id': service.id,
        'name': service.name
    })

@app.route('/api/quick_add/vehicle', methods=['POST'])
def api_quick_add_vehicle():
    data = request.json
    from models import Vehicle
    vehicle = Vehicle(
        name=data.get('name'),
        number=data.get('number'),
        type=data.get('type'),
        status=data.get('status', 'Active')
    )
    db.session.add(vehicle)
    db.session.commit()
    return jsonify({
        'id': vehicle.id,
        'name': vehicle.name,
        'number': vehicle.number,
        'type': vehicle.type
    })

@app.route('/api/quick_add/driver', methods=['POST'])
def api_quick_add_driver():
    data = request.json
    from models import Driver
    driver = Driver(
        name=data.get('name'),
        phone=data.get('phone')
    )
    db.session.add(driver)
    db.session.commit()
    return jsonify({
        'id': driver.id,
        'name': driver.name,
        'phone': driver.phone
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

