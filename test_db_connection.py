import os
from sqlalchemy import create_engine, text

# Load environment variable from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable not set.')

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"Successfully connected to the database!\nPostgreSQL version: {version}")
except Exception as e:
    print(f"Failed to connect to the database: {e}") 