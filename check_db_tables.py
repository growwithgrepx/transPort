#!/usr/bin/env python3
"""
Script to check database tables and their structure
"""

import sqlite3

DB_PATH = 'instance/app.db'

def print_table_schema(table_name):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f'PRAGMA table_info({table_name})')
    columns = cursor.fetchall()
    print(f"\nSchema for table '{table_name}':")
    if columns:
        for col in columns:
            print(f"  {col[1]} ({col[2]})")
    else:
        print("  [Table does not exist]")
    conn.close()

if __name__ == '__main__':
    print_table_schema('job')
    print_table_schema('discount')
    print_table_schema('billing') 