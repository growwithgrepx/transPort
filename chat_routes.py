from flask import request, jsonify, make_response
from app import app, db, csrf
from models import Job, Driver, Agent, Vehicle, Service, Billing, Discount
from datetime import datetime
import re

@app.route('/api/chat', methods=['POST'])
@csrf.exempt
def chat_api():
    try:
        data = request.get_json()
        message = data.get('message', '').lower().strip()
        
        # Parse the message and generate response
        response, data = parse_chat_message(message)
        
        return jsonify({
            'response': response,
            'data': data
        })
        
    except Exception as e:
        return jsonify({
            'response': f'Sorry, I encountered an error: {str(e)}',
            'data': None
        }), 500

@app.route('/api/chat/download', methods=['POST'])
@csrf.exempt
def chat_download():
    try:
        data = request.get_json()
        query = data.get('query', '')
        table_data = data.get('data', [])
        
        if not table_data:
            return jsonify({'error': 'No data to download'}), 400
        
        # Create CSV content
        import csv
        import io
        
        output = io.StringIO()
        if table_data:
            writer = csv.DictWriter(output, fieldnames=table_data[0].keys())
            writer.writeheader()
            writer.writerows(table_data)
        
        csv_content = output.getvalue()
        output.close()
        
        # Create response
        response = make_response(csv_content)
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = f'attachment; filename="{query.replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.csv"'
        
        return response
        
    except Exception as e:
        return jsonify({'error': f'Download error: {str(e)}'}), 500

def parse_chat_message(message):
    """Parse chat message and return appropriate response and data"""
    
    # Jobs queries
    if re.search(r'\b(all\s+)?jobs?\b', message):
        return handle_jobs_query(message)
    
    # Driver queries
    elif re.search(r'\bdrivers?\b', message):
        return handle_drivers_query(message)
    
    # Vehicle queries
    elif re.search(r'\bvehicles?\b', message):
        return handle_vehicles_query(message)
    
    # Agent queries
    elif re.search(r'\bagents?\b', message):
        return handle_agents_query(message)
    
    # Service queries
    elif re.search(r'\bservices?\b', message):
        return handle_services_query(message)
    
    # Billing queries
    elif re.search(r'\bbilling?\b', message):
        return handle_billing_query(message)
    
    # Payment queries
    elif re.search(r'\bpayment\b', message):
        return handle_payment_query(message)
    
    # Status queries
    elif re.search(r'\bstatus\b', message):
        return handle_status_query(message)
    
    # Dashboard/Summary queries
    elif re.search(r'\b(dashboard|summary|overview)\b', message):
        return handle_dashboard_query(message)
    
    # Help
    elif re.search(r'\b(help|what can you do)\b', message):
        return handle_help_query(message)
    
    else:
        return "I'm not sure what you're asking for. Try asking about jobs, drivers, vehicles, agents, services, or payment status.", None

def handle_jobs_query(message):
    """Handle job-related queries"""
    
    if re.search(r'\bactive\b', message):
        jobs = Job.query.filter(Job.order_status.in_(['New', 'In Progress'])).limit(10).all()
        return f"I found {len(jobs)} active jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bpending\b', message):
        jobs = Job.query.filter(Job.order_status == 'Pending').limit(10).all()
        return f"I found {len(jobs)} pending jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bcompleted\b', message):
        jobs = Job.query.filter(Job.order_status == 'Completed').limit(10).all()
        return f"I found {len(jobs)} completed jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bcancelled\b', message):
        jobs = Job.query.filter(Job.order_status == 'Cancelled').limit(10).all()
        return f"I found {len(jobs)} cancelled jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bunpaid\b', message):
        jobs = Job.query.filter(Job.payment_status == 'Unpaid').limit(10).all()
        return f"I found {len(jobs)} unpaid jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bpaid\b', message):
        jobs = Job.query.filter(Job.payment_status == 'Paid').limit(10).all()
        return f"I found {len(jobs)} paid jobs:", [format_job(job) for job in jobs]
    
    else:
        # All jobs
        jobs = Job.query.order_by(Job.id.desc()).limit(10).all()
        return f"I found {len(jobs)} recent jobs:", [format_job(job) for job in jobs]

def handle_drivers_query(message):
    """Handle driver-related queries"""
    
    if re.search(r'\bavailable\b', message):
        # Drivers not assigned to active jobs
        active_driver_ids = db.session.query(Job.driver_id).filter(
            Job.order_status.in_(['New', 'In Progress'])
        ).distinct().all()
        active_ids = [id[0] for id in active_driver_ids if id[0]]
        
        drivers = Driver.query.filter(~Driver.id.in_(active_ids)).all()
        return f"I found {len(drivers)} available drivers:", [format_driver(driver) for driver in drivers]
    
    else:
        drivers = Driver.query.limit(10).all()
        return f"I found {len(drivers)} drivers:", [format_driver(driver) for driver in drivers]

def handle_vehicles_query(message):
    """Handle vehicle-related queries"""
    
    if re.search(r'\bavailable\b', message):
        # Get vehicles that are not currently assigned to active jobs
        # Since Job model doesn't have vehicle_id, we'll check by vehicle number
        active_jobs = Job.query.filter(Job.order_status.in_(['New', 'In Progress'])).all()
        active_vehicle_numbers = [job.vehicle_number for job in active_jobs if job.vehicle_number]
        
        # Get vehicles not in active jobs
        available_vehicles = Vehicle.query.filter(~Vehicle.number.in_(active_vehicle_numbers)).all()
        return f"I found {len(available_vehicles)} available vehicles:", [format_vehicle(vehicle) for vehicle in available_vehicles]
    
    else:
        vehicles = Vehicle.query.limit(10).all()
        return f"I found {len(vehicles)} vehicles:", [format_vehicle(vehicle) for vehicle in vehicles]

def handle_agents_query(message):
    """Handle agent-related queries"""
    agents = Agent.query.limit(10).all()
    return f"I found {len(agents)} agents:", [format_agent(agent) for agent in agents]

def handle_services_query(message):
    """Handle service-related queries"""
    services = Service.query.limit(10).all()
    return f"I found {len(services)} services:", [format_service(service) for service in services]

def handle_billing_query(message):
    """Handle billing-related queries"""
    billings = Billing.query.limit(10).all()
    return f"I found {len(billings)} billing records:", [format_billing(billing) for billing in billings]

def handle_payment_query(message):
    """Handle payment-related queries"""
    
    if re.search(r'\bunpaid\b', message):
        jobs = Job.query.filter(Job.payment_status == 'Unpaid').limit(10).all()
        return f"I found {len(jobs)} unpaid jobs:", [format_job(job) for job in jobs]
    
    elif re.search(r'\bpaid\b', message):
        jobs = Job.query.filter(Job.payment_status == 'Paid').limit(10).all()
        return f"I found {len(jobs)} paid jobs:", [format_job(job) for job in jobs]
    
    else:
        # Payment summary
        total_jobs = Job.query.count()
        paid_jobs = Job.query.filter(Job.payment_status == 'Paid').count()
        unpaid_jobs = Job.query.filter(Job.payment_status == 'Unpaid').count()
        
        return f"Payment Summary:\n- Total Jobs: {total_jobs}\n- Paid: {paid_jobs}\n- Unpaid: {unpaid_jobs}", None

def handle_status_query(message):
    """Handle status-related queries"""
    
    # Job status summary
    new_jobs = Job.query.filter(Job.order_status == 'New').count()
    in_progress_jobs = Job.query.filter(Job.order_status == 'In Progress').count()
    completed_jobs = Job.query.filter(Job.order_status == 'Completed').count()
    cancelled_jobs = Job.query.filter(Job.order_status == 'Cancelled').count()
    
    return f"Job Status Summary:\n- New: {new_jobs}\n- In Progress: {in_progress_jobs}\n- Completed: {completed_jobs}\n- Cancelled: {cancelled_jobs}", None

def handle_dashboard_query(message):
    """Handle dashboard/summary queries"""
    
    # Overall summary
    total_jobs = Job.query.count()
    total_drivers = Driver.query.count()
    total_vehicles = Vehicle.query.count()
    total_agents = Agent.query.count()
    
    active_jobs = Job.query.filter(Job.order_status.in_(['New', 'In Progress'])).count()
    completed_jobs = Job.query.filter(Job.order_status == 'Completed').count()
    unpaid_jobs = Job.query.filter(Job.payment_status == 'Unpaid').count()
    
    return f"Fleet Dashboard Summary:\n- Total Jobs: {total_jobs}\n- Active Jobs: {active_jobs}\n- Completed Jobs: {completed_jobs}\n- Unpaid Jobs: {unpaid_jobs}\n- Total Drivers: {total_drivers}\n- Total Vehicles: {total_vehicles}\n- Total Agents: {total_agents}", None

def handle_help_query(message):
    """Handle help queries"""
    return """I can help you with the following queries:

**Jobs:**
- "Show all jobs"
- "Active jobs"
- "Pending jobs"
- "Completed jobs"
- "Unpaid jobs"

**Drivers:**
- "All drivers"
- "Available drivers"

**Vehicles:**
- "All vehicles"
- "Available vehicles"

**Others:**
- "Payment status"
- "Job status"
- "Dashboard summary"

Try asking me about any of these topics!""", None

# Data formatting functions
def format_job(job):
    return {
        'id': job.id,
        'customer_name': job.customer_name,
        'pickup_location': job.pickup_location,
        'dropoff_location': job.dropoff_location,
        'order_status': job.order_status,
        'payment_status': job.payment_status,
        'pickup_date': job.pickup_date,
        'driver_contact': job.driver_contact,
        'vehicle_type': job.vehicle_type
    }

def format_driver(driver):
    return {
        'id': driver.id,
        'name': driver.name,
        'phone': driver.phone
    }

def format_vehicle(vehicle):
    return {
        'id': vehicle.id,
        'name': vehicle.name,
        'number': vehicle.number,
        'type': vehicle.type,
        'status': vehicle.status
    }

def format_agent(agent):
    return {
        'id': agent.id,
        'name': agent.name,
        'email': agent.email,
        'mobile': agent.mobile,
        'type': agent.type,
        'status': agent.status
    }

def format_service(service):
    return {
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'status': service.status
    }

def format_billing(billing):
    return {
        'id': billing.id,
        'job_id': billing.job_id,
        'amount': billing.amount,
        'discount_id': billing.discount_id
    } 