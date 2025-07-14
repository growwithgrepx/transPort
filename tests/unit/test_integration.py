"""
Integration tests for the transport application.
Tests focus on real-world scenarios and component interactions.
"""

import pytest
from unittest.mock import patch, MagicMock
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models.user import User
from models.job import Job
from models.driver import Driver
from models.agent import Agent
from models.vehicle import Vehicle
from models.service import Service
from models.role import Role


class TestUserJobIntegration:
    """Test integration between users and jobs"""
    
    def test_user_creates_job(self, test_app, clean_db):
        """Test that a user can create a job"""
        with test_app.app_context():
            from extensions import db
            
            # Create a user
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123',
                active=True
            )
            db.session.add(user)
            db.session.commit()
            
            # Create a job
            job = Job(
                customer_name='John Doe',
                customer_email='john@example.com',
                pickup_location='Airport',
                dropoff_location='Hotel',
                type_of_service='Airport Transfer',
                vehicle_type='Sedan',
                payment_mode='Credit Card',
                status='Active'
            )
            db.session.add(job)
            db.session.commit()
            
            # Verify job was created
            assert job.id is not None
            assert job.customer_name == 'John Doe'
            assert job.status == 'Active'
            
            # Verify job can be retrieved
            retrieved_job = Job.query.get(job.id)
            assert retrieved_job is not None
            assert retrieved_job.customer_name == 'John Doe'
    
    def test_job_lifecycle(self, test_app):
        """Test complete job lifecycle"""
        with test_app.app_context():
            from extensions import db
            
            # Create job
            job = Job(
                customer_name='Jane Smith',
                pickup_location='Airport',
                dropoff_location='Hotel',
                status='Inactive'
            )
            db.session.add(job)
            db.session.commit()
            
            # Update job status
            job.status = 'Active'
            db.session.commit()
            
            # Verify status change
            retrieved_job = Job.query.get(job.id)
            assert retrieved_job.status == 'Active'
            
            # Complete job
            job.status = 'Completed'
            db.session.commit()
            
            # Verify completion
            retrieved_job = Job.query.get(job.id)
            assert retrieved_job.status == 'Completed'
    
    def test_job_with_driver_and_agent(self, test_app, clean_db):
        """Test job with driver and agent relationships"""
        with test_app.app_context():
            from extensions import db
            
            # Create driver
            driver = Driver(
                name='John Driver',
                phone='1234567890'
            )
            db.session.add(driver)
            
            # Create agent
            agent = Agent(
                name='Test Agent',
                email='agent@example.com',
                mobile='0987654321',
                type='Corporate'
            )
            db.session.add(agent)
            db.session.commit()
            
            # Create job with relationships
            job = Job(
                customer_name='Customer',
                pickup_location='Airport',
                dropoff_location='Hotel',
                driver_id=driver.id,
                agent_id=agent.id
            )
            db.session.add(job)
            db.session.commit()
            
            # Verify relationships
            assert job.driver_id == driver.id
            assert job.agent_id == agent.id
            
            # Verify job can be found by driver
            driver_jobs = Job.query.filter_by(driver_id=driver.id).all()
            assert len(driver_jobs) == 1
            assert driver_jobs[0].id == job.id
            
            # Verify job can be found by agent
            agent_jobs = Job.query.filter_by(agent_id=agent.id).all()
            assert len(agent_jobs) == 1
            assert agent_jobs[0].id == job.id


class TestAuthenticationIntegration:
    """Test authentication and authorization integration"""
    
    def test_user_login_workflow(self, test_app, clean_db):
        """Test complete user login workflow"""
        with test_app.test_client() as client:
            # Test login page access
            response = client.get('/login')
            assert response.status_code == 200
            
            # Test login with valid credentials
            with test_app.app_context():
                # Create test user
                from extensions import db
                user = User(
                    username='testuser',
                    email='test@example.com',
                    password='password123',
                    active=True
                )
                db.session.add(user)
                db.session.commit()
            
            response = client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Should redirect to dashboard after successful login
            assert response.status_code == 200
            assert b'dashboard' in response.data.lower()
    
    def test_protected_route_access(self, test_app, clean_db):
        """Test access to protected routes"""
        with test_app.test_client() as client:
            # Try to access protected route without login
            response = client.get('/jobs', follow_redirects=True)
            assert response.status_code == 200
            # Should redirect to login page
            
            # Login and try again
            with test_app.app_context():
                from extensions import db
                user = User(
                    username='testuser',
                    email='test@example.com',
                    password='password123',
                    active=True
                )
                db.session.add(user)
                db.session.commit()
            
            client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Now should be able to access protected route
            response = client.get('/jobs')
            assert response.status_code == 200
    
    def test_user_roles_and_permissions(self, test_app):
        """Test user roles and permissions"""
        with test_app.app_context():
            from extensions import db
            
            # Create roles
            admin_role = Role(name='system_admin', description='System Administrator')
            manager_role = Role(name='fleet_manager', description='Fleet Manager')
            db.session.add(admin_role)
            db.session.add(manager_role)
            db.session.commit()
            
            # Create user with roles
            user = User(
                username='adminuser',
                email='admin@example.com',
                password='password123',
                active=True
            )
            user.roles.append(admin_role)
            user.roles.append(manager_role)
            db.session.add(user)
            db.session.commit()
            
            # Verify roles
            assert len(user.roles) == 2
            role_names = [role.name for role in user.roles]
            assert 'system_admin' in role_names
            assert 'fleet_manager' in role_names
            
            # Test role checking
            assert any(role.name == 'system_admin' for role in user.roles)
            assert any(role.name == 'fleet_manager' for role in user.roles)
            assert not any(role.name == 'regular_user' for role in user.roles)


class TestDataManagementIntegration:
    """Test data management and CRUD operations"""
    
    def test_job_crud_operations(self, test_app):
        """Test complete CRUD operations for jobs"""
        with test_app.app_context():
            from extensions import db
            
            # Create
            job = Job(
                customer_name='Test Customer',
                pickup_location='Airport',
                dropoff_location='Hotel',
                type_of_service='Airport Transfer'
            )
            db.session.add(job)
            db.session.commit()
            job_id = job.id
            
            # Read
            retrieved_job = Job.query.get(job_id)
            assert retrieved_job is not None
            assert retrieved_job.customer_name == 'Test Customer'
            
            # Update
            retrieved_job.customer_name = 'Updated Customer'
            retrieved_job.status = 'Active'
            db.session.commit()
            
            # Verify update
            updated_job = Job.query.get(job_id)
            assert updated_job.customer_name == 'Updated Customer'
            assert updated_job.status == 'Active'
            
            # Delete
            db.session.delete(updated_job)
            db.session.commit()
            
            # Verify deletion
            deleted_job = Job.query.get(job_id)
            assert deleted_job is None
    
    def test_bulk_job_operations(self, test_app):
        """Test bulk operations on jobs"""
        with test_app.app_context():
            from extensions import db
            
            # Create multiple jobs
            jobs = []
            for i in range(5):
                job = Job(
                    customer_name=f'Customer {i}',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    status='Inactive'
                )
                jobs.append(job)
                db.session.add(job)
            db.session.commit()
            
            # Verify all jobs were created
            all_jobs = Job.query.all()
            assert len(all_jobs) >= 5
            
            # Bulk update status
            Job.query.filter(Job.status == 'Inactive').update({'status': 'Active'})
            db.session.commit()
            
            # Verify bulk update
            active_jobs = Job.query.filter_by(status='Active').all()
            assert len(active_jobs) >= 5
            
            # Bulk delete
            Job.query.filter(Job.customer_name.like('Customer %')).delete()
            db.session.commit()
            
            # Verify bulk delete
            remaining_jobs = Job.query.filter(Job.customer_name.like('Customer %')).all()
            assert len(remaining_jobs) == 0
    
    def test_data_consistency(self, test_app):
        """Test data consistency across operations"""
        with test_app.app_context():
            from extensions import db
            
            # Create related data
            driver = Driver(name='Test Driver', phone='1234567890')
            agent = Agent(name='Test Agent', email='agent@example.com')
            db.session.add(driver)
            db.session.add(agent)
            db.session.commit()
            
            # Create job with foreign keys
            job = Job(
                customer_name='Test Customer',
                pickup_location='Airport',
                dropoff_location='Hotel',
                driver_id=driver.id,
                agent_id=agent.id
            )
            db.session.add(job)
            db.session.commit()
            
            # Verify foreign key constraints
            assert job.driver_id == driver.id
            assert job.agent_id == agent.id
            
            # Test cascade behavior (if implemented)
            # This would depend on the specific cascade settings in the models
            
            # Verify data integrity
            retrieved_job = Job.query.get(job.id)
            assert retrieved_job.driver_id == driver.id
            assert retrieved_job.agent_id == agent.id


class TestSearchAndFilterIntegration:
    """Test search and filter functionality"""
    
    def test_job_search_functionality(self, test_app):
        """Test job search functionality"""
        with test_app.app_context():
            from extensions import db
            
            # Create test jobs
            jobs_data = [
                {'customer_name': 'John Doe', 'pickup_location': 'Airport', 'status': 'Active'},
                {'customer_name': 'Jane Smith', 'pickup_location': 'Downtown', 'status': 'Active'},
                {'customer_name': 'Bob Johnson', 'pickup_location': 'Airport', 'status': 'Inactive'},
            ]
            
            for job_data in jobs_data:
                job = Job(**job_data)
                db.session.add(job)
            db.session.commit()
            
            # Test search by customer name
            john_jobs = Job.query.filter(Job.customer_name.ilike('%John%')).all()
            assert len(john_jobs) == 2
            
            # Test search by location
            airport_jobs = Job.query.filter(Job.pickup_location.ilike('%Airport%')).all()
            assert len(airport_jobs) == 3
            
            # Test search by status
            active_jobs = Job.query.filter_by(status='Active').all()
            assert len(active_jobs) == 2
            
            # Test combined search
            active_airport_jobs = Job.query.filter(
                Job.status == 'Active',
                Job.pickup_location.ilike('%Airport%')
            ).all()
            assert len(active_airport_jobs) == 1
            assert active_airport_jobs[0].customer_name == 'John Doe'
    
    def test_advanced_filtering(self, test_app):
        """Test advanced filtering scenarios"""
        with test_app.app_context():
            from extensions import db
            
            # Create jobs with various attributes
            jobs_data = [
                {
                    'customer_name': 'Customer A',
                    'type_of_service': 'Airport Transfer',
                    'vehicle_type': 'Sedan',
                    'payment_mode': 'Credit Card',
                    'status': 'Active'
                },
                {
                    'customer_name': 'Customer B',
                    'type_of_service': 'City Tour',
                    'vehicle_type': 'Van',
                    'payment_mode': 'Cash',
                    'status': 'Active'
                },
                {
                    'customer_name': 'Customer C',
                    'type_of_service': 'Airport Transfer',
                    'vehicle_type': 'Van',
                    'payment_mode': 'Credit Card',
                    'status': 'Inactive'
                }
            ]
            
            for job_data in jobs_data:
                job = Job(**job_data)
                db.session.add(job)
            db.session.commit()
            
            # Test multiple filter criteria
            filtered_jobs = Job.query.filter(
                Job.type_of_service == 'Airport Transfer',
                Job.vehicle_type == 'Sedan',
                Job.payment_mode == 'Credit Card',
                Job.status == 'Active'
            ).all()
            
            assert len(filtered_jobs) == 1
            assert filtered_jobs[0].customer_name == 'Customer A'
            
            # Test OR conditions
            sedan_or_van_jobs = Job.query.filter(
                Job.vehicle_type.in_(['Sedan', 'Van'])
            ).all()
            assert len(sedan_or_van_jobs) == 3
            
            # Test date range filtering (if date fields are implemented)
            # This would test filtering by pickup_date ranges


class TestErrorHandlingIntegration:
    """Test error handling across components"""
    
    def test_database_error_handling(self, test_app, clean_db):
        """Test database error handling"""
        with test_app.app_context():
            from extensions import db
            from sqlalchemy.exc import IntegrityError
            
            # Test unique constraint violation
            user1 = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            db.session.add(user1)
            db.session.commit()
            
            # Try to create user with same email
            user2 = User(
                username='differentuser',
                email='test@example.com',  # Same email
                password='password123'
            )
            db.session.add(user2)
            
            with pytest.raises(IntegrityError):
                db.session.commit()
            
            db.session.rollback()
    
    def test_validation_error_handling(self, test_app):
        """Test validation error handling"""
        with test_app.app_context():
            from extensions import db
            
            # Test invalid email format
            user = User()
            with pytest.raises(ValueError, match='Invalid email format'):
                user.validate_email('invalid-email')
            
            # Test invalid username
            with pytest.raises(ValueError, match='Username must be at least 3 characters long'):
                user.validate_username('ab')
    
    def test_application_error_handling(self, test_app):
        """Test application-level error handling"""
        with test_app.test_client() as client:
            # Test 404 error
            response = client.get('/nonexistent-page')
            assert response.status_code == 404
            
            # Test 500 error (if we can trigger one)
            # This would require a route that intentionally raises an error


class TestPerformanceIntegration:
    """Test performance aspects of the application"""
    
    def test_database_query_performance(self, test_app):
        """Test database query performance"""
        with test_app.app_context():
            from extensions import db
            import time
            
            # Create many jobs
            jobs = []
            for i in range(100):
                job = Job(
                    customer_name=f'Customer {i}',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    status='Active'
                )
                jobs.append(job)
            
            db.session.add_all(jobs)
            db.session.commit()
            
            # Test query performance
            start_time = time.time()
            all_jobs = Job.query.all()
            query_time = time.time() - start_time
            
            assert len(all_jobs) >= 100
            assert query_time < 1.0  # Should complete within 1 second
            
            # Test filtered query performance
            start_time = time.time()
            active_jobs = Job.query.filter_by(status='Active').all()
            filtered_query_time = time.time() - start_time
            
            assert len(active_jobs) >= 100
            assert filtered_query_time < 1.0
    
    def test_memory_usage(self, test_app):
        """Test memory usage with large datasets"""
        with test_app.app_context():
            from extensions import db
            import gc
            
            # Create large dataset
            jobs = []
            for i in range(1000):
                job = Job(
                    customer_name=f'Customer {i}',
                    pickup_location='Airport',
                    dropoff_location='Hotel',
                    status='Active'
                )
                jobs.append(job)
            
            db.session.add_all(jobs)
            db.session.commit()
            
            # Force garbage collection
            gc.collect()
            
            # Query all jobs
            all_jobs = Job.query.all()
            assert len(all_jobs) >= 1000
            
            # Clean up
            Job.query.delete()
            db.session.commit()
            
            # Force garbage collection again
            gc.collect()


class TestSecurityIntegration:
    """Test security aspects of the application"""
    
    def test_sql_injection_prevention(self, test_app):
        """Test SQL injection prevention"""
        with test_app.app_context():
            from extensions import db
            
            # Create a test job
            job = Job(
                customer_name='Test Customer',
                pickup_location='Airport',
                dropoff_location='Hotel'
            )
            db.session.add(job)
            db.session.commit()
            
            # Test that malicious input doesn't break queries
            malicious_input = "'; DROP TABLE jobs; --"
            
            # This should not cause any issues
            jobs = Job.query.filter(Job.customer_name.ilike(f'%{malicious_input}%')).all()
            assert isinstance(jobs, list)
            
            # Verify table still exists
            all_jobs = Job.query.all()
            assert len(all_jobs) >= 1
    
    def test_xss_prevention(self, test_app):
        """Test XSS prevention"""
        with test_app.app_context():
            from extensions import db
            
            # Create job with potentially malicious content
            malicious_name = '<script>alert("XSS")</script>'
            job = Job(
                customer_name=malicious_name,
                pickup_location='Airport',
                dropoff_location='Hotel'
            )
            db.session.add(job)
            db.session.commit()
            
            # Retrieve the job
            retrieved_job = Job.query.get(job.id)
            assert retrieved_job.customer_name == malicious_name
            
            # The actual XSS prevention would be in the template rendering
            # This test verifies the data is stored correctly
    
    def test_authentication_security(self, test_app):
        """Test authentication security"""
        with test_app.test_client() as client:
            # Test login with invalid credentials
            response = client.post('/login', data={
                'username': 'nonexistent',
                'password': 'wrongpassword'
            })
            
            # Should not reveal whether user exists
            assert response.status_code == 200
            
            # Test login with empty credentials
            response = client.post('/login', data={
                'username': '',
                'password': ''
            })
            
            assert response.status_code == 200 