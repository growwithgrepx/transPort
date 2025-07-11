#!/usr/bin/env python3
"""
Debug script to test job form template rendering
"""

from app import app, db
from models import Vehicle, Agent, Service, Driver
from flask import render_template_string

with app.app_context():
    print("Debugging job form template...")
    print("=" * 50)
    
    # Get the data that would be passed to the template
    agents = Agent.query.filter_by(status='Active').all()
    services = Service.query.filter_by(status='Active').all()
    vehicles = Vehicle.query.filter_by(status='Active').all()
    drivers = Driver.query.all()
    
    print(f"Data being passed to template:")
    print(f"- Agents: {len(agents)}")
    print(f"- Services: {len(services)}")
    print(f"- Vehicles: {len(vehicles)}")
    print(f"- Drivers: {len(drivers)}")
    
    # Test template rendering with just the vehicle dropdown
    template_code = """
    <select class="form-select" id="vehicle_id" name="vehicle_id" required>
      <option value="">Select Vehicle</option>
    {% for vehicle in vehicles %}
        <option value="{{ vehicle.id }}" data-type="{{ vehicle.type }}" data-number="{{ vehicle.number }}" {% if job and job.vehicle_id == vehicle.id %}selected{% endif %}>
          {{ vehicle.number }} ({{ vehicle.name }})
        </option>
    {% endfor %}
    </select>
    """
    
    try:
        rendered = render_template_string(template_code, vehicles=vehicles, job=None)
        print("\nRendered vehicle dropdown:")
        print(rendered)
    except Exception as e:
        print(f"Error rendering template: {e}")
    
    print("\n" + "=" * 50)
    print("Debug completed!") 