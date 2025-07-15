# transPort Admin Portal

This is a Flask-based admin portal to manage jobs, drivers, agents, billing, and discounts, replacing the previous Excel workflow.

## Features
- Admin login/logout
- Password reset
- Manage Jobs, Drivers, Agents, Billing, Discounts
- SQLite database
- Bootstrap-based UI (customizable)

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask flask_sqlalchemy werkzeug
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **First time setup:**
   - The database will be created automatically on first run.
   - You may need to manually add an admin user to the database using a Python shell.

## Folder Structure
- `app.py` - Main Flask app
- `models.py` - Database models
- `templates/` - HTML templates
- `static/css/` - Custom CSS

## Customization
- Edit `static/css/style.css` for custom styles.
- Extend templates in `templates/` for new pages or features. 

##  create DB 

(.venv) PS D:\transPort> python -m flask db upgrade

[2025-07-11 13:10:45,857] INFO in app: Transport Admin Portal startup

INFO  [alembic.runtime.migration] Context impl SQLiteImpl.

INFO  [alembic.runtime.migration] Will assume non-transactional DDL.

INFO  [alembic.runtime.migration] Running upgrade  -> 81cc723bc649, Initial migration

INFO  [alembic.runtime.migration] Running upgrade 81cc723bc649 -> 7dfcbd72e186, Rename password_hash to password for Flask-Security compatibility
INFO  [alembic.runtime.migration] Running upgrade 7dfcbd72e186 -> 13c83c53107e, Ensure User model matches Flask-Security-Too requirements
INFO  [alembic.runtime.migration] Running upgrade 13c83c53107e -> 160a19a33cd5, Add permissions column and get_permissions to Role for Flask-Security-Too
INFO  [alembic.runtime.migration] Running upgrade 160a19a33cd5 -> dc024f26d6ba, Add Price and CustomerDiscount models

(.venv) PS D:\transPort> python .\scripts\seed_db.py

[2025-07-11 13:10:56,709] INFO in app: Transport Admin Portal startup

fleetmanager, Password: manager123
sysadmin, Password: sysadmin123
employee1, Password: employee123
accountant1, Password: accountant123
custservice1, Password: custservice123
Sample data inserted successfully.

(.venv) PS D:\transPort> 
