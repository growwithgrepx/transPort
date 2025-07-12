import pytest
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .pages.jobs_page import JobsPage
from .pages.login_page import LoginPage
from .utils.screenshot_helper import save_debug_artifacts

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("seeded_db")
def test_jobs_crud(live_server, browser, seeded_db):
    """Test CRUD operations for jobs with improved error handling"""
    
    # Login first
    login_page = LoginPage(browser, live_server)
    login_page.load()
    login_page.login("fleetmanager", "manager123")

    jobs_page = JobsPage(browser, live_server)
    jobs_page.load()

    # Use seeded related objects
    agent = seeded_db['agent']
    driver = seeded_db['driver']
    service = seeded_db['service']
    vehicle = seeded_db['vehicle']

    # --- CREATE ---
    job_data = {
        "agent_name": agent.name,
        "customer_name": agent.name,
        "customer_email": agent.email,
        "customer_mobile": agent.mobile,
        "service_name": service.name,
        "pickup_date": "2025-07-12",
        "pickup_time": "10:00",
        "pickup_location": "Test Pickup Location",
        "dropoff_location": "Test Dropoff Location",
        "vehicle_name": f"{vehicle.name} ({vehicle.number})",
        "driver_name": f"{driver.name} ({driver.phone})",
        "passenger_name": "Test Passenger",
        "passenger_email": "passenger@example.com",
        "passenger_mobile": "99988877",
        # Advanced fields
        "customer_reference": "REF-CRUD-001",
        "payment_mode": "Card",
        "payment_status": "Paid",
        "order_status": "New",
        "message": "Test message for CRUD.",
        "remarks": "Test remarks for CRUD.",
        "has_additional_stop": True,
        "has_request": True,
        "reference": "REF-CRUD-001",
        "status": "Pending"
    }
    
    try:
        logger.info("Starting job creation test...")
        
        # Click Add Job button
        jobs_page.click_add_job()
        
        # Show advanced fields if they exist
        try:
            advanced_fields = browser.find_element(By.ID, "advanced-fields")
            if advanced_fields.value_of_css_property("display") == "none":
                browser.execute_script('document.getElementById("advanced-fields").style.display = "block";')
                time.sleep(0.5)
        except:
            logger.info("Advanced fields section not found or already visible")
        
        # Fill and submit the form
        jobs_page.fill_job_form(job_data)
        jobs_page.submit_job_form()
        
        # Verify job was created
        assert jobs_page.verify_job_created(job_data), "Job creation failed - job not found in list"
        logger.info("Job creation test passed")
        
    except Exception as e:
        logger.error(f"Job creation failed: {e}")
        save_debug_artifacts(browser, "job_create_failure")
        raise

    # --- READ ---
    try:
        logger.info("Starting job read test...")
        
        # Reload the jobs page to ensure fresh data
        jobs_page.load()
        
        assert jobs_page.verify_job_created(job_data), "Job read failed - job not found after creation"
        logger.info("Job read test passed")
        
    except Exception as e:
        logger.error(f"Job read failed: {e}")
        save_debug_artifacts(browser, "job_read_failure")
        raise

    # --- UPDATE ---
    updated_data = job_data.copy()
    updated_data["customer_name"] = "Updated Customer"
    updated_data["remarks"] = "Updated remarks"
    updated_data["status"] = "Completed"
    
    try:
        logger.info("Starting job update test...")
        
        jobs_page.edit_job(updated_data)
        
        assert jobs_page.verify_job_created(updated_data), "Job update failed - updated job not found"
        logger.info("Job update test passed")
        
    except Exception as e:
        logger.error(f"Job update failed: {e}")
        save_debug_artifacts(browser, "job_update_failure")
        raise

    # --- DELETE ---
    try:
        logger.info("Starting job deletion test...")
        
        jobs_page.delete_job(updated_data)
        
        # Wait for deletion to complete
        time.sleep(2)
        
        assert jobs_page.verify_job_deleted(updated_data), "Job deletion failed - job still exists"
        logger.info("Job deletion test passed")
        
    except Exception as e:
        logger.error(f"Job deletion failed: {e}")
        save_debug_artifacts(browser, "job_delete_failure")
        raise

    logger.info("All CRUD tests passed successfully!")


# Additional helper test to debug form issues
@pytest.mark.usefixtures("seeded_db")
def test_job_form_debug(live_server, browser, seeded_db):
    """Debug test to help identify form issues"""
    
    # Login first
    login_page = LoginPage(browser, live_server)
    login_page.load()
    login_page.login("fleetmanager", "manager123")

    jobs_page = JobsPage(browser, live_server)
    jobs_page.load()
    
    # Click Add Job
    jobs_page.click_add_job()
    
    # Wait for form
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, "jobForm")))
    
    # Get form details
    form = browser.find_element(By.ID, "jobForm")
    logger.info(f"Form found: {form.tag_name}")
    
    # Find all form fields
    fields = form.find_elements(By.TAG_NAME, "input")
    fields.extend(form.find_elements(By.TAG_NAME, "select"))
    fields.extend(form.find_elements(By.TAG_NAME, "textarea"))
    
    logger.info(f"Found {len(fields)} form fields:")
    for field in fields:
        field_name = field.get_attribute("name")
        field_type = field.get_attribute("type")
        field_id = field.get_attribute("id")
        logger.info(f"  - {field_name} ({field_type}) [ID: {field_id}]")
    
    # Check for submit button
    submit_buttons = form.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
    logger.info(f"Found {len(submit_buttons)} submit buttons")
    
    for btn in submit_buttons:
        btn_text = btn.text or btn.get_attribute("value")
        btn_id = btn.get_attribute("id")
        logger.info(f"  - Submit button: '{btn_text}' [ID: {btn_id}]")
    
    # Check for advanced fields section
    try:
        advanced_section = browser.find_element(By.ID, "advanced-fields")
        display_style = advanced_section.value_of_css_property("display")
        logger.info(f"Advanced fields section found, display: {display_style}")
    except:
        logger.info("No advanced fields section found")
    
    # Save screenshot for debugging
    save_debug_artifacts(browser, "form_debug")


# Test with minimal data to isolate issues
@pytest.mark.usefixtures("seeded_db")
def test_minimal_job_create(live_server, browser, seeded_db):
    """Test job creation with minimal required fields only"""
    
    # Login first
    login_page = LoginPage(browser, live_server)
    login_page.load()
    login_page.login("fleetmanager", "manager123")

    jobs_page = JobsPage(browser, live_server)
    jobs_page.load()
    
    # Use seeded related objects
    agent = seeded_db['agent']
    service = seeded_db['service']
    
    # Minimal job data - only required fields
    minimal_job_data = {
        "agent_name": agent.name,  # must match datalist
        "service_name": service.name,  # must match datalist
        "vehicle_name": f"{seeded_db['vehicle'].name} ({seeded_db['vehicle'].number})",
        "driver_name": f"{seeded_db['driver'].name} ({seeded_db['driver'].phone})",
        "pickup_date": "2025-07-12",
        "pickup_time": "10:00",
        "pickup_location": "Test Pickup",
        "dropoff_location": "Test Dropoff"
    }
    
    try:
        logger.info("Starting minimal job creation test...")
        
        jobs_page.click_add_job()
        
        # Fill and submit the form
        jobs_page.fill_job_form(minimal_job_data)
        jobs_page.submit_job_form()
        
        # Verify job was created
        assert jobs_page.verify_job_created(minimal_job_data), "Minimal job creation failed"
        logger.info("Minimal job creation test passed")
        
    except Exception as e:
        logger.error(f"Minimal job creation failed: {e}")
        save_debug_artifacts(browser, "minimal_job_create_failure")
        raise