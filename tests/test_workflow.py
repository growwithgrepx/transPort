#!/usr/bin/env python3
"""
Test script to verify workflow components work locally
"""

import os
import sys
import subprocess
from pathlib import Path

def test_pytest_unit():
    """Test that pytest can run unit tests"""
    print("🧪 Testing pytest unit tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "unit/test_models.py::test_user_model",
            "--junitxml=test_results/unit-test-results.xml",
            "-v"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Unit tests passed")
            return True
        else:
            print(f"❌ Unit tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running unit tests: {e}")
        return False

def test_pytest_selenium():
    """Test that pytest can run selenium tests"""
    print("🌐 Testing pytest selenium tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "selenium_tests/test_smoke.py",
            "--junitxml=test_results/selenium-test-results.xml",
            "-v"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Selenium tests passed")
            return True
        else:
            print(f"❌ Selenium tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running selenium tests: {e}")
        return False

def test_database_management():
    """Test database management utility"""
    print("🗄️ Testing database management...")
    
    try:
        # Set environment variable
        env = os.environ.copy()
        env['DATABASE_URL'] = 'sqlite:///test_selenium.db'
        
        result = subprocess.run([
            sys.executable, "manage_test_db.py", "list"
        ], capture_output=True, text=True, cwd=Path(__file__).parent, env=env)
        
        if result.returncode == 0:
            print("✅ Database management works")
            return True
        else:
            print(f"❌ Database management failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running database management: {e}")
        return False

def test_test_runner():
    """Test the custom test runner"""
    print("🏃 Testing custom test runner...")
    
    try:
        # Set environment variable
        env = os.environ.copy()
        env['DATABASE_URL'] = 'sqlite:///test_selenium.db'
        
        result = subprocess.run([
            sys.executable, "config/run_tests.py", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).parent, env=env)
        
        if result.returncode == 0:
            print("✅ Custom test runner works")
            return True
        else:
            print(f"❌ Custom test runner failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running custom test runner: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing workflow components...")
    print("=" * 50)
    
    # Create test_results directory
    test_results_dir = Path(__file__).parent / "test_results"
    test_results_dir.mkdir(exist_ok=True)
    
    results = []
    
    # Test each component
    results.append(("Unit Tests", test_pytest_unit()))
    results.append(("Selenium Tests", test_pytest_selenium()))
    results.append(("Database Management", test_database_management()))
    results.append(("Custom Test Runner", test_test_runner()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All workflow components are working!")
        return 0
    else:
        print("⚠️ Some components need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 