"""
Enhanced JobsPage implementing true Page Object Model.
No assertions or test logic - pure page interaction methods with builder pattern.
"""

import logging
from typing import Optional, Dict, Any, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from ..core.base_page import BasePage, FormMixin
from ..core.locators import get_locator, JobsPageLocators
from ..core.exceptions import (
    ElementNotFoundException,
    FormValidationException,
    NavigationException,
    DataNotFoundException
)

logger = logging.getLogger(__name__)


class JobsPage(BasePage, FormMixin):
    """Enhanced Page Object Model for the Jobs page"""
    
    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url, "JobsPage")
    
    def is_loaded(self) -> bool:
        """Check if the jobs page is loaded and ready"""
        try:
            # Check for jobs table presence
            return self.is_element_present(get_locator("jobs", "JOBS_TABLE"))
        except Exception:
            return False
    
    def get_page_url(self) -> str:
        """Get the jobs page URL"""
        return f"{self.base_url}/jobs"
    
    def click_add_job_button(self) -> 'JobsPage':
        """Click the Add Job button to navigate to job creation form"""
        locator = get_locator("jobs", "ADD_JOB_BUTTON")
        return self.click_element(locator)
    
    def wait_for_job_form(self, timeout: int = 10) -> 'JobsPage':
        """Wait for job form to be ready for interaction"""
        locator = get_locator("jobs", "JOB_FORM")
        self.find_element(locator, timeout=timeout)
        return self
    
    def fill_agent_name(self, agent_name: str) -> 'JobsPage':
        """Fill the agent name field"""
        locator = get_locator("jobs", "AGENT_NAME_FIELD")
        self.fill_field(locator, agent_name)
        # Trigger input event for autocomplete
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                           self.find_element(locator))
        return self
    
    def fill_service_name(self, service_name: str) -> 'JobsPage':
        """Fill the service name field"""
        locator = get_locator("jobs", "SERVICE_NAME_FIELD")
        self.fill_field(locator, service_name)
        # Trigger input event for autocomplete
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                           self.find_element(locator))
        return self
    
    def fill_vehicle_name(self, vehicle_name: str) -> 'JobsPage':
        """Fill the vehicle name field"""
        locator = get_locator("jobs", "VEHICLE_NAME_FIELD")
        self.fill_field(locator, vehicle_name)
        # Trigger input event for autocomplete
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                           self.find_element(locator))
        return self
    
    def fill_driver_name(self, driver_name: str) -> 'JobsPage':
        """Fill the driver name field"""
        locator = get_locator("jobs", "DRIVER_NAME_FIELD")
        self.fill_field(locator, driver_name)
        # Trigger input event for autocomplete
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", 
                           self.find_element(locator))
        return self
    
    def fill_pickup_date(self, pickup_date: str) -> 'JobsPage':
        """Fill the pickup date field using JavaScript to avoid browser validation issues"""
        locator = get_locator("jobs", "PICKUP_DATE_FIELD")
        element = self.find_element(locator)
        self.execute_script("arguments[0].value = arguments[1];", element, pickup_date)
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
        self.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
        return self
    
    def fill_pickup_time(self, pickup_time: str) -> 'JobsPage':
        """Fill the pickup time field using JavaScript to avoid browser validation issues"""
        locator = get_locator("jobs", "PICKUP_TIME_FIELD")
        element = self.find_element(locator)
        self.execute_script("arguments[0].value = arguments[1];", element, pickup_time)
        self.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)
        self.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
        return self
    
    def fill_pickup_location(self, pickup_location: str) -> 'JobsPage':
        """Fill the pickup location field"""
        locator = get_locator("jobs", "PICKUP_LOCATION_FIELD")
        return self.fill_field(locator, pickup_location)
    
    def fill_dropoff_location(self, dropoff_location: str) -> 'JobsPage':
        """Fill the dropoff location field"""
        locator = get_locator("jobs", "DROPOFF_LOCATION_FIELD")
        return self.fill_field(locator, dropoff_location)
    
    def fill_customer_name(self, customer_name: str) -> 'JobsPage':
        """Fill the customer name field"""
        locator = get_locator("jobs", "CUSTOMER_NAME_FIELD")
        return self.fill_field(locator, customer_name)
    
    def fill_customer_email(self, customer_email: str) -> 'JobsPage':
        """Fill the customer email field"""
        locator = get_locator("jobs", "CUSTOMER_EMAIL_FIELD")
        return self.fill_field(locator, customer_email)
    
    def fill_customer_mobile(self, customer_mobile: str) -> 'JobsPage':
        """Fill the customer mobile field"""
        locator = get_locator("jobs", "CUSTOMER_MOBILE_FIELD")
        return self.fill_field(locator, customer_mobile)
    
    def fill_remarks(self, remarks: str) -> 'JobsPage':
        """Fill the remarks field"""
        locator = get_locator("jobs", "REMARKS_FIELD")
        return self.fill_field(locator, remarks)
    
    def select_status(self, status: str) -> 'JobsPage':
        """Select job status from dropdown"""
        locator = get_locator("jobs", "STATUS_FIELD")
        return self.select_option(locator, status)
    
    def click_submit_button(self) -> 'JobsPage':
        """Click the form submit button"""
        locator = get_locator("jobs", "SUBMIT_BUTTON")
        return self.click_element(locator)
    
    def submit_job_form(self) -> 'JobsPage':
        """Submit the job form and wait for result"""
        logger.info("Submitting job form...")
        
        # Store current URL before submission
        original_url = self.get_current_url()
        
        # Click submit button
        self.click_submit_button()
        
        # Wait for either success (redirect to jobs page) or error (stay on form)
        try:
            # Wait for redirect to jobs page (success case)
            self.wait_for_url_contains("/jobs", timeout=10)
            if "add" not in self.get_current_url():
                logger.info("Job form submitted successfully, redirected to jobs page")
                return self
        except Exception:
            pass
        
        # Check if we're still on the form page (error case)
        if "/jobs/add" in self.get_current_url():
            # Check for validation errors
            validation_errors = self.get_validation_errors()
            if validation_errors:
                raise FormValidationException("Job Form", validation_errors)
            
            # Check for general error messages
            error_message = self.get_error_message()
            if error_message:
                raise FormValidationException("Job Form", [error_message])
            
            raise FormValidationException("Job Form", ["Form submission failed"])
        
        return self
    
    def get_jobs_count(self) -> int:
        """Get the number of jobs in the table"""
        try:
            # Wait for table to load
            self.find_element(get_locator("jobs", "JOBS_TABLE"))
            
            # Count table rows (excluding header and filter row)
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#jobs-table tbody tr")
            return len(rows)
        except Exception as e:
            logger.error(f"Error getting jobs count: {str(e)}")
            return 0
    
    def search_job(self, search_term: str) -> 'JobsPage':
        """Search for a job by term"""
        locator = get_locator("jobs", "SEARCH_INPUT")
        self.fill_field(locator, search_term)
        return self
    
    def is_job_in_table(self, search_criteria: Dict[str, str]) -> bool:
        """Check if a job exists in the table based on search criteria"""
        try:
            # Get all table rows (data rows only, excluding header and filter)
            rows = self.driver.find_elements(By.CSS_SELECTOR, "#jobs-table tbody tr")
            
            for row in rows:
                row_text = row.text.lower()
                # Check if all search criteria are found in the row
                if all(criteria.lower() in row_text for criteria in search_criteria.values()):
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Error checking job in table: {str(e)}")
            return False
    
    def click_edit_job(self, job_index: int = 0) -> 'JobsPage':
        """Click edit button for a specific job (default: first job)"""
        # Find edit button in the specified row
        # Note: Table has header + filter row, so data rows start from index 2
        edit_xpath = f"//table[@id='jobs-table']//tr[{job_index + 2}]//a[contains(@href, 'edit')]"
        edit_button = self.driver.find_element(By.XPATH, edit_xpath)
        
        # Scroll to button and click
        self.execute_script("arguments[0].scrollIntoView(true);", edit_button)
        edit_button.click()
        
        # Wait for form to load
        self.wait_for_job_form()
        return self
    
    def click_delete_job(self, job_index: int = 0) -> 'JobsPage':
        """Click delete button for a specific job and confirm deletion"""
        # Find delete button in the specified row
        # Note: Table has header + filter row, so data rows start from index 2
        delete_xpath = f"//table[@id='jobs-table']//tr[{job_index + 2}]//button[contains(@class, 'btn-danger')]"
        delete_button = self.driver.find_element(By.XPATH, delete_xpath)
        
        # Scroll to button and click
        self.execute_script("arguments[0].scrollIntoView(true);", delete_button)
        delete_button.click()
        
        # Wait for confirmation dialog and confirm
        self.wait_for_alert_present()
        self.accept_alert()
        
        # Wait for page to refresh
        self.find_element(get_locator("jobs", "JOBS_TABLE"))
        return self
    
    def get_job_data_from_row(self, row_index: int = 0) -> Dict[str, str]:
        """Extract job data from a specific table row"""
        try:
            # Note: Table has header + filter row, so data rows start from index 2
            row_xpath = f"//table[@id='jobs-table']//tr[{row_index + 2}]"
            row = self.driver.find_element(By.XPATH, row_xpath)
            cells = row.find_elements(By.TAG_NAME, "td")
            
            # Extract data from cells (adjust based on actual table structure)
            job_data = {}
            if len(cells) >= 1:
                job_data['customer'] = cells[0].text.strip()
            if len(cells) >= 2:
                job_data['pickup_location'] = cells[1].text.strip()
            if len(cells) >= 3:
                job_data['dropoff_location'] = cells[2].text.strip()
            # Add more fields as needed based on table structure
            
            return job_data
        except Exception as e:
            logger.error(f"Error extracting job data from row: {str(e)}")
            return {}
    
    def show_advanced_fields(self) -> 'JobsPage':
        """Show advanced fields section if it exists"""
        try:
            advanced_locator = get_locator("jobs", "ADVANCED_FIELDS")
            if self.is_element_present(advanced_locator):
                element = self.find_element(advanced_locator)
                if element.value_of_css_property("display") == "none":
                    self.execute_script('document.getElementById("advanced-fields").style.display = "block";')
        except Exception:
            logger.info("Advanced fields section not found or already visible")
        
        return self
    
    def get_form_validation_errors(self) -> List[str]:
        """Get all validation errors from the form"""
        return self.get_validation_errors()
    
    def is_form_valid(self) -> bool:
        """Check if the form is valid (no validation errors)"""
        return len(self.get_validation_errors()) == 0
    
    def clear_form(self) -> 'JobsPage':
        """Clear all form fields"""
        # Clear text fields
        text_fields = [
            "AGENT_NAME_FIELD", "SERVICE_NAME_FIELD", "VEHICLE_NAME_FIELD", "DRIVER_NAME_FIELD",
            "PICKUP_LOCATION_FIELD", "DROPOFF_LOCATION_FIELD", "CUSTOMER_NAME_FIELD",
            "CUSTOMER_EMAIL_FIELD", "CUSTOMER_MOBILE_FIELD", "REMARKS_FIELD"
        ]
        
        for field_name in text_fields:
            try:
                locator = get_locator("jobs", field_name)
                self.fill_field(locator, "")
            except Exception:
                pass  # Field might not exist or be readonly
        
        # Clear date/time fields
        date_time_fields = ["PICKUP_DATE_FIELD", "PICKUP_TIME_FIELD"]
        for field_name in date_time_fields:
            try:
                locator = get_locator("jobs", field_name)
                element = self.find_element(locator)
                self.execute_script("arguments[0].value = '';", element)
            except Exception:
                pass
        
        return self 