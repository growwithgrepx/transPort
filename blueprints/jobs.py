from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from extensions import db
from models import Job

jobs_bp = Blueprint('jobs', __name__, template_folder='../templates')

@jobs_bp.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
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