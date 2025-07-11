#!/usr/bin/env python3
"""
Script to manually add missing columns to the database
"""

from app import app, db
import sqlite3

DB_PATH = 'instance/app.db'

BILLING_COLUMNS_TO_ADD = [
    ('invoice_number', 'VARCHAR(128)'),
    ('invoice_date', 'VARCHAR(32)'),
    ('due_date', 'VARCHAR(32)'),
    ('base_price', 'FLOAT'),
    ('base_discount_amount', 'FLOAT'),
    ('agent_discount_amount', 'FLOAT'),
    ('additional_discount_amount', 'FLOAT'),
    ('additional_charges', 'FLOAT'),
    ('subtotal', 'FLOAT'),
    ('tax_amount', 'FLOAT'),
    ('total_amount', 'FLOAT'),
    ('payment_status', 'VARCHAR(32)'),
    ('payment_date', 'VARCHAR(32)'),
    ('payment_method', 'VARCHAR(32)'),
    ('notes', 'TEXT'),
    ('terms_conditions', 'TEXT'),
]

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def add_column(cursor, table, column, coltype):
    print(f"Adding column '{column}' to '{table}'...")
    cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {coltype}")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for column, coltype in BILLING_COLUMNS_TO_ADD:
        if not column_exists(cursor, 'billing', column):
            add_column(cursor, 'billing', column, coltype)
        else:
            print(f"Column '{column}' already exists in 'billing'.")
    conn.commit()
    conn.close()
    print("\nBilling schema update complete.")

if __name__ == '__main__':
    main() 