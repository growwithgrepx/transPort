#!/usr/bin/env python3
"""
Test Database Management Utility

This script helps manage the file-based SQLite test database used by tests.
Provides inspection, cleanup, and maintenance capabilities for test databases.

Features:
- List and inspect test databases
- Clean up old/corrupted databases
- Verify database integrity
- Generate test database reports
- Integration with CI/CD pipeline
"""

import os
import sys
import sqlite3
import glob
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# Add parent directory to path to import app models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import app, db
from models.user import User
from models.agent import Agent
from models.driver import Driver
from models.service import Service
from models.vehicle import Vehicle
from models.job import Job
from models.role import Role

class TestDatabaseManager:
    """Manages test database operations"""
    
    def __init__(self, test_dir: str = None):
        self.test_dir = test_dir or os.path.dirname(os.path.dirname(__file__))
        self.db_pattern = os.path.join(self.test_dir, 'test_selenium*.db')
        self.report_dir = os.path.join(self.test_dir, 'reports')
        
        # Ensure reports directory exists
        os.makedirs(self.report_dir, exist_ok=True)
    
    def get_test_db_files(self) -> List[str]:
        """Get all test database files in the tests directory"""
        return glob.glob(self.db_pattern)
    
    def get_database_info(self, db_path: str) -> Dict:
        """Get comprehensive information about a database"""
        if not os.path.exists(db_path):
            return {"error": f"Database not found: {db_path}"}
        
        info = {
            "path": db_path,
            "filename": os.path.basename(db_path),
            "size_bytes": os.path.getsize(db_path),
            "created": datetime.fromtimestamp(os.path.getctime(db_path)),
            "modified": datetime.fromtimestamp(os.path.getmtime(db_path)),
            "tables": [],
            "record_counts": {},
            "integrity_check": None
        }
        
        # Check database integrity
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA integrity_check")
                result = cursor.fetchone()
                info["integrity_check"] = result[0] if result else "Unknown"
        except Exception as e:
            info["integrity_check"] = f"Error: {e}"
        
        # Get table information using SQLAlchemy
        with app.app_context():
            original_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            
            try:
                inspector = db.inspect(db.engine)
                info["tables"] = inspector.get_table_names()
                
                # Count records in each table
                tables = [User, Agent, Driver, Service, Vehicle, Job, Role]
                for table in tables:
                    try:
                        count = table.query.count()
                        info["record_counts"][table.__name__] = count
                    except Exception as e:
                        info["record_counts"][table.__name__] = f"Error: {e}"
            except Exception as e:
                info["error"] = f"SQLAlchemy error: {e}"
            finally:
                if original_uri:
                    app.config['SQLALCHEMY_DATABASE_URI'] = original_uri
        
        return info
    
    def inspect_database(self, db_path: str = None, detailed: bool = False) -> None:
        """Inspect the contents of a test database"""
        if db_path is None:
            db_files = self.get_test_db_files()
            if not db_files:
                print("❌ No test databases found")
                return
            db_path = max(db_files, key=os.path.getctime)
        
        info = self.get_database_info(db_path)
        
        if "error" in info:
            print(f"❌ {info['error']}")
            return
        
        print(f"📊 Database Inspection: {info['filename']}")
        print("=" * 70)
        print(f"Path: {info['path']}")
        print(f"Size: {info['size_bytes']:,} bytes")
        print(f"Created: {info['created'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Modified: {info['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Integrity: {info['integrity_check']}")
        print(f"Tables: {', '.join(info['tables']) if info['tables'] else 'None'}")
        
        if info['record_counts']:
            print("\n📋 Record Counts:")
            print("-" * 30)
            for table, count in info['record_counts'].items():
                print(f"  {table}: {count}")
        
        if detailed and info['tables']:
            self._show_detailed_data(db_path)
        
        print("=" * 70)
    
    def _show_detailed_data(self, db_path: str) -> None:
        """Show detailed sample data from the database"""
        with app.app_context():
            original_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
            app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
            
            try:
                print("\n📋 Sample Data:")
                print("-" * 30)
                
                # Users
                try:
                    users = User.query.limit(5).all()
                    if users:
                        print(f"Users ({len(users)}):")
                        for user in users:
                            print(f"  - {user.username} ({user.email}) - Active: {user.active}")
                except Exception as e:
                    print(f"Users: Error - {e}")
                
                # Agents
                try:
                    agents = Agent.query.limit(5).all()
                    if agents:
                        print(f"Agents ({len(agents)}):")
                        for agent in agents:
                            print(f"  - {agent.name} ({agent.email}) - Type: {agent.type}")
                except Exception as e:
                    print(f"Agents: Error - {e}")
                
                # Jobs
                try:
                    jobs = Job.query.limit(5).all()
                    if jobs:
                        print(f"Jobs ({len(jobs)}):")
                        for job in jobs:
                            print(f"  - Job #{job.id}: {job.pickup_location} → {job.dropoff_location}")
                except Exception as e:
                    print(f"Jobs: Error - {e}")
                
            finally:
                if original_uri:
                    app.config['SQLALCHEMY_DATABASE_URI'] = original_uri
    
    def list_databases(self, show_details: bool = False) -> None:
        """List all test database files"""
        db_files = self.get_test_db_files()
        if not db_files:
            print("❌ No test databases found")
            return
        
        print("📁 Test Databases:")
        print("=" * 60)
        
        for db_file in sorted(db_files, key=os.path.getctime, reverse=True):
            if show_details:
                info = self.get_database_info(db_file)
                if "error" not in info:
                    print(f"  {info['filename']}")
                    print(f"    Size: {info['size_bytes']:,} bytes")
                    print(f"    Created: {info['created'].strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"    Integrity: {info['integrity_check']}")
                    print(f"    Tables: {len(info['tables'])}")
                    print()
                else:
                    print(f"  {os.path.basename(db_file)} - {info['error']}")
            else:
                size = os.path.getsize(db_file)
                ctime = os.path.getctime(db_file)
                ctime_str = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M:%S')
                print(f"  {os.path.basename(db_file)} ({size:,} bytes) - Created: {ctime_str}")
    
    def cleanup_old_databases(self, days_old: int = 7) -> None:
        """Remove test databases older than specified days"""
        db_files = self.get_test_db_files()
        if not db_files:
            print("ℹ️  No test databases found")
            return
        
        cutoff_time = datetime.now() - timedelta(days=days_old)
        old_files = []
        
        for db_file in db_files:
            if datetime.fromtimestamp(os.path.getctime(db_file)) < cutoff_time:
                old_files.append(db_file)
        
        if not old_files:
            print(f"ℹ️  No databases older than {days_old} days found")
            return
        
        print(f"🗑️  Removing {len(old_files)} database(s) older than {days_old} days:")
        for db_file in old_files:
            try:
                os.remove(db_file)
                print(f"  ✅ Removed: {os.path.basename(db_file)}")
            except Exception as e:
                print(f"  ❌ Failed to remove {os.path.basename(db_file)}: {e}")
    
    def cleanup_all_databases(self) -> None:
        """Remove all test database files"""
        db_files = self.get_test_db_files()
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
    
    def generate_report(self, output_format: str = 'json') -> None:
        """Generate a comprehensive report of all test databases"""
        db_files = self.get_test_db_files()
        if not db_files:
            print("❌ No test databases found for report generation")
            return
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_databases": len(db_files),
            "databases": []
        }
        
        for db_file in db_files:
            info = self.get_database_info(db_file)
            report["databases"].append(info)
        
        # Calculate summary statistics
        total_size = sum(info.get('size_bytes', 0) for info in report["databases"] if 'error' not in info)
        report["summary"] = {
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "average_size_bytes": total_size // len(db_files) if db_files else 0
        }
        
        if output_format == 'json':
            report_file = os.path.join(self.report_dir, f"test_db_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            print(f"📊 Report generated: {report_file}")
        else:
            # Print to console
            print("📊 Test Database Report")
            print("=" * 50)
            print(f"Generated: {report['generated_at']}")
            print(f"Total databases: {report['total_databases']}")
            print(f"Total size: {report['summary']['total_size_mb']} MB")
            print()
            
            for db_info in report["databases"]:
                if "error" not in db_info:
                    print(f"  {db_info['filename']}")
                    print(f"    Size: {db_info['size_bytes']:,} bytes")
                    print(f"    Tables: {len(db_info['tables'])}")
                    print(f"    Integrity: {db_info['integrity_check']}")
                    print()
    
    def verify_database_integrity(self, db_path: str = None) -> bool:
        """Verify the integrity of a test database"""
        if db_path is None:
            db_files = self.get_test_db_files()
            if not db_files:
                print("❌ No test databases found")
                return False
            db_path = max(db_files, key=os.path.getctime)
        
        info = self.get_database_info(db_path)
        
        if "error" in info:
            print(f"❌ Database error: {info['error']}")
            return False
        
        print(f"🔍 Verifying database: {info['filename']}")
        
        # Check file integrity
        if info['integrity_check'] != 'ok':
            print(f"❌ Database integrity check failed: {info['integrity_check']}")
            return False
        
        # Check if database has expected tables
        expected_tables = ['user', 'agent', 'driver', 'service', 'vehicle', 'job', 'role']
        missing_tables = [table for table in expected_tables if table not in info['tables']]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
            return False
        
        print("✅ Database integrity verified")
        return True

def main():
    """Main entry point with improved argument parsing"""
    parser = argparse.ArgumentParser(
        description="Test Database Management Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage_test_db.py list                    # List all databases
  python manage_test_db.py list --detailed         # List with details
  python manage_test_db.py inspect                 # Inspect most recent database
  python manage_test_db.py inspect --detailed      # Inspect with sample data
  python manage_test_db.py inspect test_selenium_abc123.db  # Inspect specific database
  python manage_test_db.py cleanup                 # Remove all databases
  python manage_test_db.py cleanup --days 3        # Remove databases older than 3 days
  python manage_test_db.py report                  # Generate JSON report
  python manage_test_db.py report --format text    # Generate text report
  python manage_test_db.py verify                  # Verify database integrity
        """
    )
    
    parser.add_argument('command', choices=[
        'list', 'inspect', 'cleanup', 'report', 'verify'
    ], help='Command to execute')
    
    parser.add_argument('database', nargs='?', help='Specific database file to operate on')
    parser.add_argument('--detailed', action='store_true', help='Show detailed information')
    parser.add_argument('--days', type=int, default=7, help='Days threshold for cleanup (default: 7)')
    parser.add_argument('--format', choices=['json', 'text'], default='json', help='Report format (default: json)')
    
    args = parser.parse_args()
    
    manager = TestDatabaseManager()
    
    try:
        if args.command == 'list':
            manager.list_databases(show_details=args.detailed)
        elif args.command == 'inspect':
            manager.inspect_database(args.database, detailed=args.detailed)
        elif args.command == 'cleanup':
            if args.days == 0:
                manager.cleanup_all_databases()
            else:
                manager.cleanup_old_databases(args.days)
        elif args.command == 'report':
            manager.generate_report(args.format)
        elif args.command == 'verify':
            manager.verify_database_integrity(args.database)
    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 