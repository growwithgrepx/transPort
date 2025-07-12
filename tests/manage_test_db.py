#!/usr/bin/env python3
"""
Test Database Management Utility

This script helps manage the file-based SQLite test database used by Selenium tests.
"""

import os
import sys
import sqlite3
import glob
from pathlib import Path

# Add parent directory to path to import app models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from models.user import User
from models.agent import Agent
from models.driver import Driver
from models.service import Service
from models.vehicle import Vehicle
from models.job import Job
from models.role import Role

def get_test_db_files():
    """Get all test database files in the tests directory"""
    test_dir = os.path.dirname(__file__)
    pattern = os.path.join(test_dir, 'test_selenium*.db')
    return glob.glob(pattern)

def inspect_database(db_path=None):
    """Inspect the contents of the test database"""
    if db_path is None:
        # Use the most recent test database
        db_files = get_test_db_files()
        if not db_files:
            print("❌ No test databases found")
            return
        db_path = max(db_files, key=os.path.getctime)
    
    if not os.path.exists(db_path):
        print(f"❌ Test database not found: {db_path}")
        return
    
    print(f"📊 Inspecting test database: {db_path}")
    print("=" * 60)
    
    with app.app_context():
        # Temporarily set the database URI
        original_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        
        try:
            # Check file size
            size = os.path.getsize(db_path)
            print(f"Database size: {size:,} bytes")
            
            # Check if tables exist
            try:
                # Try to get table names from the database
                inspector = db.inspect(db.engine)
                table_names = inspector.get_table_names()
                print(f"Tables found: {', '.join(table_names) if table_names else 'None'}")
                
                if not table_names:
                    print("⚠️  No tables found in database - it may be empty or not initialized")
                    return
                
            except Exception as e:
                print(f"⚠️  Error checking tables: {e}")
                return
            
            # Count records in each table
            tables = [User, Agent, Driver, Service, Vehicle, Job, Role]
            for table in tables:
                try:
                    count = table.query.count()
                    print(f"{table.__name__}: {count} records")
                except Exception as e:
                    print(f"{table.__name__}: Error - {e}")
            
            # Show sample data
            print("\n📋 Sample Data:")
            print("-" * 30)
            
            # Users
            try:
                users = User.query.all()
                if users:
                    print(f"Users ({len(users)}):")
                    for user in users:
                        print(f"  - {user.username} ({user.email}) - Active: {user.active}")
            except Exception as e:
                print(f"Users: Error - {e}")
            
            # Agents
            try:
                agents = Agent.query.all()
                if agents:
                    print(f"Agents ({len(agents)}):")
                    for agent in agents:
                        print(f"  - {agent.name} ({agent.email}) - Type: {agent.type}")
            except Exception as e:
                print(f"Agents: Error - {e}")
            
            # Jobs
            try:
                jobs = Job.query.all()
                if jobs:
                    print(f"Jobs ({len(jobs)}):")
                    for job in jobs:
                        print(f"  - Job #{job.id}: {job.pickup_location} → {job.dropoff_location}")
            except Exception as e:
                print(f"Jobs: Error - {e}")
            
            print("=" * 60)
        finally:
            # Restore original URI
            if original_uri:
                app.config['SQLALCHEMY_DATABASE_URI'] = original_uri

def list_databases():
    """List all test database files"""
    db_files = get_test_db_files()
    if not db_files:
        print("❌ No test databases found")
        return
    
    print("📁 Test Databases:")
    print("=" * 40)
    for db_file in sorted(db_files, key=os.path.getctime, reverse=True):
        size = os.path.getsize(db_file)
        ctime = os.path.getctime(db_file)
        from datetime import datetime
        ctime_str = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {os.path.basename(db_file)} ({size:,} bytes) - Created: {ctime_str}")

def cleanup_all_databases():
    """Remove all test database files"""
    db_files = get_test_db_files()
    if not db_files:
        print("ℹ️  No test databases found to clean up")
        return
    
    print(f"🗑️  Removing {len(db_files)} test database(s):")
    for db_file in db_files:
        try:
            os.remove(db_file)
            print(f"  ✅ Removed: {os.path.basename(db_file)}")
        except Exception as e:
            print(f"  ❌ Failed to remove {os.path.basename(db_file)}: {e}")

def show_help():
    """Show help information"""
    print("""
🔧 Test Database Management Utility

Usage: python manage_test_db.py [command]

Commands:
  list      - List all test database files
  inspect   - Show contents of the most recent test database
  inspect <file> - Show contents of specific database file
  cleanup   - Remove all test database files
  help      - Show this help message

Examples:
  python manage_test_db.py list              # View all test databases
  python manage_test_db.py inspect           # View most recent database
  python manage_test_db.py inspect test_selenium_abc123.db  # View specific database
  python manage_test_db.py cleanup           # Remove all test databases
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        list_databases()
    elif command == 'inspect':
        db_path = sys.argv[2] if len(sys.argv) > 2 else None
        inspect_database(db_path)
    elif command == 'cleanup':
        cleanup_all_databases()
    elif command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == '__main__':
    main() 