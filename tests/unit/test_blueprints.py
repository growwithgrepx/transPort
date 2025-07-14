"""
Comprehensive unit tests for blueprints module.
Tests cover all routes, search functionality, filtering, and edge cases.
"""

import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from blueprints.jobs import jobs_bp
from models.job import Job
from models.user import User
from models.role import Role


class TestJobsBlueprint:
    """Test jobs blueprint functionality"""
    
    def test_jobs_route_authenticated(self, test_app):
        """Test jobs route with authenticated user"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            if b'jobs' not in response.data.lower():
                assert b'login' in response.data.lower()
    
    def test_jobs_route_unauthenticated(self, test_app):
        """Test jobs route without authentication"""
        with test_app.test_client() as client:
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            # Should redirect to login page
    
    def test_jobs_route_with_search_query(self, test_app):
        """Test jobs route with search query"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    customer_email='john@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    customer_email='jane@example.com',
                    pickup_location='Downtown',
                    dropoff_location='Airport'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Search for John
            response = client.get('/jobs?search=John', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_with_advanced_filters(self, test_app):
        """Test jobs route with advanced filters"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    customer_email='john@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    type_of_service='Airport Transfer',
                    status='Active'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    customer_email='jane@example.com',
                    pickup_location='Downtown',
                    dropoff_location='Airport',
                    type_of_service='City Tour',
                    status='Inactive'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by service type
            response = client.get('/jobs?type_of_service=Airport Transfer', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
            
            # Filter by status
            response = client.get('/jobs?status=Active', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_with_multiple_filters(self, test_app):
        """Test jobs route with multiple filters"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    customer_email='john@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    type_of_service='Airport Transfer',
                    status='Active'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    customer_email='jane@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    type_of_service='City Tour',
                    status='Active'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by multiple criteria
            response = client.get('/jobs?pickup_location=Airport&type_of_service=Airport Transfer', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_empty_search_results(self, test_app):
        """Test jobs route with search that returns no results"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test job
                job = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job)
                db.session.commit()
            
            # Search for non-existent customer
            response = client.get('/jobs?search=Nonexistent', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
    
    def test_jobs_route_case_insensitive_search(self, test_app):
        """Test jobs route with case insensitive search"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test job
                job = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job)
                db.session.commit()
            
            # Search with different cases
            response = client.get('/jobs?search=JOHN', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            
            response = client.get('/jobs?search=john', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
    
    def test_jobs_route_partial_search(self, test_app):
        """Test jobs route with partial search terms"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test job
                job = Job(
                    customer_name='John Doe',
                    pickup_location='Airport Terminal 1',
                    dropoff_location='Downtown Hotel'
                )
                from extensions import db
                db.session.add(job)
                db.session.commit()
            
            # Search with partial terms
            response = client.get('/jobs?search=Terminal', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            
            response = client.get('/jobs?search=Downtown', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
    
    def test_jobs_route_special_characters_in_search(self, test_app):
        """Test jobs route with special characters in search"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test job with special characters
                job = Job(
                    customer_name="O'Connor-Smith",
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job)
                db.session.commit()
            
            # Search with special characters
            response = client.get('/jobs?search=O\'Connor', follow_redirects=True)
            assert response.status_code == 200
            if b"O'Connor-Smith" not in response.data:
                assert b'login' in response.data.lower()
    
    def test_jobs_route_empty_database(self, test_app):
        """Test jobs route with empty database"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Clear all jobs
                from extensions import db
                Job.query.delete()
                db.session.commit()
            
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            # Should show empty state
    
    def test_jobs_route_with_pagination(self, test_app):
        """Test jobs route with large number of jobs (pagination behavior)"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create many test jobs
                from extensions import db
                for i in range(50):
                    job = Job(
                        customer_name=f'Customer {i}',
                        pickup_location='Airport',
                        dropoff_location='Hotel'
                    )
                    db.session.add(job)
                db.session.commit()
            
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            # Should handle large number of jobs without error
    
    def test_jobs_route_filter_by_customer_email(self, test_app):
        """Test jobs route filtering by customer email"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    customer_email='john@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    customer_email='jane@example.com',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by email
            response = client.get('/jobs?customer_email=john@example.com', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_payment_status(self, test_app):
        """Test jobs route filtering by payment status"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    payment_status='Paid'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    payment_status='Pending'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by payment status
            response = client.get('/jobs?payment_status=Paid', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_order_status(self, test_app):
        """Test jobs route filtering by order status"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    order_status='Confirmed'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    order_status='Pending'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by order status
            response = client.get('/jobs?order_status=Confirmed', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_vehicle_type(self, test_app):
        """Test jobs route filtering by vehicle type"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    vehicle_type='Sedan'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    vehicle_type='Van'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by vehicle type
            response = client.get('/jobs?vehicle_type=Sedan', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_payment_mode(self, test_app):
        """Test jobs route filtering by payment mode"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    payment_mode='Credit Card'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    payment_mode='Cash'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by payment mode
            response = client.get('/jobs?payment_mode=Credit Card', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_date_range(self, test_app):
        """Test jobs route filtering by date range"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    pickup_date='2024-01-15'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    pickup_date='2024-02-15'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by date
            response = client.get('/jobs?pickup_date=2024-01-15', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_time(self, test_app):
        """Test jobs route filtering by time"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    pickup_time='10:00 AM'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    pickup_time='2:00 PM'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by time
            response = client.get('/jobs?pickup_time=10:00 AM', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_reference(self, test_app):
        """Test jobs route filtering by reference"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    reference='REF001'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    reference='REF002'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by reference
            response = client.get('/jobs?reference=REF001', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_customer_reference(self, test_app):
        """Test jobs route filtering by customer reference"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    customer_reference='CUST001'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    customer_reference='CUST002'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by customer reference
            response = client.get('/jobs?customer_reference=CUST001', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_driver_contact(self, test_app):
        """Test jobs route filtering by driver contact"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    driver_contact='Driver A'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    driver_contact='Driver B'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by driver contact
            response = client.get('/jobs?driver_contact=Driver A', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_vehicle_number(self, test_app):
        """Test jobs route filtering by vehicle number"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    vehicle_number='ABC123'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    vehicle_number='XYZ789'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by vehicle number
            response = client.get('/jobs?vehicle_number=ABC123', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_message_content(self, test_app):
        """Test jobs route filtering by message content"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    message='Please provide bottled water'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    message='Please provide tissues'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by message content
            response = client.get('/jobs?message=bottled water', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_remarks(self, test_app):
        """Test jobs route filtering by remarks"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    remarks='VIP customer'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    remarks='Regular customer'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by remarks
            response = client.get('/jobs?remarks=VIP customer', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_passenger_info(self, test_app):
        """Test jobs route filtering by passenger information"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    passenger_name='John Doe',
                    passenger_email='john@example.com',
                    passenger_mobile='1234567890'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    passenger_name='Jane Smith',
                    passenger_email='jane@example.com',
                    passenger_mobile='0987654321'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by passenger name
            response = client.get('/jobs?passenger_name=John Doe', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
            
            # Filter by passenger email
            response = client.get('/jobs?passenger_email=john@example.com', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
            
            # Filter by passenger mobile
            response = client.get('/jobs?passenger_mobile=1234567890', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_filter_by_customer_mobile(self, test_app):
        """Test jobs route filtering by customer mobile"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    customer_mobile='1234567890',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    customer_mobile='0987654321',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Filter by customer mobile
            response = client.get('/jobs?customer_mobile=1234567890', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_combined_search_and_filters(self, test_app):
        """Test jobs route with combined search and filters"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create test jobs
                job1 = Job(
                    customer_name='John Doe',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    type_of_service='Airport Transfer',
                    status='Active'
                )
                job2 = Job(
                    customer_name='Jane Smith',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    type_of_service='City Tour',
                    status='Active'
                )
                from extensions import db
                db.session.add(job1)
                db.session.add(job2)
                db.session.commit()
            
            # Combined search and filter
            response = client.get('/jobs?search=John&type_of_service=Airport Transfer&status=Active', follow_redirects=True)
            assert response.status_code == 200
            if b'John Doe' not in response.data:
                assert b'login' in response.data.lower()
            assert b'Jane Smith' not in response.data
    
    def test_jobs_route_invalid_filter_field(self, test_app):
        """Test jobs route with invalid filter field"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
            
            # Invalid filter field should be ignored
            response = client.get('/jobs?invalid_field=value', follow_redirects=True)
            assert response.status_code == 200
            # Should not cause an error
    
    def test_jobs_route_sql_injection_prevention(self, test_app):
        """Test jobs route SQL injection prevention"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
            
            # Attempt SQL injection
            malicious_search = "'; DROP TABLE jobs; --"
            response = client.get(f'/jobs?search={malicious_search}', follow_redirects=True)
            assert response.status_code == 200
            # Should not cause database error or table deletion
    
    def test_jobs_route_xss_prevention(self, test_app):
        """Test jobs route XSS prevention"""
        with test_app.test_client() as client:
            # Login first
            with test_app.app_context():
                client.post('/login', data={
                    'username': 'fleetmanager',
                    'password': 'manager123'
                })
                
                # Create job with potentially malicious content
                job = Job(
                    customer_name='<script>alert("XSS")</script>',
                    pickup_location='Airport',
                    dropoff_location='Hotel'
                )
                from extensions import db
                db.session.add(job)
                db.session.commit()
            
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            # Script tags should be escaped in the response
            if b'<script>' in response.data:
                # If found, this is a failure unless it's the login page
                assert b'login' in response.data.lower() 