#!/usr/bin/env python3
"""
Comprehensive test runner for the transport application.
Supports running different types of tests and generating coverage reports.
"""

import os
import sys
import subprocess
import argparse
import time
import json
from datetime import datetime
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"{'='*60}")
    
    start_time = time.time()
    try:
        result = subprocess.run(command, check=True, capture_output=False)
        end_time = time.time()
        print(f"\n✅ {description} completed successfully in {end_time - start_time:.2f} seconds")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False


def get_timestamp():
    """Get current timestamp for report naming"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run_unit_tests():
    """Run unit tests with coverage"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        "../unit/",
        "--cov=app",
        "--cov=models", 
        "--cov=blueprints",
        "--cov=extensions",
        "--cov-report=term-missing",
        "--cov-report=html:../reports/htmlcov/unit",
        "--cov-report=xml:../reports/coverage_unit.xml",
        "--junit-xml=../reports/junit_unit.xml",
        "--cov-fail-under=90",
        "-v",
        "--tb=short"
    ]
    return run_command(command, "Unit Tests")


def run_integration_tests():
    """Run integration tests"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        "../unit/test_integration.py",
        "--junit-xml=../reports/junit_integration.xml",
        "-v",
        "--tb=short"
    ]
    return run_command(command, "Integration Tests")


def run_all_tests():
    """Run all tests with coverage"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        "../",
        "--cov=app",
        "--cov=models",
        "--cov=blueprints", 
        "--cov=extensions",
        "--cov-report=term-missing",
        "--cov-report=html:../reports/htmlcov",
        "--cov-report=xml:../reports/coverage.xml",
        "--junit-xml=../reports/junit.xml",
        "--cov-fail-under=85",
        "-v",
        "--tb=short"
    ]
    return run_command(command, "All Tests")


def run_selenium_tests():
    """Run Selenium tests"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        "../selenium_tests/",
        "--junit-xml=../reports/junit_selenium.xml",
        "-v",
        "--tb=short"
    ]
    return run_command(command, "Selenium Tests")


def run_smoke_tests():
    """Run smoke tests"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        "../",
        "-m", "smoke",
        "--junit-xml=../reports/junit_smoke.xml",
        "-v",
        "--tb=short"
    ]
    return run_command(command, "Smoke Tests")


def run_specific_test(test_path):
    """Run a specific test file or test function"""
    timestamp = get_timestamp()
    command = [
        sys.executable, "-m", "pytest",
        test_path,
        "--junit-xml=../reports/junit_specific.xml",
        "-v",
        "--tb=short"
    ]
    return run_command(command, f"Specific Test: {test_path}")


def generate_coverage_report():
    """Generate a comprehensive coverage report"""
    print(f"\n{'='*60}")
    print("Generating Coverage Report")
    print(f"{'='*60}")
    
    # Create coverage directory if it doesn't exist
    coverage_dir = Path("../reports")
    coverage_dir.mkdir(exist_ok=True)
    
    # Generate HTML report
    command = [
        sys.executable, "-m", "coverage", "html",
        "--directory=../reports/htmlcov",
        "--title=Transport App Coverage Report"
    ]
    success = run_command(command, "HTML Coverage Report")
    
    # Generate XML report
    command = [
        sys.executable, "-m", "coverage", "xml",
        "--output-file=../reports/coverage.xml"
    ]
    success &= run_command(command, "XML Coverage Report")
    
    # Generate text report
    command = [
        sys.executable, "-m", "coverage", "report",
        "--show-missing",
        "--precision=2"
    ]
    success &= run_command(command, "Text Coverage Report")
    
    return success


def generate_test_summary():
    """Generate a JSON summary of test results"""
    timestamp = get_timestamp()
    summary = {
        "timestamp": timestamp,
        "datetime": datetime.now().isoformat(),
        "test_run": {
            "unit_tests": {"status": "unknown", "file": "junit_unit.xml"},
            "integration_tests": {"status": "unknown", "file": "junit_integration.xml"},
            "selenium_tests": {"status": "unknown", "file": "junit_selenium.xml"},
            "coverage": {"file": "coverage.xml"}
        },
        "environment": {
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "platform": sys.platform
        }
    }
    
    # Save summary
    summary_file = Path("../reports/test_summary.json")
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"✅ Test summary saved to {summary_file}")
    return True


def clean_coverage():
    """Clean coverage data"""
    command = [sys.executable, "-m", "coverage", "erase"]
    return run_command(command, "Clean Coverage Data")


def clean_reports():
    """Clean old test reports"""
    reports_dir = Path("../reports")
    if reports_dir.exists():
        # Keep only the latest reports (last 5 runs)
        report_files = list(reports_dir.glob("*.xml")) + list(reports_dir.glob("*.json"))
        report_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove old files (keep latest 5)
        removed_count = 0
        for old_file in report_files[5:]:
            old_file.unlink()
            removed_count += 1
            print(f"🗑️  Removed old report: {old_file.name}")
        
        if removed_count > 0:
            print(f"✅ Cleaned {removed_count} old report files")
        else:
            print("✅ No old reports to clean")
    else:
        print("✅ Reports directory doesn't exist yet")
    
    return True


def manage_test_databases():
    """Manage test databases using the database management utility"""
    print(f"\n{'='*60}")
    print("Managing Test Databases")
    print(f"{'='*60}")
    
    # Import the database manager
    sys.path.insert(0, str(Path(__file__).parent.parent))
    try:
        from utils.manage_test_db import TestDatabaseManager
        manager = TestDatabaseManager()
        
        # List current databases
        print("📁 Current test databases:")
        manager.list_databases()
        
        # Clean up old databases (older than 3 days)
        print("\n🧹 Cleaning up old test databases...")
        manager.cleanup_old_databases(days_old=3)
        
        # Verify database integrity
        print("\n🔍 Verifying database integrity...")
        db_files = manager.get_test_db_files()
        if db_files:
            manager.verify_database_integrity()
        
        # Generate database report
        print("\n📊 Generating database report...")
        manager.generate_report()
        
        return True
    except ImportError as e:
        print(f"❌ Could not import database manager: {e}")
        return False
    except Exception as e:
        print(f"❌ Database management failed: {e}")
        return False


def install_dependencies():
    """Install test dependencies"""
    command = [
        sys.executable, "-m", "pip", "install",
        "pytest",
        "pytest-cov",
        "pytest-flask",
        "factory-boy",
        "coverage"
    ]
    return run_command(command, "Install Test Dependencies")


def check_test_environment():
    """Check if test environment is properly set up"""
    print(f"\n{'='*60}")
    print("Checking Test Environment")
    print(f"{'='*60}")
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check if required packages are installed
    required_packages = [
        "pytest",
        "pytest-cov", 
        "pytest-flask",
        "flask",
        "flask-sqlalchemy",
        "flask-login"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (missing)")
            missing_packages.append(package)
    
    # Check test database configuration
    try:
        # Add the parent directory to sys.path to import tests module
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from tests.conftest import create_test_app
        print("✅ Test database configuration")
    except ImportError as e:
        print(f"❌ Test database configuration: {e}")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: python run_tests.py --install-deps")
        return False
    
    print("\n✅ Test environment is ready")
    return True


def main():
    """Main function to handle command line arguments and run tests"""
    parser = argparse.ArgumentParser(description="Run tests for the transport application")
    parser.add_argument("--unit", action="store_true", help="Run unit tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--selenium", action="store_true", help="Run Selenium tests")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--clean", action="store_true", help="Clean coverage data and old reports")
    parser.add_argument("--install-deps", action="store_true", help="Install test dependencies")
    parser.add_argument("--check-env", action="store_true", help="Check test environment")
    parser.add_argument("--test", type=str, help="Run specific test file or test function")
    parser.add_argument("--manage-db", action="store_true", help="Manage test databases")
    
    args = parser.parse_args()
    
    # Change to the config directory for relative paths to work
    os.chdir(Path(__file__).parent)
    
    success = True
    
    if args.check_env:
        success = check_test_environment()
    elif args.install_deps:
        success = install_dependencies()
    elif args.clean:
        success = clean_coverage() and clean_reports()
    elif args.coverage:
        success = generate_coverage_report()
    elif args.manage_db:
        success = manage_test_databases()
    elif args.unit:
        success = run_unit_tests()
    elif args.integration:
        success = run_integration_tests()
    elif args.selenium:
        success = run_selenium_tests()
    elif args.smoke:
        success = run_smoke_tests()
    elif args.test:
        success = run_specific_test(args.test)
    elif args.all:
        success = run_all_tests()
    else:
        # Default: run all tests
        success = run_all_tests()
    
    # Generate summary if tests were run
    if not any([args.check_env, args.install_deps, args.clean, args.coverage]):
        generate_test_summary()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 All tests completed successfully!")
    else:
        print("❌ Some tests failed!")
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 