import sqlite3

DB_PATH = 'instance/app.db'

COLUMNS_TO_ADD = [
    ('name', 'VARCHAR(128)'),
    ('amount', 'FLOAT'),
    ('discount_type', 'VARCHAR(32)'),
    ('is_base_discount', 'BOOLEAN'),
    ('is_active', 'BOOLEAN'),
    ('valid_from', 'VARCHAR(32)'),
    ('valid_to', 'VARCHAR(32)'),
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
    for column, coltype in COLUMNS_TO_ADD:
        if not column_exists(cursor, 'discount', column):
            add_column(cursor, 'discount', column, coltype)
        else:
            print(f"Column '{column}' already exists in 'discount'.")
    conn.commit()
    conn.close()
    print("\nSchema update complete.")

if __name__ == '__main__':
    main() 