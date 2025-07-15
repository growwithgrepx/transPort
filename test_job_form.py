#!/usr/bin/env python3
"""
Test script to debug job form
"""

from app import app, db
from models import Vehicle, Agent, Service, Driver

with app.app_context():
    print("Testing job form data...")
    print("=" * 50)
    
    # Test vehicle query
    vehicles = Vehicle.query.filter_by(status='Active').all()
    print(f"Active vehicles found: {len(vehicles)}")
    
    for vehicle in vehicles:
        print(f"- ID: {vehicle.id}")
        print(f"  Name: {vehicle.name}")
        print(f"  Number: {vehicle.number}")
        print(f"  Type: {vehicle.type}")
        print(f"  Status: {vehicle.status}")
        print()
    
    # Test other entities
    agents = Agent.query.filter_by(status='Active').all()
    services = Service.query.filter_by(status='Active').all()
    drivers = Driver.query.all()
    
    print(f"Active agents: {len(agents)}")
    print(f"Active services: {len(services)}")
    print(f"All drivers: {len(drivers)}")
    
    print("\n" + "=" * 50)
    print("Test completed!") 