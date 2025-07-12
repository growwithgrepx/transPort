import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)

class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 10)
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present and visible"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for an element to be clickable"""
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    def get_current_url(self):
        """Get the current URL"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get the page title"""
        return self.driver.title
    
    def take_screenshot(self, filename):
        """Take a screenshot and save it to test_screenshots folder"""
        try:
            # Ensure test_screenshots directory exists
            os.makedirs("test_screenshots", exist_ok=True)
            
            # If filename doesn't include path, save to test_screenshots folder
            if not os.path.dirname(filename):
                filename = os.path.join("test_screenshots", filename)
            
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
        except Exception as e:
            logger.error(f"Failed to take screenshot: {str(e)}")
    
    def get_page_source(self):
        """Get the page source"""
        return self.driver.page_source 