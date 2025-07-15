#!/usr/bin/env python3
"""
Script to check vehicles in the database
"""

from app import app, db
from models import Vehicle

with app.app_context():
    print("Checking vehicles in database...")
    print("=" * 50)
    
    # Check all vehicles
    all_vehicles = Vehicle.query.all()
    print(f"Total vehicles: {len(all_vehicles)}")
    
    if all_vehicles:
        print("\nAll vehicles:")
        for vehicle in all_vehicles:
            print(f"- ID: {vehicle.id}, Name: {vehicle.name}, Number: {vehicle.number}, Type: {vehicle.type}, Status: {vehicle.status}")
    else:
        print("No vehicles found in database")
    
    # Check active vehicles
    active_vehicles = Vehicle.query.filter_by(status='Active').all()
    print(f"\nActive vehicles: {len(active_vehicles)}")
    
    if active_vehicles:
        print("\nActive vehicles:")
        for vehicle in active_vehicles:
            print(f"- ID: {vehicle.id}, Name: {vehicle.name}, Number: {vehicle.number}, Type: {vehicle.type}, Status: {vehicle.status}")
    else:
        print("No active vehicles found")
    
    # Check different statuses
    statuses = db.session.query(Vehicle.status).distinct().all()
    print(f"\nAvailable statuses: {[s[0] for s in statuses]}")
    
    print("\n" + "=" * 50)
    print("Script completed!") 