from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify, make_response
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import json
from datetime import datetime
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, Email, Length, Optional
from math import ceil
from flask_admin import Admin, expose
from flask_admin.contrib.sqla import ModelView
from flask import abort
from flask_wtf.csrf import CSRFProtect, generate_csrf
from models import User
import logging
from logging.handlers import RotatingFileHandler
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
import traceback
from functools import wraps

app = Flask(__name__)

# Initialize Sentry for error tracking
sentry_dsn = os.environ.get('SENTRY_DSN')
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=1.0,
        environment=os.environ.get('FLASK_ENV', 'development')
    )

# Configure logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/transport_app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Transport Admin Portal startup')

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

app_env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config_map.get(app_env, DevelopmentConfig))

if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError('DATABASE_URL environment variable must be set to a valid PostgreSQL connection string.')

db.init_app(app)
csrf = CSRFProtect(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

migrate = Migrate(app, db)

with app.app_context():
    from models import User, Job, Driver, Agent, Billing, Discount, Service, Vehicle, Role

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(Form):
    username = StringField('Username or Email', validators=[
        DataRequired(message='Username or email is required'),
        Length(min=3, max=150, message='Username must be between 3 and 150 characters')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=3, max=255, message='Password must be between 3 and 255 characters')
    ])

# Input validation decorators
def validate_json_input(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            if request.is_json:
                data = request.get_json()
                if not data:
                    app.logger.warning(f'Empty JSON data received in {f.__name__}')
                    return jsonify({'error': 'No input data provided'}), 400
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f'JSON validation error in {f.__name__}: {str(e)}')
            return jsonify({'error': 'Invalid JSON data'}), 400
    return decorated_function

def validate_form_input(required_fields=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if required_fields and request.method == 'POST':
                for field in required_fields:
                    if not request.form.get(field):
                        app.logger.warning(f'Missing required field {field} in {f.__name__}')
                        flash(f'{field.replace("_", " ").title()} is required', 'error')
                        return redirect(request.url)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def handle_database_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Database error in {f.__name__}: {str(e)}')
            app.logger.error(traceback.format_exc())
            flash('An error occurred while processing your request. Please try again.', 'error')
            return redirect(url_for('dashboard'))
    return decorated_function

# Custom admin view to restrict access to admins only
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and any(role.name in ['fleet_manager', 'system_admin'] for role in current_user.roles)
    def inaccessible_callback(self, name, **kwargs):
        return abort(403)

# Initialize Flask-Admin
admin = Admin(app, name='Admin', template_mode='bootstrap4')

with app.app_context():
    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Role, db.session))
    admin.add_view(AdminModelView(Job, db.session))
    admin.add_view(AdminModelView(Driver, db.session))
    admin.add_view(AdminModelView(Agent, db.session))
    admin.add_view(AdminModelView(Vehicle, db.session))
    admin.add_view(AdminModelView(Billing, db.session))
    admin.add_view(AdminModelView(Discount, db.session))
    admin.add_view(AdminModelView(Service, db.session))

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    app.logger.error(f'Bad request: {error}')
    return render_template('errors/400.html'), 400

@app.errorhandler(403)
def forbidden(error):
    app.logger.error(f'Forbidden access: {error}')
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def not_found(error):
    app.logger.error(f'Page not found: {error}')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal server error: {error}')
    app.logger.error(traceback.format_exc())
    db.session.rollback()
    return render_template('errors/500.html'), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        app.logger.info(f'User {current_user.username} already authenticated, redirecting to dashboard')
        return redirect(url_for('dashboard'))
    
    form = LoginForm(request.form)
    error = None
    
    if request.method == 'POST':
        app.logger.info(f'Login attempt for user: {request.form.get("username", "unknown")}')
        
        if form.validate():
            username = form.username.data.strip()
            password = form.password.data
            
            # Input sanitization
            if not username or not password:
                error = 'Username and password are required'
                app.logger.warning('Empty username or password provided')
            else:
                try:
                    # Try to find user by username or email
                    user = User.query.filter(
                        (User.username == username) | (User.email == username)
                    ).first()
                    
                    if user and user.check_password(password):
                        if user.active:
                            login_user(user)
                            app.logger.info(f'User {user.username} logged in successfully')
                            flash('Login successful!', 'success')
                            next_page = request.args.get('next')
                            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
                        else:
                            error = 'Account is inactive. Please contact administrator.'
                            app.logger.warning(f'Inactive user {user.username} attempted to login')
                    else:
                        error = 'Invalid username or password'
                        app.logger.warning(f'Failed login attempt for user: {username}')
                        
                except Exception as e:
                    app.logger.error(f'Login error: {str(e)}')
                    error = 'An error occurred during login. Please try again.'
        else:
            error = 'Please correct the errors below'
            app.logger.warning(f'Form validation failed: {form.errors}')
    
    return render_template('login.html', form=form, error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    from models import Job, Vehicle, Driver
    from datetime import date
    # Unassigned Jobs: jobs with no driver or vehicle assigned
    unassigned_jobs = Job.query.filter((Job.driver_id == None) | (Job.vehicle_type == None)).count()
    # Ready to Invoice: jobs with order_status 'Completed' and not yet billed (assuming payment_status 'Unpaid')
    ready_to_invoice = Job.query.filter(Job.order_status == 'Completed', Job.payment_status == 'Unpaid').count()
    # Total Vehicles
    total_vehicles = Vehicle.query.count()
    # Available Drivers: drivers not assigned to any active job (assuming jobs with order_status 'New' or 'In Progress')
    active_driver_ids = [job.driver_id for job in Job.query.filter(Job.order_status.in_(['New', 'In Progress'])).all() if job.driver_id]
    available_drivers = Driver.query.filter(~Driver.id.in_(active_driver_ids)).count()
    # Active Jobs: jobs with order_status 'New' or 'In Progress'
    active_jobs = Job.query.filter(Job.order_status.in_(['New', 'In Progress'])).count()
    # Completed Today: jobs with order_status 'Completed' and pickup_date is today
    completed_today = Job.query.filter(Job.order_status == 'Completed', Job.pickup_date == date.today().isoformat()).count()
    return render_template('dashboard.html',
        unassigned_jobs=unassigned_jobs,
        ready_to_invoice=ready_to_invoice,
        total_vehicles=total_vehicles,
        available_drivers=available_drivers,
        active_jobs=active_jobs,
        completed_today=completed_today
    )


# JOBS CRUD
@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    page = request.args.get('page', 1, type=int)
    per_page = 20
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
        query = Job.query.filter(*filters)
    elif search_query:
        query = Job.query.filter(
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
        )
    else:
        query = Job.query
    pagination = query.order_by(Job.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    return render_template('jobs.html', jobs=jobs, search_query=search_query, pagination=pagination)

@app.route('/jobs/table', methods=['GET'])
@login_required
def jobs_table():
    page = request.args.get('page', 1, type=int)
    per_page = 20
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
        query = Job.query.filter(*filters)
    elif search_query:
        query = Job.query.filter(
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
        )
    else:
        query = Job.query
    pagination = query.order_by(Job.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    jobs = pagination.items
    return render_template('jobs_table.html', jobs=jobs, pagination=pagination)


@app.route('/jobs/add', methods=['GET', 'POST'])
@login_required
@handle_database_errors
@validate_form_input(['customer_name', 'pickup_date', 'pickup_location', 'dropoff_location'])
def add_job():
    from models import Agent, Service, Vehicle, Driver
    agents = Agent.query.filter_by(status='Active').all()
    services = Service.query.filter_by(status='Active').all()
    vehicles = Vehicle.query.filter_by(status='Active').all()
    drivers = Driver.query.all()
    if request.method == 'POST':
        try:
            # Validate and sanitize input
            agent_id = request.form.get('agent_id')
            agent = Agent.query.get(agent_id) if agent_id and agent_id.isdigit() else None
            
            service_id = request.form.get('service_id')
            service = Service.query.get(service_id) if service_id and service_id.isdigit() else None
            
            vehicle_id = request.form.get('vehicle_id')
            vehicle = Vehicle.query.get(vehicle_id) if vehicle_id and vehicle_id.isdigit() else None
            
            driver_id = request.form.get('driver_id')
            driver = Driver.query.get(driver_id) if driver_id and driver_id.isdigit() else None
            
            # Validate required fields
            customer_name = (agent.name if agent else request.form.get('customer_name', '').strip())
            pickup_location = request.form.get('pickup_location', '').strip()
            dropoff_location = request.form.get('dropoff_location', '').strip()
            pickup_date = request.form.get('pickup_date', '').strip()
            
            if not customer_name:
                flash('Customer name is required', 'error')
                return redirect(request.url)
            
            if not pickup_location:
                flash('Pickup location is required', 'error')
                return redirect(request.url)
            
            if not dropoff_location:
                flash('Dropoff location is required', 'error')
                return redirect(request.url)
            
            if not pickup_date:
                flash('Pickup date is required', 'error')
                return redirect(request.url)
            
            # Validate date format
            try:
                datetime.strptime(pickup_date, '%Y-%m-%d')
            except ValueError:
                flash('Invalid pickup date format', 'error')
                return redirect(request.url)
            
            # Validate email if provided
            customer_email = (agent.email if agent else request.form.get('customer_email', '').strip())
            if customer_email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', customer_email):
                flash('Invalid customer email format', 'error')
                return redirect(request.url)
            
            passenger_email = request.form.get('passenger_email', '').strip()
            if passenger_email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', passenger_email):
                flash('Invalid passenger email format', 'error')
                return redirect(request.url)
            
            # Validate mobile numbers
            customer_mobile = (agent.mobile if agent else request.form.get('customer_mobile', '').strip())
            if customer_mobile and not re.match(r'^[\d\s\-\+\(\)]+$', customer_mobile):
                flash('Invalid customer mobile number format', 'error')
                return redirect(request.url)
            
            passenger_mobile = request.form.get('passenger_mobile', '').strip()
            if passenger_mobile and not re.match(r'^[\d\s\-\+\(\)]+$', passenger_mobile):
                flash('Invalid passenger mobile number format', 'error')
                return redirect(request.url)
            
            stops = request.form.getlist('additional_stops[]')
            
            job = Job(
                customer_name=customer_name,
                customer_email=customer_email,
                customer_mobile=customer_mobile,
                agent_id=agent.id if agent else None,
                type_of_service=service.name if service else request.form.get('type_of_service', '').strip(),
                vehicle_type=vehicle.type if vehicle else request.form.get('vehicle_type', '').strip(),
                vehicle_number=vehicle.number if vehicle else request.form.get('vehicle_number', '').strip(),
                driver_contact=driver.name if driver else request.form.get('driver_contact', '').strip(),
                driver_id=driver.id if driver else None,
                customer_reference=request.form.get('customer_reference', '').strip(),
                passenger_name=request.form.get('passenger_name', '').strip(),
                passenger_email=passenger_email,
                passenger_mobile=passenger_mobile,
                pickup_date=pickup_date,
                pickup_time=request.form.get('pickup_time', '').strip(),
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                payment_mode=request.form.get('payment_mode', '').strip(),
                payment_status=request.form.get('payment_status', '').strip(),
                order_status=request.form.get('order_status', '').strip(),
                message=request.form.get('message', '').strip(),
                remarks=request.form.get('remarks', '').strip(),
                has_additional_stop=bool(request.form.get('has_additional_stop')),
                additional_stops=json.dumps(stops) if stops else None,
                has_request=bool(request.form.get('has_request')),
                reference=request.form.get('reference', '').strip(),
                status=request.form.get('status', '').strip(),
                date=pickup_date
            )
            
            db.session.add(job)
            db.session.commit()
            
            app.logger.info(f'Job created successfully by user {current_user.username}: {job.id}')
            flash('Job created successfully', 'success')
            return redirect(url_for('jobs'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating job: {str(e)}')
            flash('Error creating job. Please try again.', 'error')
            return redirect(request.url)
    return render_template('job_form.html', action='Add', job=None, agents=agents, services=services, vehicles=vehicles, drivers=drivers, stops=[])


@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
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
@login_required
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('jobs'))


@app.route('/jobs/smart_add', methods=['GET', 'POST'])
@login_required
def smart_add_job():
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
@login_required
def drivers():
    name = request.args.get('name', '')
    phone = request.args.get('phone', '')
    query = Driver.query
    if name:
        query = query.filter(Driver.name.ilike(f'%{name}%'))
    if phone:
        query = query.filter(Driver.phone.ilike(f'%{phone}%'))
    drivers = query.all()
    if request.headers.get('HX-Request') == 'true':
        return render_template('drivers_table.html', drivers=drivers)
    return render_template('drivers.html', drivers=drivers)


@app.route('/drivers/add', methods=['GET', 'POST'])
@login_required
def add_driver():
    errors = {}
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        driver = Driver(name=name, phone=phone)
        db.session.add(driver)
        db.session.commit()
        if request.headers.get('HX-Request') == 'true':
            drivers = Driver.query.all()
            response = make_response(render_template('drivers_table.html', drivers=drivers))
            response.headers['HX-Trigger'] = 'closeModal'
            return response
        return redirect(url_for('drivers'))
    return render_template('driver_form.html', action='Add', driver=None, errors=errors,
        action_url=url_for('add_driver'), hx_post_url=url_for('add_driver'), hx_target='#drivers-table', hx_swap='outerHTML')


@app.route('/drivers/edit/<int:driver_id>', methods=['GET', 'POST'])
@login_required
def edit_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    errors = {}
    if request.method == 'POST':
        driver.name = request.form['name']
        driver.phone = request.form['phone']
        db.session.commit()
        return redirect(url_for('drivers'))
    if request.headers.get('HX-Request') == 'true':
        return render_template('driver_form.html', action='Edit', driver=driver, errors=errors,
            action_url=url_for('edit_driver', driver_id=driver.id), hx_post_url=url_for('edit_driver', driver_id=driver.id), hx_target='#drivers-table', hx_swap='outerHTML')
    return render_template('edit_driver_page.html', action='Edit', driver=driver, errors=errors,
        action_url=url_for('edit_driver', driver_id=driver.id), hx_post_url=None, hx_target=None, hx_swap=None)


@app.route('/drivers/delete/<int:driver_id>', methods=['POST'])
@login_required
def delete_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)
    db.session.delete(driver)
    db.session.commit()
    return redirect(url_for('drivers'))


# AGENTS CRUD
@app.route('/agents')
@login_required
def agents():
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
    if request.headers.get('HX-Request') == 'true':
        return render_template('agents_table.html', agents=agents)
    return render_template('agents.html', agents=agents)


@app.route('/agents/add', methods=['GET', 'POST'])
@login_required
def add_agent():
    errors = {}
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        type_ = request.form['type']
        status = request.form['status']
        agent = Agent(name=name, email=email, mobile=mobile, type=type_, status=status)
        db.session.add(agent)
        db.session.commit()
        if request.headers.get('HX-Request') == 'true':
            agents = Agent.query.all()
            response = make_response(render_template('agents_table.html', agents=agents))
            response.headers['HX-Trigger'] = 'closeModal'
            return response
        return redirect(url_for('agents'))
    return render_template('agent_form.html', action='Add', agent=None, errors=errors,
        action_url=url_for('add_agent'), hx_post_url=url_for('add_agent'), hx_target='#agents-table', hx_swap='outerHTML')


@app.route('/agents/edit/<int:agent_id>', methods=['GET', 'POST'])
@login_required
def edit_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    errors = {}
    if request.method == 'POST':
        agent.name = request.form['name']
        agent.email = request.form['email']
        agent.mobile = request.form['mobile']
        agent.type = request.form['type']
        agent.status = request.form['status']
        db.session.commit()
        return redirect(url_for('agents'))
    if request.headers.get('HX-Request') == 'true':
        return render_template('agent_form.html', action='Edit', agent=agent, errors=errors,
            action_url=url_for('edit_agent', agent_id=agent.id), hx_post_url=url_for('edit_agent', agent_id=agent.id), hx_target='#agents-table', hx_swap='outerHTML')
    return render_template('edit_agent_page.html', action='Edit', agent=agent, errors=errors,
        action_url=url_for('edit_agent', agent_id=agent.id), hx_post_url=None, hx_target=None, hx_swap=None)


@app.route('/agents/delete/<int:agent_id>', methods=['POST'])
@login_required
def delete_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    db.session.delete(agent)
    db.session.commit()
    return redirect(url_for('agents'))


# BILLING CRUD
@app.route('/billing')
@login_required
def billing():
    billings = Billing.query.all()
    return render_template('billing.html', billings=billings)


@app.route('/billing/add', methods=['GET', 'POST'])
@login_required
def add_billing():
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
@login_required
def edit_billing(billing_id):
    billing = Billing.query.get_or_404(billing_id)
    if request.method == 'POST':
        billing.job_id = request.form['job_id']
        billing.amount = request.form['amount']
        billing.discount_id = request.form['discount_id']
        db.session.commit()
        return redirect(url_for('billing'))
    return render_template('billing_form.html', action='Edit', billing=billing)


@app.route('/billing/delete/<int:billing_id>', methods=['POST'])
@login_required
def delete_billing(billing_id):
    billing = Billing.query.get_or_404(billing_id)
    db.session.delete(billing)
    db.session.commit()
    return redirect(url_for('billing'))


# DISCOUNTS CRUD
@app.route('/discounts')
@login_required
def discounts():
    discounts = Discount.query.all()
    return render_template('discounts.html', discounts=discounts)


@app.route('/discounts/add', methods=['GET', 'POST'])
@login_required
def add_discount():
    if request.method == 'POST':
        code = request.form['code']
        percent = request.form['percent']
        discount = Discount(code=code, percent=percent)
        db.session.add(discount)
        db.session.commit()
        return redirect(url_for('discounts'))
    return render_template('discount_form.html', action='Add')


@app.route('/discounts/edit/<int:discount_id>', methods=['GET', 'POST'])
@login_required
def edit_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    if request.method == 'POST':
        discount.code = request.form['code']
        discount.percent = request.form['percent']
        db.session.commit()
        return redirect(url_for('discounts'))
    return render_template('discount_form.html', action='Edit', discount=discount)


@app.route('/discounts/delete/<int:discount_id>', methods=['POST'])
@login_required
def delete_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    db.session.delete(discount)
    db.session.commit()
    return redirect(url_for('discounts'))


# SERVICES CRUD
@app.route('/services')
@login_required
def services():
    name = request.args.get('name', '')
    status = request.args.get('status', '')
    query = Service.query
    if name:
        query = query.filter(Service.name.ilike(f'%{name}%'))
    if status:
        query = query.filter(Service.status == status)
    services = query.all()
    if request.headers.get('HX-Request') == 'true':
        return render_template('services.html', services=services)
    return render_template('services.html', services=services)


@app.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
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
@login_required
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.status = request.form['status']
        db.session.commit()
        return redirect(url_for('services'))
    return render_template('service_form.html', action='Edit', service=service)


@app.route('/services/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    service = Service.query.get_or_404(service_id)
    db.session.delete(service)
    db.session.commit()
    return redirect(url_for('services'))


# VEHICLES CRUD
@app.route('/vehicles')
@login_required
def vehicles():
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
    if request.headers.get('HX-Request') == 'true':
        return render_template('vehicles.html', vehicles=vehicles)
    return render_template('vehicles.html', vehicles=vehicles)


@app.route('/vehicles/add', methods=['GET', 'POST'])
@login_required
def add_vehicle():
    errors = {}
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        type_ = request.form['type']
        status = request.form['status']
        vehicle = Vehicle(name=name, number=number, type=type_, status=status)
        db.session.add(vehicle)
        db.session.commit()
        return redirect(url_for('vehicles'))
    return render_template('vehicle_form.html', action='Add', vehicle=None, errors=errors)


@app.route('/vehicles/edit/<int:vehicle_id>', methods=['GET', 'POST'])
@login_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    errors = {}
    if request.method == 'POST':
        vehicle.name = request.form['name']
        vehicle.number = request.form['number']
        vehicle.type = request.form['type']
        vehicle.status = request.form['status']
        db.session.commit()
        return redirect(url_for('vehicles'))
    return render_template('vehicle_form.html', action='Edit', vehicle=vehicle, errors=errors)


@app.route('/vehicles/delete/<int:vehicle_id>', methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect(url_for('vehicles'))


@app.route('/api/quick_add/agent', methods=['POST'])
@login_required
@validate_json_input
@handle_database_errors
def api_quick_add_agent():
    data = request.json
    from models import Agent
    
    # Validate required fields
    if not data.get('name'):
        app.logger.warning('Agent creation failed: missing name')
        return jsonify({'error': 'Agent name is required'}), 400
    
    # Validate email format if provided
    email = data.get('email', '').strip()
    if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        app.logger.warning(f'Agent creation failed: invalid email format {email}')
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Validate mobile format if provided
    mobile = data.get('mobile', '').strip()
    if mobile and not re.match(r'^[\d\s\-\+\(\)]+$', mobile):
        app.logger.warning(f'Agent creation failed: invalid mobile format {mobile}')
        return jsonify({'error': 'Invalid mobile number format'}), 400
    
    try:
        agent = Agent(
            name=data.get('name', '').strip(),
            email=email,
            mobile=mobile,
            type=data.get('type', '').strip(),
            status=data.get('status', 'Active')
        )
        db.session.add(agent)
        db.session.commit()
        
        app.logger.info(f'Agent created successfully by user {current_user.username}: {agent.id}')
        return jsonify({
            'id': agent.id,
            'name': agent.name,
            'email': agent.email,
            'mobile': agent.mobile
        })
    except Exception as e:
        app.logger.error(f'Error creating agent: {str(e)}')
        return jsonify({'error': 'Failed to create agent'}), 500

@app.route('/api/quick_add/service', methods=['POST'])
@login_required
def api_quick_add_service():
    data = request.json
    from models import Service
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
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
@login_required
def api_quick_add_vehicle():
    data = request.json
    from models import Vehicle
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
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
@login_required
def api_quick_add_driver():
    data = request.json
    from models import Driver
    if not data:
        return jsonify({'error': 'No input data provided'}), 400
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

@app.cli.command('create-admin')
@click.argument('username')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin(username, email, password):
    from models import User, Role
    from app import db
    fleet_manager_role = Role.query.filter_by(name='fleet_manager').first()
    if not fleet_manager_role:
        fleet_manager_role = Role(name='fleet_manager', description='Fleet Manager')
        db.session.add(fleet_manager_role)
        db.session.commit()
    system_admin_role = Role.query.filter_by(name='system_admin').first()
    if not system_admin_role:
        system_admin_role = Role(name='system_admin', description='System Administrator')
        db.session.add(system_admin_role)
        db.session.commit()
    user = User.query.filter_by(username=username).first()
    if user:
        click.echo(f'User {username} already exists.')
        return
    user = User(username=username, email=email, active=True)
    user.set_password(password)
    user.roles.append(fleet_manager_role)
    user.roles.append(system_admin_role)
    db.session.add(user)
    db.session.commit()
    click.echo(f'Admin user {username} created successfully.')

# CSRF token is automatically handled by Flask-WTF and Flask-Security

@app.context_processor
def inject_role_helpers():
    def has_role(role_name):
        return any(role.name == role_name for role in getattr(current_user, 'roles', []))
    def has_any_role(*role_names):
        return any(role.name in role_names for role in getattr(current_user, 'roles', []))
    return dict(has_role=has_role, has_any_role=has_any_role)

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)