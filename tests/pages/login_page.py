import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Page Object Model for the Login page"""
    
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.login_url = f"{base_url}/login"
    
    def load(self):
        """Load the login page"""
        self.driver.get(self.login_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        logger.info(f"Loaded login page: {self.driver.current_url}")
    
    def login(self, username, password):
        """Login with provided credentials"""
        try:
            logger.info(f"Attempting to login with username: {username}")
            
            # Wait for form to be ready
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            # Find and fill username field
            username_field = self.driver.find_element(By.ID, "username")
            username_field.clear()
            username_field.send_keys(username)
            
            # Find and fill password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Find and click submit button
            submit_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            
            # Wait for redirect to dashboard or jobs page
            try:
                WebDriverWait(self.driver, 10).until(
                    lambda driver: "/dashboard" in driver.current_url or "/jobs" in driver.current_url
                )
                logger.info("Login successful")
                return True
            except TimeoutException:
                # Check if we're still on login page (login failed)
                if "/login" in self.driver.current_url:
                    # Look for error messages
                    try:
                        error_elements = self.driver.find_elements(By.CLASS_NAME, "alert-danger")
                        if error_elements:
                            error_text = error_elements[0].text
                            logger.error(f"Login failed with error: {error_text}")
                            raise Exception(f"Login failed: {error_text}")
                    except NoSuchElementException:
                        pass
                    
                    logger.error("Login failed - still on login page")
                    raise Exception("Login failed - still on login page")
                else:
                    # We might be on a different page, check current URL
                    logger.info(f"Login completed, current URL: {self.driver.current_url}")
                    return True
                    
        except Exception as e:
            logger.error(f"Error during login: {str(e)}")
            # Take screenshot for debugging
            self.take_screenshot("login_error.png")
            raise
    
    def is_logged_in(self):
        """Check if user is logged in"""
        try:
            # Check if we're on a protected page (not login page)
            if "/login" in self.driver.current_url:
                return False
            
            # Look for logout link or user menu
            logout_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/logout')]")
            if logout_elements:
                return True
            
            # Check for dashboard or jobs page elements
            dashboard_elements = self.driver.find_elements(By.ID, "dashboard")
            jobs_elements = self.driver.find_elements(By.ID, "jobs-table")
            
            return len(dashboard_elements) > 0 or len(jobs_elements) > 0
            
        except Exception as e:
            logger.error(f"Error checking login status: {str(e)}")
            return False
    
    def logout(self):
        """Logout the current user"""
        try:
            # Find and click logout link
            logout_link = self.driver.find_element(By.XPATH, "//a[contains(@href, '/logout')]")
            logout_link.click()
            
            # Wait for redirect to login page
            WebDriverWait(self.driver, 10).until(
                lambda driver: "/login" in driver.current_url
            )
            logger.info("Logout successful")
            
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}") 