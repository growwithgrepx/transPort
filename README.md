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