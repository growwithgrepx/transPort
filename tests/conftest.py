import os
import sys

# --- ROOT CAUSE FIX: Always use a single, deterministic file-based SQLite DB for all Selenium tests ---
TEST_DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'test_selenium.db'))
SQLITE_URI = f'sqlite:///{TEST_DB_PATH}?check_same_thread=False'
os.environ['DATABASE_URL'] = SQLITE_URI
os.environ['FLASK_ENV'] = 'test'
# Remove the DB file at the start of the session for a clean slate
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import threading
import time
import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask
from app import app as flask_app, db
from werkzeug.serving import make_server
from selenium.webdriver.chrome.service import Service as ChromeService
from models.user import User
from models.role import Role
import uuid
from models.agent import Agent
from models.driver import Driver
from models.service import Service
from models.vehicle import Vehicle
from models.discount import Discount
from models.price import Price
from models.customer_discount import CustomerDiscount
from models.billing import Billing
from sqlalchemy.exc import IntegrityError

# Configure logging for tests
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Global variable to store seeded data
_seeded_data = None

# --- Flask app and DB fixtures ---
@pytest.fixture(scope='session')
def test_app():
    flask_app.config.update({
        'SQLALCHEMY_DATABASE_URI': SQLITE_URI,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    with flask_app.app_context():
        try:
            db.create_all()
            logger.info(f"Created new test database: {TEST_DB_PATH}")
            
            # --- SEED ALL TEST DATA BEFORE SERVER STARTS ---
            global _seeded_data
            _seeded_data = seed_test_data()
            logger.info("All test data seeded successfully")
            
            yield flask_app
        finally:
            db.session.remove()
            db.engine.dispose()
            logger.info(f"Test database preserved at: {TEST_DB_PATH}")

def seed_test_data():
    """Seed all test data - called once before server starts"""
    # Role (get or create)
    role = Role.query.filter_by(name='fleet_manager').first()
    if not role:
        role = Role(name='fleet_manager', description='Fleet Manager')
        db.session.add(role)
        db.session.commit()
    
    # User
    user = User.query.filter_by(username='fleetmanager').first()
    if not user:
        user = User(
            username='fleetmanager',
            email='fleetmanager@example.com',
            password='manager123',
            active=True,
            fs_uniquifier=str(uuid.uuid4())
        )
        user.roles.append(role)
        db.session.add(user)
    else:
        # Always set password and active status for test
        user.password = 'manager123'
        user.active = True
        if role not in user.roles:
            user.roles.append(role)
    db.session.commit()
    logger.info(f"Test user: {user.username}, password: {user.password}, active: {user.active}")
    
    # Agent
    agent = Agent.query.filter_by(name='Test Agent').first()
    if not agent:
        agent = Agent(name='Test Agent', email='agent@example.com', mobile='12345678', type='Corporate', status='Active')
        db.session.add(agent)
    
    # Driver
    driver = Driver.query.filter_by(name='Test Driver').first()
    if not driver:
        driver = Driver(name='Test Driver', phone='87654321')
        db.session.add(driver)
    
    # Service
    service = Service.query.filter_by(name='Test Service').first()
    if not service:
        service = Service(name='Test Service', description='A test service', status='Active')
        db.session.add(service)
    
    # Vehicle
    vehicle = Vehicle.query.filter_by(number='TEST123').first()
    if not vehicle:
        vehicle = Vehicle(name='Test Vehicle', number='TEST123', type='Van', status='Active')
        db.session.add(vehicle)
    
    db.session.commit()
    
    # Price (for service)
    price = Price.query.filter_by(service_id=service.id).first()
    if not price:
        price = Price(service_id=service.id, amount=100.0, currency='USD')
        db.session.add(price)
    
    # Discount
    discount = Discount.query.filter_by(code='TEST10').first()
    if not discount:
        discount = Discount(code='TEST10', percent=10.0)
        db.session.add(discount)
    
    db.session.commit()
    
    # CustomerDiscount (agent-discount)
    customer_discount = CustomerDiscount.query.filter_by(customer_id=agent.id, discount_id=discount.id).first()
    if not customer_discount:
        customer_discount = CustomerDiscount(customer_id=agent.id, discount_id=discount.id, valid_from=None, valid_to=None)
        db.session.add(customer_discount)
    
    db.session.commit()
    
    # Log all users in the DB for debug
    all_users = User.query.all()
    logger.info(f"All users in test DB before test: {[{'username': u.username, 'password': u.password, 'active': u.active} for u in all_users]}")
    
    return {
        'db': db,
        'agent': agent,
        'driver': driver,
        'service': service,
        'vehicle': vehicle,
        'user': user,
        'role': role,
        'price': price,
        'discount': discount,
        'customer_discount': customer_discount
    }

@pytest.fixture(scope='function')
def seeded_db(test_app):
    """Provide references to seeded data - no DB mutations"""
    global _seeded_data
    if _seeded_data is None:
        raise RuntimeError("Test data not seeded. Ensure test_app fixture runs first.")
    
    # Return references to the seeded objects
    yield _seeded_data
    logger.info("Test data preserved in database for debugging")

@pytest.fixture(scope='function')
def clean_db(test_app):
    """Clean database between tests to avoid constraint violations"""
    with test_app.app_context():
        # Clear all data except the seeded data
        from models.user import User
        from models.job import Job
        from models.role import Role
        
        # Delete all users except the seeded one
        User.query.filter(User.username != 'fleetmanager').delete()
        
        # Delete all jobs
        Job.query.delete()
        
        # Delete all roles except the seeded one
        Role.query.filter(Role.name != 'fleet_manager').delete()
        
        db.session.commit()
        yield

# --- Live server fixture ---
@pytest.fixture(scope='session')
def live_server(test_app):
    port = 5001
    server = make_server('127.0.0.1', port, test_app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    # Health check
    import requests
    for _ in range(10):
        try:
            r = requests.get(f'http://127.0.0.1:{port}/')
            if r.status_code < 500:
                break
        except Exception:
            time.sleep(0.5)
    else:
        server.shutdown()
        raise RuntimeError('Test server failed to start')
    yield f'http://127.0.0.1:{port}'
    server.shutdown()

# --- Selenium browser fixture ---
@pytest.fixture(scope='session')
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    driver = None
    try:
        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        yield driver
    finally:
        if driver:
            driver.quit()

@pytest.fixture(autouse=True)
def cleanup_session(browser):
    yield
    try:
        browser.delete_all_cookies()
        browser.execute_script("window.localStorage.clear();")
        browser.execute_script("window.sessionStorage.clear();")
    except Exception:
        pass  # Ignore cleanup errors 