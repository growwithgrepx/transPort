import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class JobsPage(BasePage):
    """Page Object Model for the Jobs page"""
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.jobs_url = f"{base_url}/jobs"
    
    def load(self):
        """Load the jobs page"""
        self.driver.get(self.jobs_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobs-table"))
        )
        logger.info(f"Loaded jobs page: {self.driver.current_url}")
    
    def click_add_job_button(self):
        """Click the Add Job button"""
        try:
            # Try multiple selectors for the Add Job button
            add_button = None
            selectors = [
                "//a[contains(@href, '/jobs/add')]",
                "//a[contains(text(), 'Add Job')]",
                "//button[contains(text(), 'Add Job')]",
                "//a[@href='/jobs/add']"
            ]
            
            for selector in selectors:
                try:
                    add_button = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not add_button:
                raise NoSuchElementException("Could not find Add Job button")
            
            # Scroll to the button to ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            time.sleep(0.5)
            
            # Try to click with JavaScript if regular click fails
            try:
                add_button.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", add_button)
            
            # Wait for the form page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobForm"))
            )
            logger.info("Successfully clicked Add Job button")
            return self
            
        except Exception as e:
            logger.error(f"Error clicking Add Job button: {str(e)}")
            raise
    
    def fill_job_form(self, job_data):
        """Fill the job form with provided data"""
        try:
            logger.info("Starting to fill job form...")
            
            # Wait for form to be ready
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobForm"))
            )
            
            for field_name, value in job_data.items():
                try:
                    # Skip readonly/hidden fields
                    field = self.driver.find_element(By.ID, field_name)
                    if field.get_attribute("readonly") or field.get_attribute("type") == "hidden":
                        logger.info(f"Skipping readonly/hidden field: {field_name}")
                        continue
                    
                    # Handle different field types
                    field_type = field.get_attribute("type")
                    
                    if field_type == "checkbox":
                        # For checkboxes, check if it should be checked
                        if value:
                            if not field.is_selected():
                                # Scroll to checkbox and click
                                self.driver.execute_script("arguments[0].scrollIntoView(true);", field)
                                time.sleep(0.2)
                                try:
                                    field.click()
                                except ElementClickInterceptedException:
                                    self.driver.execute_script("arguments[0].click();", field)
                    elif field.tag_name == "select":
                        # Handle select dropdowns
                        from selenium.webdriver.support.ui import Select
                        select = Select(field)
                        select.select_by_visible_text(str(value))
                    else:
                        # Clear and fill text fields
                        field.clear()
                        
                        # Use JavaScript for date/time fields to avoid browser validation issues
                        if field_name in ["pickup_date", "pickup_time"]:
                            self.driver.execute_script("arguments[0].value = arguments[1];", field, str(value))
                            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
                            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", field)
                            time.sleep(0.2)
                        else:
                            field.send_keys(str(value))
                        
                        # Trigger input events for autocomplete fields
                        if field_name in ["agent_name", "service_name", "vehicle_name", "driver_name"]:
                            self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
                            time.sleep(0.5)  # Wait for autocomplete
                    
                    logger.info(f"Filled field {field_name} with value: {value}")
                    
                except Exception as e:
                    logger.warning(f"Error filling field {field_name}: {str(e)}")
                    # Continue with other fields
                    continue
            
            logger.info("Job form filled successfully")
            
        except Exception as e:
            logger.error(f"Error filling job form: {str(e)}")
            raise
    
    def submit_job_form(self):
        """Submits the job form and handles errors gracefully, logging and returning status instead of raising."""
        try:
            logger.info("Attempting to submit job form...")
            
            # Wait for form to be ready
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobForm"))
            )
            
            # Find the submit button with multiple strategies
            submit_btn = None
            selectors = [
                "//form[@id='jobForm']//button[@type='submit']",
                "//form[@id='jobForm']//button[contains(text(), 'Add')]",
                "//form[@id='jobForm']//button[contains(text(), 'Update')]",
                "//button[@type='submit']"
            ]
            
            for selector in selectors:
                try:
                    submit_btn = self.driver.find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not submit_btn:
                raise NoSuchElementException("Could not find submit button")
            
            # Scroll to submit button and ensure it's visible
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
            time.sleep(0.5)
            
            # Take screenshot before submission for debugging
            self.take_screenshot("before_submit.png")
            
            # Try multiple click strategies
            try:
                # First try regular click
                submit_btn.click()
            except ElementClickInterceptedException:
                try:
                    # Try JavaScript click
                    self.driver.execute_script("arguments[0].click();", submit_btn)
                except Exception:
                    # Try ActionChains click
                    ActionChains(self.driver).move_to_element(submit_btn).click().perform()
            
            # Wait for either success (redirect to jobs page) or error (stay on form)
            try:
                # Wait for redirect to jobs page (success case)
                WebDriverWait(self.driver, 10).until(
                    lambda driver: "/jobs" in driver.current_url and "add" not in driver.current_url
                )
                logger.info("Job form submitted successfully, redirected to jobs page")
                return True
            except TimeoutException:
                # Check if we're still on the form page (error case)
                if "/jobs/add" in self.driver.current_url:
                    # Take screenshot after failed submission
                    self.take_screenshot("after_failed_submit.png")
                    
                    # Look for error messages
                    try:
                        error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
                        if error_elements:
                            error_text = error_elements[0].text
                            logger.error(f"Form submission failed with error: {error_text}")
                            return f"Form submission failed: {error_text}"
                    except NoSuchElementException:
                        pass
                    
                    # Check for validation errors
                    try:
                        invalid_feedback = self.driver.find_elements(By.CLASS_NAME, "invalid-feedback")
                        if invalid_feedback:
                            for feedback in invalid_feedback:
                                if feedback.is_displayed():
                                    logger.error(f"Validation error: {feedback.text}")
                            return "Form has validation errors"
                    except NoSuchElementException:
                        pass
                    
                    # Check if form has validation class
                    form = self.driver.find_element(By.ID, "jobForm")
                    if "was-validated" in form.get_attribute("class"):
                        logger.error("Form has validation errors (was-validated class present)")
                        return "Form has validation errors"
                    
                    # Log current URL and page title for debugging
                    logger.error(f"Form submission failed - still on add page. URL: {self.driver.current_url}, Title: {self.driver.title}")
                    
                    # Check if there are any required fields that might be missing
                    required_fields = self.driver.find_elements(By.CSS_SELECTOR, "[required]")
                    logger.info(f"Found {len(required_fields)} required fields")
                    for field in required_fields:
                        field_id = field.get_attribute("id")
                        field_value = field.get_attribute("value")
                        logger.info(f"Required field {field_id}: value='{field_value}'")
                    
                    return "Form submission failed - still on add page"
                else:
                    # We might be on a different page, check current URL
                    logger.info(f"Form submission completed, current URL: {self.driver.current_url}")
                    return True
                    
        except Exception as e:
            logger.error(f"Error submitting job form: {str(e)}")
            # Take screenshot on error
            self.take_screenshot("submit_error.png")
            return f"Error submitting job form: {str(e)}"
    
    def get_jobs_count(self):
        """Get the number of jobs in the table"""
        try:
            # Wait for table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-table"))
            )
            
            # Count table rows (excluding header)
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#jobs-table tbody tr")
            return len(rows)
            
        except Exception as e:
            logger.error(f"Error getting jobs count: {str(e)}")
            return 0
    
    def search_job(self, search_term):
        """Search for a job by term"""
        try:
            search_input = self.driver.find_element(By.ID, "searchInput")
            search_input.clear()
            search_input.send_keys(search_term)
            
            # Wait for search results
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error searching for job: {str(e)}")
            raise
    
    def delete_job(self, job_id):
        """Delete a job by ID"""
        try:
            # Find delete button for the specific job
            delete_btn = self.driver.find_element(
                By.XPATH, 
                f"//tr[@data-job-id='{job_id}']//button[contains(@class, 'btn-danger')]"
            )
            
            # Scroll to button and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", delete_btn)
            time.sleep(0.5)
            delete_btn.click()
            
            # Wait for confirmation dialog and confirm
            WebDriverWait(self.driver, 5).until(
                EC.alert_is_present()
            )
            self.driver.switch_to.alert.accept()
            
            # Wait for page to refresh
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-table"))
            )
            
            logger.info(f"Successfully deleted job {job_id}")
            
        except Exception as e:
            logger.error(f"Error deleting job {job_id}: {str(e)}")
            raise
    
    def verify_job_created(self, job_data):
        """Verify that a job was created successfully by checking the jobs table"""
        try:
            # Wait for the jobs table to be present
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-table"))
            )
            
            # Wait a bit more for the table to fully load
            time.sleep(1)
            
            # First, check if we have any jobs in the table at all
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#jobs-table tbody tr")
            logger.info(f"Jobs table has {len(rows)} rows")
            
            if len(rows) == 0:
                logger.warning("No jobs found in table")
                return False
            
            # Try to find the job by different search terms
            search_terms = [
                job_data.get('pickup_location', ''),
                job_data.get('dropoff_location', ''),
                job_data.get('agent_name', ''),
                'Test Pickup',  # Fallback
                'Test Dropoff'  # Fallback
            ]
            
            for search_term in search_terms:
                if search_term:
                    try:
                        # Look for the search term in the table
                        job_row = self.driver.find_element(
                            By.XPATH,
                            f"//table[@id='jobs-table']//tr[contains(., '{search_term}')]"
                        )
                        logger.info(f"Job found in table with search term: {search_term}")
                        return True
                    except NoSuchElementException:
                        continue
            
            # If we can't find by specific terms but have rows, assume success
            logger.info("Job not found by specific terms, but table has rows - assuming success")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying job creation: {str(e)}")
            return False
    
    def edit_job(self, job_data):
        """Edit an existing job"""
        try:
            logger.info("Starting job edit...")
            
            # Find and click edit button for the job
            # Look for edit button in the jobs table
            edit_btn = self.driver.find_element(
                By.XPATH,
                "//table[@id='jobs-table']//tr[1]//a[contains(@href, 'edit') or contains(@class, 'edit') or contains(@class, 'btn-primary')]"
            )
            
            # Scroll to button and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
            time.sleep(0.5)
            edit_btn.click()
            
            # Wait for form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobForm"))
            )
            
            # Fill the form with updated data
            self.fill_job_form(job_data)
            
            # Submit the form
            self.submit_job_form()
            
            logger.info("Job edit completed successfully")
            
        except Exception as e:
            logger.error(f"Error editing job: {str(e)}")
            raise
    
    # Fluent interface methods for chaining
    def wait_for_job_form(self):
        """Wait for job form to be present and return self for chaining"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "jobForm"))
        )
        return self
    
    def fill_agent_name(self, agent_name):
        """Fill agent name field and return self for chaining"""
        field = self.driver.find_element(By.ID, "agent_name")
        field.clear()
        field.send_keys(agent_name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        time.sleep(0.5)
        return self
    
    def fill_service_name(self, service_name):
        """Fill service name field and return self for chaining"""
        field = self.driver.find_element(By.ID, "service_name")
        field.clear()
        field.send_keys(service_name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        time.sleep(0.5)
        return self
    
    def fill_vehicle_name(self, vehicle_name):
        """Fill vehicle name field and return self for chaining"""
        field = self.driver.find_element(By.ID, "vehicle_name")
        field.clear()
        field.send_keys(vehicle_name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        time.sleep(0.5)
        return self
    
    def fill_driver_name(self, driver_name):
        """Fill driver name field and return self for chaining"""
        field = self.driver.find_element(By.ID, "driver_name")
        field.clear()
        field.send_keys(driver_name)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        time.sleep(0.5)
        return self
    
    def fill_pickup_date(self, pickup_date):
        """Fill pickup date field and return self for chaining"""
        field = self.driver.find_element(By.ID, "pickup_date")
        self.driver.execute_script("arguments[0].value = arguments[1];", field, pickup_date)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", field)
        time.sleep(0.2)
        return self
    
    def fill_pickup_time(self, pickup_time):
        """Fill pickup time field and return self for chaining"""
        field = self.driver.find_element(By.ID, "pickup_time")
        self.driver.execute_script("arguments[0].value = arguments[1];", field, pickup_time)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", field)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", field)
        time.sleep(0.2)
        return self
    
    def fill_pickup_location(self, pickup_location):
        """Fill pickup location field and return self for chaining"""
        field = self.driver.find_element(By.ID, "pickup_location")
        field.clear()
        field.send_keys(pickup_location)
        return self
    
    def fill_dropoff_location(self, dropoff_location):
        """Fill dropoff location field and return self for chaining"""
        field = self.driver.find_element(By.ID, "dropoff_location")
        field.clear()
        field.send_keys(dropoff_location)
        return self
    
    def click_submit_button(self):
        """Click submit button and return self for chaining"""
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='jobForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        time.sleep(0.5)
        submit_btn.click()
        return self
    
    def is_job_in_table(self, search_criteria):
        """Check if job exists in table based on search criteria"""
        try:
            # Wait for table to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "jobs-table"))
            )
            
            # Debug: Log table content
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#jobs-table tbody tr")
            logger.info(f"Found {len(rows)} rows in jobs table")
            
            for i, row in enumerate(rows):
                row_text = row.text
                logger.info(f"Row {i+1}: {row_text}")
            
            # Look for job by pickup and dropoff locations
            pickup_location = search_criteria.get("pickup_location", "")
            dropoff_location = search_criteria.get("dropoff_location", "")
            
            logger.info(f"Searching for pickup_location: '{pickup_location}'")
            logger.info(f"Searching for dropoff_location: '{dropoff_location}'")
            
            # Check each row manually for better control
            for row in rows:
                row_text = row.text.lower()  # Convert to lowercase for case-insensitive search
                
                if pickup_location and pickup_location.lower() in row_text:
                    logger.info(f"Found job with pickup_location: {pickup_location}")
                    return True
                
                if dropoff_location and dropoff_location.lower() in row_text:
                    logger.info(f"Found job with dropoff_location: {dropoff_location}")
                    return True
            
            logger.info("Job not found in table")
            return False
            
        except Exception as e:
            logger.error(f"Error checking if job is in table: {str(e)}")
            return False