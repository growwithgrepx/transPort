#!/usr/bin/env python3
"""
Test Database Management Wrapper

This is a convenience wrapper for the test database management utility.
It calls the main utility located in tests/utils/manage_test_db.py
"""

import sys
import os

# Add the utils directory to the path
utils_dir = os.path.join(os.path.dirname(__file__), 'utils')
sys.path.insert(0, utils_dir)

# Import and run the main utility
from manage_test_db import main

if __name__ == '__main__':
    main() 