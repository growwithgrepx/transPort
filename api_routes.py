from flask import request, jsonify
from app import app, db
from models import Agent, Service, Vehicle, Driver

@app.route('/api/quick_add/agent', methods=['POST'])
def api_quick_add_agent():
    try:
        name = request.form.get('name')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        commission_rate = request.form.get('commission_rate', 0)
        
        if not name:
            return jsonify({'success': False, 'error': 'Name is required'}), 400
        
        # Check if agent already exists
        existing_agent = Agent.query.filter_by(name=name).first()
        if existing_agent:
            return jsonify({'success': False, 'error': 'Agent already exists'}), 400
        
        # Create new agent
        agent = Agent(
            name=name,
            email=email,
            phone=phone,
            commission_rate=commission_rate
        )
        
        db.session.add(agent)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'agent': {
                'id': agent.id,
                'name': agent.name,
                'email': agent.email,
                'phone': agent.phone
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/quick_add/service', methods=['POST'])
def api_quick_add_service():
    try:
        name = request.form.get('name')
        description = request.form.get('description', '')
        base_price = request.form.get('base_price', 0)
        
        if not name:
            return jsonify({'success': False, 'error': 'Service name is required'}), 400
        
        # Check if service already exists
        existing_service = Service.query.filter_by(name=name).first()
        if existing_service:
            return jsonify({'success': False, 'error': 'Service already exists'}), 400
        
        # Create new service
        service = Service(
            name=name,
            description=description,
            base_price=base_price
        )
        
        db.session.add(service)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'service': {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'base_price': service.base_price
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/quick_add/vehicle', methods=['POST'])
def api_quick_add_vehicle():
    try:
        registration_number = request.form.get('registration_number')
        make = request.form.get('make', '')
        model = request.form.get('model', '')
        year = request.form.get('year')
        capacity = request.form.get('capacity')
        fuel_type = request.form.get('fuel_type', '')
        
        if not registration_number:
            return jsonify({'success': False, 'error': 'Registration number is required'}), 400
        
        # Check if vehicle already exists
        existing_vehicle = Vehicle.query.filter_by(registration_number=registration_number).first()
        if existing_vehicle:
            return jsonify({'success': False, 'error': 'Vehicle already exists'}), 400
        
        # Create new vehicle
        vehicle = Vehicle(
            registration_number=registration_number,
            make=make,
            model=model,
            year=year,
            capacity=capacity,
            fuel_type=fuel_type
        )
        
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'vehicle': {
                'id': vehicle.id,
                'registration_number': vehicle.registration_number,
                'make': vehicle.make,
                'model': vehicle.model
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/quick_add/driver', methods=['POST'])
def api_quick_add_driver():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        license_number = request.form.get('license_number', '')
        
        if not name:
            return jsonify({'success': False, 'error': 'Driver name is required'}), 400
        
        # Check if driver already exists
        existing_driver = Driver.query.filter_by(name=name).first()
        if existing_driver:
            return jsonify({'success': False, 'error': 'Driver already exists'}), 400
        
        # Create new driver
        driver = Driver(
            name=name,
            phone=phone,
            email=email,
            license_number=license_number
        )
        
        db.session.add(driver)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'driver': {
                'id': driver.id,
                'name': driver.name,
                'phone': driver.phone,
                'email': driver.email
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500 