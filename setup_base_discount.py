#!/usr/bin/env python3
"""
Script to set up base discount for the transport system
"""

from app import app
from models import Discount
from extensions import db

def setup_base_discount():
    """Set up a base discount for the system"""
    with app.app_context():
        # Check if base discount already exists
        existing_base_discount = Discount.query.filter_by(is_base_discount=True, is_active=True).first()
        
        if existing_base_discount:
            print(f"Base discount already exists: {existing_base_discount.name} ({existing_base_discount.percent}%)")
            return
        
        # Create a new base discount
        base_discount = Discount(
            name="Standard Base Discount",
            code="BASE10",
            percent=10.0,  # 10% base discount
            discount_type='percentage',
            is_base_discount=True,
            is_active=True
        )
        
        db.session.add(base_discount)
        db.session.commit()
        
        print(f"Base discount created successfully: {base_discount.name} ({base_discount.percent}%)")

if __name__ == "__main__":
    setup_base_discount() 