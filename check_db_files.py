#!/usr/bin/env python3
"""
Script to check both database files
"""

import sqlite3
import os

def check_database_files():
    """Check both database files"""
    
    files = ['instance/transPort.db', 'instance/app.db']
    
    for db_file in files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"\n{db_file}: {size} bytes")
            
            if size > 0:
                try:
                    conn = sqlite3.connect(db_file)
                    cursor = conn.cursor()
                    
                    # Get all tables
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    
                    print(f"Tables in {db_file}:")
                    for table in tables:
                        print(f"  - {table[0]}")
                    
                    conn.close()
                except Exception as e:
                    print(f"Error reading {db_file}: {e}")
            else:
                print("File is empty")
        else:
            print(f"{db_file}: File does not exist")

if __name__ == "__main__":
    check_database_files() 