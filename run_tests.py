#!/usr/bin/env python3
"""
Main test runner script for TransPort Flask Application

This script delegates to the tests/config/run_tests.py script to maintain
clean separation of test-related files within the tests directory.

Usage:
    python run_tests.py [options]
    
Examples:
    python run_tests.py --unit
    python run_tests.py --selenium
    python run_tests.py --all
    python run_tests.py --coverage
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Main entry point for test execution"""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    
    # Path to the actual test runner
    test_runner = script_dir / "tests" / "config" / "run_tests.py"
    
    if not test_runner.exists():
        print(f"❌ Error: Test runner not found at {test_runner}")
        print("Please ensure tests/config/run_tests.py exists")
        sys.exit(1)
    
    # Change to the project root directory
    os.chdir(script_dir)
    
    # Build the command to run the test runner
    cmd = [sys.executable, str(test_runner)] + sys.argv[1:]
    
    try:
        # Run the test runner with all arguments passed through
        result = subprocess.run(cmd, check=False)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 