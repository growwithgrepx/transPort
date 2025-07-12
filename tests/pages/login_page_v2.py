"""
Enhanced LoginPage implementing true Page Object Model.
No assertions or test logic - pure page interaction methods.
"""

import logging
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver

from ..core.base_page import BasePage
from ..core.locators import get_locator, LoginPageLocators
from ..core.exceptions import AuthenticationException, PageLoadTimeoutException

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Enhanced Page Object Model for the Login page"""
    
    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url, "LoginPage")
    
    def is_loaded(self) -> bool:
        """Check if the login page is loaded and ready"""
        try:
            # Check for username field presence
            return self.is_element_present(get_locator("login", "USERNAME_FIELD"))
        except Exception:
            return False
    
    def get_page_url(self) -> str:
        """Get the login page URL"""
        return f"{self.base_url}/login"
    
    def enter_username(self, username: str) -> 'LoginPage':
        """Enter username in the username field"""
        locator = get_locator("login", "USERNAME_FIELD")
        return self.fill_field(locator, username)
    
    def enter_password(self, password: str) -> 'LoginPage':
        """Enter password in the password field"""
        locator = get_locator("login", "PASSWORD_FIELD")
        return self.fill_field(locator, password)
    
    def click_login_button(self) -> 'LoginPage':
        """Click the login submit button"""
        locator = get_locator("login", "SUBMIT_BUTTON")
        return self.click_element(locator)
    
    def login(self, username: str, password: str) -> 'LoginPage':
        """Complete login process with provided credentials"""
        logger.info(f"Attempting to login with username: {username}")
        
        # Fill in credentials
        self.enter_username(username)
        self.enter_password(password)
        
        # Store current URL before clicking login
        original_url = self.get_current_url()
        
        # Click login button
        self.click_login_button()
        
        # Wait for navigation (either success or error)
        try:
            self.wait_for_url_change(original_url, timeout=10)
            logger.info("Login successful - URL changed")
            return self
        except Exception:
            # Check if we're still on login page (login failed)
            if "/login" in self.get_current_url():
                error_message = self.get_error_message()
                if error_message:
                    raise AuthenticationException(username, error_message)
                else:
                    raise AuthenticationException(username, "Login failed - still on login page")
            else:
                # We might be on a different page, check current URL
                logger.info(f"Login completed, current URL: {self.get_current_url()}")
                return self
    
    def get_error_message(self) -> Optional[str]:
        """Get login error message if present"""
        locator = get_locator("login", "ERROR_MESSAGE")
        try:
            element = self.find_element(locator, timeout=2)
            if element and element.is_displayed():
                return element.text.strip()
        except Exception:
            pass
        return None

    def get_success_message(self) -> Optional[str]:
        """Get login success message if present"""
        locator = get_locator("login", "SUCCESS_MESSAGE")
        try:
            element = self.find_element(locator, timeout=2)
            if element and element.is_displayed():
                return element.text.strip()
        except Exception:
            pass
        return None
    
    def is_login_form_present(self) -> bool:
        """Check if login form is present on the page"""
        return self.is_element_present(get_locator("login", "LOGIN_FORM"))
    
    def clear_form(self) -> 'LoginPage':
        """Clear all form fields"""
        self.enter_username("")
        self.enter_password("")
        return self
    
    def get_username_field_value(self) -> str:
        """Get the current value of the username field"""
        locator = get_locator("login", "USERNAME_FIELD")
        return self.get_element_attribute(locator, "value")
    
    def get_password_field_value(self) -> str:
        """Get the current value of the password field"""
        locator = get_locator("login", "PASSWORD_FIELD")
        return self.get_element_attribute(locator, "value")
    
    def is_username_field_enabled(self) -> bool:
        """Check if username field is enabled"""
        locator = get_locator("login", "USERNAME_FIELD")
        element = self.find_element(locator)
        return element.is_enabled()
    
    def is_password_field_enabled(self) -> bool:
        """Check if password field is enabled"""
        locator = get_locator("login", "PASSWORD_FIELD")
        element = self.find_element(locator)
        return element.is_enabled()
    
    def is_login_button_enabled(self) -> bool:
        """Check if login button is enabled"""
        locator = get_locator("login", "SUBMIT_BUTTON")
        element = self.find_element(locator)
        return element.is_enabled()
    
    def wait_for_login_form(self, timeout: int = 10) -> 'LoginPage':
        """Wait for login form to be ready"""
        locator = get_locator("login", "LOGIN_FORM")
        self.find_element(locator, timeout=timeout)
        return self 