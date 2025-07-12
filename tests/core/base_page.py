"""
Enhanced BasePage class implementing true Page Object Model architecture.
Provides fluent interface, builder pattern, and proper separation of concerns.
"""

import logging
import os
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementClickInterceptedException,
    StaleElementReferenceException
)

from .exceptions import (
    ElementNotFoundException,
    ElementNotClickableException,
    PageLoadTimeoutException,
    FormValidationException,
    NavigationException
)
from .wait_conditions import SmartWait, WaitConditions, retry_element_operation
from .locators import Locator, get_locator

logger = logging.getLogger(__name__)


class BasePage(ABC):
    """
    Abstract base class for all page objects.
    Implements true Page Object Model with fluent interface and builder pattern.
    """
    
    def __init__(self, driver: WebDriver, base_url: str, page_name: str = None):
        self.driver = driver
        self.base_url = base_url
        self.page_name = page_name or self.__class__.__name__
        self.wait = SmartWait(driver)
        self._current_url = None
    
    @abstractmethod
    def is_loaded(self) -> bool:
        """Check if the page is loaded and ready for interaction"""
        pass
    
    @abstractmethod
    def get_page_url(self) -> str:
        """Get the URL for this page"""
        pass
    
    def load(self) -> 'BasePage':
        """Load the page and return self for method chaining"""
        url = self.get_page_url()
        logger.info(f"Loading page: {url}")
        
        self.driver.get(url)
        self._current_url = self.driver.current_url
        
        # Wait for page to load
        self.wait.for_page_load_complete()
        
        # Verify page is loaded
        if not self.is_loaded():
            raise PageLoadTimeoutException(self.page_name, self.wait.timeout)
        
        logger.info(f"Page loaded successfully: {self.driver.current_url}")
        return self
    
    def refresh(self) -> 'BasePage':
        """Refresh the current page"""
        logger.info("Refreshing page")
        self.driver.refresh()
        self.wait.for_page_load_complete()
        return self
    
    def navigate_to(self, url: str) -> 'BasePage':
        """Navigate to a specific URL"""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
        self._current_url = self.driver.current_url
        self.wait.for_page_load_complete()
        return self
    
    def get_current_url(self) -> str:
        """Get the current URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get the page title"""
        return self.driver.title
    
    def take_screenshot(self, filename: str) -> 'BasePage':
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
        
        return self
    
    def get_page_source(self) -> str:
        """Get the page source"""
        return self.driver.page_source
    
    def find_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Find an element using a locator with retry logic"""
        try:
            return retry_element_operation(
                self.wait.for_element_visible,
                locator.by,
                locator.value,
                timeout
            )
        except Exception as e:
            raise ElementNotFoundException(locator.name, (locator.by, locator.value), timeout)
    
    def find_clickable_element(self, locator: Locator, timeout: Optional[int] = None) -> WebElement:
        """Find a clickable element using a locator"""
        try:
            return retry_element_operation(
                self.wait.for_element_clickable,
                locator.by,
                locator.value,
                timeout
            )
        except Exception as e:
            raise ElementNotClickableException(locator.name, (locator.by, locator.value))
    
    def click_element(self, locator: Locator, timeout: Optional[int] = None) -> 'BasePage':
        """Click an element with multiple fallback strategies"""
        element = self.find_clickable_element(locator, timeout)
        
        try:
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            
            # Try regular click first
            element.click()
        except ElementClickInterceptedException:
            try:
                # Try JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                # Try ActionChains click
                ActionChains(self.driver).move_to_element(element).click().perform()
        
        logger.info(f"Clicked element: {locator.name}")
        return self
    
    def fill_field(self, locator: Locator, value: str, clear_first: bool = True) -> 'BasePage':
        """Fill a form field with value"""
        element = self.find_element(locator)
        
        if clear_first:
            element.clear()
        
        element.send_keys(str(value))
        logger.info(f"Filled field {locator.name} with value: {value}")
        return self
    
    def select_option(self, locator: Locator, option_text: str) -> 'BasePage':
        """Select an option from a dropdown"""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(option_text)
        logger.info(f"Selected option '{option_text}' in {locator.name}")
        return self
    
    def check_checkbox(self, locator: Locator, should_check: bool = True) -> 'BasePage':
        """Check or uncheck a checkbox"""
        element = self.find_element(locator)
        is_checked = element.is_selected()
        
        if should_check and not is_checked:
            self.click_element(locator)
        elif not should_check and is_checked:
            self.click_element(locator)
        
        logger.info(f"{'Checked' if should_check else 'Unchecked'} checkbox: {locator.name}")
        return self
    
    def wait_for_text(self, text: str, timeout: Optional[int] = None) -> 'BasePage':
        """Wait for text to be present on the page"""
        self.wait.for_text_present(text, timeout=timeout)
        logger.info(f"Text found on page: {text}")
        return self
    
    def wait_for_url_change(self, original_url: str, timeout: Optional[int] = None) -> 'BasePage':
        """Wait for URL to change from original"""
        self.wait.for_url_changed_from(original_url, timeout=timeout)
        logger.info(f"URL changed from: {original_url}")
        return self
    
    def wait_for_url_contains(self, url_fragment: str, timeout: Optional[int] = None) -> 'BasePage':
        """Wait for URL to contain specific fragment"""
        self.wait.for_url_contains(url_fragment, timeout=timeout)
        logger.info(f"URL contains: {url_fragment}")
        return self
    
    def get_validation_errors(self) -> List[str]:
        """Get all validation errors on the current page"""
        return WaitConditions.wait_for_validation_errors(self.driver)
    
    def get_success_message(self) -> Optional[str]:
        """Get success message if present"""
        return WaitConditions.wait_for_success_message(self.driver)
    
    def get_error_message(self) -> Optional[str]:
        """Get error message if present"""
        return WaitConditions.wait_for_error_message(self.driver)
    
    def is_element_present(self, locator: Locator) -> bool:
        """Check if an element is present on the page"""
        try:
            self.driver.find_element(locator.by, locator.value)
            return True
        except NoSuchElementException:
            return False
    
    def is_element_visible(self, locator: Locator) -> bool:
        """Check if an element is visible on the page"""
        try:
            element = self.driver.find_element(locator.by, locator.value)
            return element.is_displayed()
        except NoSuchElementException:
            return False
    
    def get_element_text(self, locator: Locator) -> str:
        """Get the text content of an element"""
        element = self.find_element(locator)
        return element.text.strip()
    
    def get_element_attribute(self, locator: Locator, attribute: str) -> str:
        """Get the value of an element attribute"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)
    
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript on the page"""
        return self.driver.execute_script(script, *args)
    
    def accept_alert(self) -> 'BasePage':
        """Accept a browser alert"""
        self.driver.switch_to.alert.accept()
        return self
    
    def dismiss_alert(self) -> 'BasePage':
        """Dismiss a browser alert"""
        self.driver.switch_to.alert.dismiss()
        return self
    
    def get_alert_text(self) -> str:
        """Get the text of a browser alert"""
        return self.driver.switch_to.alert.text
    
    def switch_to_frame(self, frame_reference) -> 'BasePage':
        """Switch to an iframe"""
        self.driver.switch_to.frame(frame_reference)
        return self
    
    def switch_to_default_content(self) -> 'BasePage':
        """Switch back to default content from iframe"""
        self.driver.switch_to.default_content()
        return self
    
    def wait_for_ajax_complete(self, timeout: Optional[int] = None) -> 'BasePage':
        """Wait for AJAX requests to complete"""
        self.wait.for_ajax_complete(timeout=timeout)
        return self


class FormBuilder:
    """Builder pattern for form filling operations"""
    
    def __init__(self, page: BasePage):
        self.page = page
        self._form_data = {}
    
    def fill_field(self, locator: Locator, value: str) -> 'FormBuilder':
        """Add a field to be filled"""
        self._form_data[locator] = value
        return self
    
    def select_option(self, locator: Locator, option_text: str) -> 'FormBuilder':
        """Add a dropdown selection"""
        self._form_data[locator] = ('select', option_text)
        return self
    
    def check_checkbox(self, locator: Locator, should_check: bool = True) -> 'FormBuilder':
        """Add a checkbox to be checked/unchecked"""
        self._form_data[locator] = ('checkbox', should_check)
        return self
    
    def submit(self, submit_locator: Locator) -> BasePage:
        """Fill all fields and submit the form"""
        # Fill all fields
        for locator, value in self._form_data.items():
            if isinstance(value, tuple):
                action, action_value = value
                if action == 'select':
                    self.page.select_option(locator, action_value)
                elif action == 'checkbox':
                    self.page.check_checkbox(locator, action_value)
            else:
                self.page.fill_field(locator, value)
        
        # Submit the form
        self.page.click_element(submit_locator)
        return self.page
    
    def build(self) -> Dict[Locator, Any]:
        """Return the form data without submitting"""
        return self._form_data.copy()


# Mixin for pages that contain forms
class FormMixin:
    """Mixin providing form-related functionality"""
    
    def build_form(self) -> FormBuilder:
        """Create a form builder for this page"""
        return FormBuilder(self)
    
    def fill_form(self, form_data: Dict[Locator, Any]) -> 'BasePage':
        """Fill a form with the provided data"""
        for locator, value in form_data.items():
            if isinstance(value, tuple):
                action, action_value = value
                if action == 'select':
                    self.select_option(locator, action_value)
                elif action == 'checkbox':
                    self.check_checkbox(locator, action_value)
            else:
                self.fill_field(locator, value)
        return self
    
    def validate_form(self) -> List[str]:
        """Validate the current form and return any errors"""
        return self.get_validation_errors()
    
    def submit_form(self, submit_locator: Locator) -> 'BasePage':
        """Submit the form using the specified submit button"""
        return self.click_element(submit_locator) 