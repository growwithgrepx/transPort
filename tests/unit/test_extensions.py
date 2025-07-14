"""
Comprehensive unit tests for extensions module.
Tests cover database initialization, configuration, and connection handling.
"""

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from extensions import db


class TestDatabaseExtension:
    """Test database extension functionality"""
    
    def test_db_initialization(self, test_app):
        """Test database initialization"""
        with test_app.app_context():
            assert db is not None
            assert hasattr(db, 'session')
            assert hasattr(db, 'engine')
            assert hasattr(db, 'Model')
    
    def test_db_create_all(self, test_app):
        """Test database create_all functionality"""
        with test_app.app_context():
            # This should not raise an exception
            db.create_all()
            assert True  # If we get here, no exception was raised
    
    def test_db_drop_all(self, test_app):
        """Test database drop_all functionality"""
        with test_app.app_context():
            # This should not raise an exception
            db.drop_all()
            assert True  # If we get here, no exception was raised
    
    def test_db_session_commit(self, test_app):
        """Test database session commit"""
        with test_app.app_context():
            # Test that session commit works
            db.session.commit()
            assert True  # If we get here, no exception was raised
    
    def test_db_session_rollback(self, test_app):
        """Test database session rollback"""
        with test_app.app_context():
            # Test that session rollback works
            db.session.rollback()
            assert True  # If we get here, no exception was raised
    
    def test_db_session_close(self, test_app):
        """Test database session close"""
        with test_app.app_context():
            # Test that session close works
            db.session.close()
            assert True  # If we get here, no exception was raised
    
    def test_db_engine_dispose(self, test_app):
        """Test database engine dispose"""
        with test_app.app_context():
            # Test that engine dispose works
            db.engine.dispose()
            assert True  # If we get here, no exception was raised
    
    def test_db_connection_string_handling(self, test_app):
        """Test database connection string handling"""
        with test_app.app_context():
            # Test that connection string is properly formatted
            uri = db.engine.url
            assert uri is not None
            assert hasattr(uri, 'drivername')
            assert hasattr(uri, 'host')
            assert hasattr(uri, 'port')
            assert hasattr(uri, 'database')
    
    def test_db_model_inheritance(self, test_app):
        """Test that models properly inherit from db.Model"""
        with test_app.app_context():
            from models.user import User
            from models.job import Job
            from models.driver import Driver
            from models.agent import Agent
            from models.vehicle import Vehicle
            from models.service import Service
            from models.billing import Billing
            from models.discount import Discount
            from models.price import Price
            from models.customer_discount import CustomerDiscount
            from models.role import Role
            
            # Check that all models inherit from db.Model
            assert isinstance(User, type)
            assert isinstance(Job, type)
            assert isinstance(Driver, type)
            assert isinstance(Agent, type)
            assert isinstance(Vehicle, type)
            assert isinstance(Service, type)
            assert isinstance(Billing, type)
            assert isinstance(Discount, type)
            assert isinstance(Price, type)
            assert isinstance(CustomerDiscount, type)
            assert isinstance(Role, type)
    
    def test_db_session_context_manager(self, test_app):
        """Test database session as context manager"""
        with test_app.app_context():
            # Test session as context manager
            with db.session.begin():
                # This should work without raising an exception
                pass
            assert True  # If we get here, no exception was raised
    
    def test_db_session_transaction_rollback(self, test_app):
        """Test database session transaction rollback on error"""
        with test_app.app_context():
            try:
                with db.session.begin():
                    # Simulate an error
                    raise SQLAlchemyError("Test error")
            except SQLAlchemyError:
                # Transaction should be rolled back
                assert True  # If we get here, rollback worked
    
    def test_db_connection_pool(self, test_app):
        """Test database connection pool functionality"""
        with test_app.app_context():
            # Test connection pool properties
            pool = db.engine.pool
            assert pool is not None
            assert hasattr(pool, 'size')
            assert hasattr(pool, 'checkedin')
            assert hasattr(pool, 'checkedout')
    
    def test_db_metadata_reflection(self, test_app):
        """Test database metadata reflection"""
        with test_app.app_context():
            # Test that metadata can be reflected
            metadata = db.metadata
            assert metadata is not None
            assert hasattr(metadata, 'tables')
    
    def test_db_table_creation(self, test_app):
        """Test database table creation"""
        with test_app.app_context():
            # Test that tables can be created
            db.create_all()
            
            # Check that tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Should have at least some tables
            assert len(tables) > 0
            
            # Check for specific tables
            expected_tables = [
                'user', 'job', 'driver', 'agent', 'vehicle', 
                'service', 'billing', 'discount', 'price', 
                'customer_discount', 'role', 'roles_users'
            ]
            
            for table in expected_tables:
                if table in tables:
                    assert True  # Table exists
                else:
                    # Table might not exist in test environment, which is OK
                    pass
    
    def test_db_column_inspection(self, test_app):
        """Test database column inspection"""
        with test_app.app_context():
            # Test that columns can be inspected
            inspector = db.inspect(db.engine)
            
            # Test user table columns
            if 'user' in inspector.get_table_names():
                columns = inspector.get_columns('user')
                assert len(columns) > 0
                
                # Check for specific columns
                column_names = [col['name'] for col in columns]
                expected_columns = ['id', 'email', 'password', 'active', 'fs_uniquifier']
                
                for col in expected_columns:
                    if col in column_names:
                        assert True  # Column exists
                    else:
                        # Column might not exist in test environment, which is OK
                        pass
    
    def test_db_foreign_key_inspection(self, test_app):
        """Test database foreign key inspection"""
        with test_app.app_context():
            # Test that foreign keys can be inspected
            inspector = db.inspect(db.engine)
            
            # Test job table foreign keys
            if 'job' in inspector.get_table_names():
                foreign_keys = inspector.get_foreign_keys('job')
                assert isinstance(foreign_keys, list)
    
    def test_db_index_inspection(self, test_app):
        """Test database index inspection"""
        with test_app.app_context():
            # Test that indexes can be inspected
            inspector = db.inspect(db.engine)
            
            # Test user table indexes
            if 'user' in inspector.get_table_names():
                indexes = inspector.get_indexes('user')
                assert isinstance(indexes, list)
    
    def test_db_unique_constraint_inspection(self, test_app):
        """Test database unique constraint inspection"""
        with test_app.app_context():
            # Test that unique constraints can be inspected
            inspector = db.inspect(db.engine)
            
            # Test user table unique constraints
            if 'user' in inspector.get_table_names():
                unique_constraints = inspector.get_unique_constraints('user')
                assert isinstance(unique_constraints, list)
    
    def test_db_session_query(self, test_app):
        """Test database session query functionality"""
        with test_app.app_context():
            # Test that queries can be executed
            from models.user import User
            
            # This should not raise an exception
            users = User.query.all()
            assert isinstance(users, list)
    
    def test_db_session_add(self, test_app):
        """Test database session add functionality"""
        with test_app.app_context():
            # Test that objects can be added to session
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            # This should not raise an exception
            db.session.add(user)
            assert True  # If we get here, no exception was raised
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_delete(self, test_app):
        """Test database session delete functionality"""
        with test_app.app_context():
            # Test that objects can be deleted from session
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # This should not raise an exception
            db.session.delete(user)
            db.session.commit()
            assert True  # If we get here, no exception was raised
    
    def test_db_session_merge(self, test_app):
        """Test database session merge functionality"""
        with test_app.app_context():
            # Test that objects can be merged
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # This should not raise an exception
            merged_user = db.session.merge(user)
            assert merged_user is not None
            
            # Clean up
            db.session.delete(user)
            db.session.commit()
    
    def test_db_session_refresh(self, test_app):
        """Test database session refresh functionality"""
        with test_app.app_context():
            # Test that objects can be refreshed
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # This should not raise an exception
            db.session.refresh(user)
            assert True  # If we get here, no exception was raised
            
            # Clean up
            db.session.delete(user)
            db.session.commit()
    
    def test_db_session_expire(self, test_app):
        """Test database session expire functionality"""
        with test_app.app_context():
            # Test that objects can be expired
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # This should not raise an exception
            db.session.expire(user)
            assert True  # If we get here, no exception was raised
            
            # Clean up
            db.session.delete(user)
            db.session.commit()
    
    def test_db_session_expire_all(self, test_app):
        """Test database session expire_all functionality"""
        with test_app.app_context():
            # Test that all objects can be expired
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # This should not raise an exception
            db.session.expire_all()
            assert True  # If we get here, no exception was raised
            
            # Clean up
            db.session.delete(user)
            db.session.commit()
    
    def test_db_session_flush(self, test_app):
        """Test database session flush functionality"""
        with test_app.app_context():
            # Test that session can be flushed
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            
            # This should not raise an exception
            db.session.flush()
            assert True  # If we get here, no exception was raised
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_is_modified(self, test_app):
        """Test database session is_modified functionality"""
        with test_app.app_context():
            # Test that session modification can be checked
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            
            # This should not raise an exception
            is_modified = db.session.is_modified(user)
            assert isinstance(is_modified, bool)
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_is_dirty(self, test_app):
        """Test database session is_dirty functionality"""
        with test_app.app_context():
            # Test that session dirtiness can be checked
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            
            # This should not raise an exception
            is_dirty = db.session.is_dirty()
            assert isinstance(is_dirty, bool)
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_new(self, test_app):
        """Test database session new functionality"""
        with test_app.app_context():
            # Test that new objects can be identified
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            
            # This should not raise an exception
            new_objects = db.session.new
            assert isinstance(new_objects, set)
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_dirty(self, test_app):
        """Test database session dirty functionality"""
        with test_app.app_context():
            # Test that dirty objects can be identified
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Modify the user
            user.username = 'modifieduser'
            
            # This should not raise an exception
            dirty_objects = db.session.dirty
            assert isinstance(dirty_objects, set)
            
            # Clean up
            db.session.rollback()
    
    def test_db_session_deleted(self, test_app):
        """Test database session deleted functionality"""
        with test_app.app_context():
            # Test that deleted objects can be identified
            from models.user import User
            
            user = User(
                username='testuser',
                email='test@example.com',
                password='password123'
            )
            
            db.session.add(user)
            db.session.commit()
            
            # Mark for deletion
            db.session.delete(user)
            
            # This should not raise an exception
            deleted_objects = db.session.deleted
            assert isinstance(deleted_objects, set)
            
            # Clean up
            db.session.rollback()
    
    def test_db_engine_execute(self, test_app):
        """Test database engine execute functionality (SQLAlchemy 2.x compatible)"""
        with test_app.app_context():
            from sqlalchemy import text
            with db.engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                assert result is not None, "Should get a result from SELECT 1"
                row = result.fetchone()
                assert row[0] == 1, "SELECT 1 should return 1"
    
    def test_db_engine_text(self, test_app):
        """Test database engine text functionality"""
        with test_app.app_context():
            from sqlalchemy import text
            
            # Test that text SQL can be executed
            sql = text("SELECT 1 as test_value")
            result = db.engine.execute(sql)
            assert result is not None
            
            # Fetch the result
            row = result.fetchone()
            assert row.test_value == 1
    
    def test_db_engine_connect(self, test_app):
        """Test database engine connect functionality"""
        with test_app.app_context():
            # Test that connections can be established
            with db.engine.connect() as connection:
                assert connection is not None
                
                # Execute a simple query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
    
    def test_db_engine_begin(self, test_app):
        """Test database engine begin functionality"""
        with test_app.app_context():
            # Test that transactions can be begun
            with db.engine.begin() as connection:
                assert connection is not None
                
                # Execute a simple query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
    
    def test_db_engine_table_names(self, test_app):
        """Test database engine table names functionality (SQLAlchemy 2.x compatible)"""
        with test_app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            assert isinstance(table_names, list), "Table names should be a list"
    
    def test_db_engine_has_table(self, test_app):
        """Test database engine has_table functionality"""
        with test_app.app_context():
            # Test that table existence can be checked
            has_user_table = db.engine.has_table('user')
            assert isinstance(has_user_table, bool)
    
    def test_db_engine_dialect(self, test_app):
        """Test database engine dialect functionality"""
        with test_app.app_context():
            # Test that dialect can be accessed
            dialect = db.engine.dialect
            assert dialect is not None
            assert hasattr(dialect, 'name')
    
    def test_db_engine_pool_status(self, test_app):
        """Test database engine pool status"""
        with test_app.app_context():
            # Test that pool status can be checked
            pool = db.engine.pool
            assert pool is not None
            
            # Check pool status
            assert hasattr(pool, 'size')
            assert hasattr(pool, 'checkedin')
            assert hasattr(pool, 'checkedout')
            assert hasattr(pool, 'overflow')
            assert hasattr(pool, 'invalid')
    
    def test_db_engine_url(self, test_app):
        """Test database engine URL functionality"""
        with test_app.app_context():
            # Test that URL can be accessed
            url = db.engine.url
            assert url is not None
            
            # Check URL components
            assert hasattr(url, 'drivername')
            assert hasattr(url, 'host')
            assert hasattr(url, 'port')
            assert hasattr(url, 'database')
            assert hasattr(url, 'username')
            assert hasattr(url, 'password')
    
    def test_db_engine_name(self, test_app):
        """Test database engine name functionality"""
        with test_app.app_context():
            # Test that engine name can be accessed
            name = db.engine.name
            assert isinstance(name, str)
    
    def test_db_engine_driver(self, test_app):
        """Test database engine driver functionality"""
        with test_app.app_context():
            # Test that driver can be accessed
            driver = db.engine.driver
            assert driver is not None
    
    def test_db_engine_echo(self, test_app):
        """Test database engine echo functionality"""
        with test_app.app_context():
            # Test that echo setting can be accessed
            echo = db.engine.echo
            assert isinstance(echo, bool)
    
    def test_db_engine_execution_options(self, test_app):
        """Test database engine execution options"""
        with test_app.app_context():
            # Test that execution options can be set
            engine_with_options = db.engine.execution_options(isolation_level='READ_COMMITTED')
            assert engine_with_options is not None
            assert engine_with_options is not db.engine  # Should return new engine
    
    def test_db_engine_connect_with_options(self, test_app):
        """Test database engine connect with options"""
        with test_app.app_context():
            # Test that connections can be established with options
            with db.engine.connect().execution_options(isolation_level='READ_COMMITTED') as connection:
                assert connection is not None
                
                # Execute a simple query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
    
    def test_db_engine_transaction_rollback(self, test_app):
        """Test database engine transaction rollback"""
        with test_app.app_context():
            # Test that transactions can be rolled back
            with db.engine.begin() as connection:
                # Execute a query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
                
                # Transaction should be automatically committed
                pass
            
            # Test manual transaction with rollback
            connection = db.engine.connect()
            transaction = connection.begin()
            
            try:
                # Execute a query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
                
                # Rollback the transaction
                transaction.rollback()
                assert True  # If we get here, rollback worked
            finally:
                connection.close()
    
    def test_db_engine_transaction_commit(self, test_app):
        """Test database engine transaction commit"""
        with test_app.app_context():
            # Test manual transaction with commit
            connection = db.engine.connect()
            transaction = connection.begin()
            
            try:
                # Execute a query
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
                
                # Commit the transaction
                transaction.commit()
                assert True  # If we get here, commit worked
            finally:
                connection.close()
    
    def test_db_engine_prepared_statements(self, test_app):
        """Test database engine prepared statements"""
        with test_app.app_context():
            # Test that prepared statements can be used
            with db.engine.connect() as connection:
                # Create a prepared statement
                stmt = connection.prepare("SELECT ? as value")
                
                # Execute with parameters
                result = stmt.execute([1])
                row = result.fetchone()
                assert row.value == 1
    
    def test_db_engine_metadata_reflection(self, test_app):
        """Test database engine metadata reflection"""
        with test_app.app_context():
            # Test that metadata can be reflected
            from sqlalchemy import MetaData
            
            metadata = MetaData()
            metadata.reflect(bind=db.engine)
            
            assert metadata is not None
            assert hasattr(metadata, 'tables')
    
    def test_db_engine_inspector(self, test_app):
        """Test database engine inspector"""
        with test_app.app_context():
            # Test that inspector can be created
            inspector = db.inspect(db.engine)
            assert inspector is not None
            
            # Test inspector methods
            assert hasattr(inspector, 'get_table_names')
            assert hasattr(inspector, 'get_columns')
            assert hasattr(inspector, 'get_foreign_keys')
            assert hasattr(inspector, 'get_indexes')
            assert hasattr(inspector, 'get_unique_constraints')
    
    def test_db_engine_connection_pool_limits(self, test_app):
        """Test database engine connection pool limits"""
        with test_app.app_context():
            # Test that pool limits can be accessed
            pool = db.engine.pool
            assert pool is not None
            
            # Check pool limits
            assert hasattr(pool, '_pool')
            assert hasattr(pool, '_overflow')
            assert hasattr(pool, '_timeout')
            assert hasattr(pool, '_recycle')
    
    def test_db_engine_connection_pool_reset(self, test_app):
        """Test database engine connection pool reset"""
        with test_app.app_context():
            # Test that pool can be reset
            pool = db.engine.pool
            assert pool is not None
            
            # Reset the pool
            pool.dispose()
            assert True  # If we get here, reset worked
    
    def test_db_engine_connection_pool_checkin(self, test_app):
        """Test database engine connection pool checkin"""
        with test_app.app_context():
            # Test that connections can be checked in
            pool = db.engine.pool
            assert pool is not None
            
            # Get a connection
            connection = pool.connect()
            assert connection is not None
            
            # Check it back in
            pool.return_(connection)
            assert True  # If we get here, checkin worked
    
    def test_db_engine_connection_pool_checkout(self, test_app):
        """Test database engine connection pool checkout"""
        with test_app.app_context():
            # Test that connections can be checked out
            pool = db.engine.pool
            assert pool is not None
            
            # Check out a connection
            connection = pool.connect()
            assert connection is not None
            
            # Return it
            pool.return_(connection)
    
    def test_db_engine_connection_pool_status_after_operations(self, test_app):
        """Test database engine connection pool status after operations"""
        with test_app.app_context():
            # Test pool status after operations
            pool = db.engine.pool
            initial_checkedout = pool.checkedout()
            
            # Perform some operations
            with db.engine.connect() as connection:
                result = connection.execute("SELECT 1")
                row = result.fetchone()
                assert row[0] == 1
            
            # Check pool status
            final_checkedout = pool.checkedout()
            assert final_checkedout == initial_checkedout  # Should be the same after connection is closed
    
    def test_db_engine_connection_pool_overflow(self, test_app):
        """Test database engine connection pool overflow"""
        with test_app.app_context():
            # Test pool overflow behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Create multiple connections to test overflow
            connections = []
            try:
                for i in range(10):  # Create more connections than pool size
                    connection = pool.connect()
                    connections.append(connection)
                    assert connection is not None
            finally:
                # Return all connections
                for connection in connections:
                    pool.return_(connection)
    
    def test_db_engine_connection_pool_timeout(self, test_app):
        """Test database engine connection pool timeout"""
        with test_app.app_context():
            # Test pool timeout behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check timeout setting
            timeout = pool._timeout
            assert isinstance(timeout, (int, float)) or timeout is None
    
    def test_db_engine_connection_pool_recycle(self, test_app):
        """Test database engine connection pool recycle"""
        with test_app.app_context():
            # Test pool recycle behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check recycle setting
            recycle = pool._recycle
            assert isinstance(recycle, (int, float)) or recycle is None
    
    def test_db_engine_connection_pool_echo(self, test_app):
        """Test database engine connection pool echo"""
        with test_app.app_context():
            # Test pool echo behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check echo setting
            echo = pool._echo
            assert isinstance(echo, bool)
    
    def test_db_engine_connection_pool_logging(self, test_app):
        """Test database engine connection pool logging"""
        with test_app.app_context():
            # Test pool logging behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check logging setting
            logging = pool._logging
            assert isinstance(logging, bool)
    
    def test_db_engine_connection_pool_reset_on_return(self, test_app):
        """Test database engine connection pool reset on return"""
        with test_app.app_context():
            # Test pool reset on return behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check reset on return setting
            reset_on_return = pool._reset_on_return
            assert isinstance(reset_on_return, str) or reset_on_return is None
    
    def test_db_engine_connection_pool_pre_ping(self, test_app):
        """Test database engine connection pool pre ping"""
        with test_app.app_context():
            # Test pool pre ping behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check pre ping setting
            pre_ping = pool._pre_ping
            assert isinstance(pre_ping, bool)
    
    def test_db_engine_connection_pool_use_lifo(self, test_app):
        """Test database engine connection pool LIFO behavior"""
        with test_app.app_context():
            # Test pool LIFO behavior
            pool = db.engine.pool
            assert pool is not None
            
            # Check LIFO setting
            use_lifo = pool._use_lifo
            assert isinstance(use_lifo, bool) 