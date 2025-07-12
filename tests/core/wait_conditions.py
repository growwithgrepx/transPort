"""
Advanced wait conditions for Selenium WebDriver.
Replaces time.sleep() calls with intelligent waits for better performance and reliability.
"""

import logging
from typing import Optional, Callable, Any, Tuple
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .exceptions import ElementNotFoundException, ElementNotClickableException

logger = logging.getLogger(__name__)


class SmartWait:
    """Enhanced wait utility with retry logic and custom conditions"""
    
    def __init__(self, driver: WebDriver, timeout: int = 10, poll_frequency: float = 0.5):
        self.driver = driver
        self.timeout = timeout
        self.poll_frequency = poll_frequency
        self.wait = WebDriverWait(driver, timeout, poll_frequency)
    
    def for_element_present(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be present in DOM"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            raise ElementNotFoundException(f"Element with {by}={value}", (by, value), wait_timeout)
    
    def for_element_visible(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be visible"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except TimeoutException:
            raise ElementNotFoundException(f"Visible element with {by}={value}", (by, value), wait_timeout)
    
    def for_element_clickable(self, by: By, value: str, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be clickable"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.element_to_be_clickable((by, value))
            )
        except TimeoutException:
            raise ElementNotClickableException(f"Element with {by}={value}", (by, value))
    
    def for_text_present(self, text: str, by: By = By.TAG_NAME, value: str = "body", timeout: Optional[int] = None) -> bool:
        """Wait for text to be present in element"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                EC.text_to_be_present_in_element((by, value), text)
            )
        except TimeoutException:
            raise ElementNotFoundException(f"Text '{text}' not found in {by}={value}", (by, value), wait_timeout)
    
    def for_url_contains(self, url_fragment: str, timeout: Optional[int] = None) -> bool:
        """Wait for URL to contain specific fragment"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                lambda driver: url_fragment in driver.current_url
            )
        except TimeoutException:
            raise ElementNotFoundException(f"URL containing '{url_fragment}' not found", None, wait_timeout)
    
    def for_url_changed_from(self, original_url: str, timeout: Optional[int] = None) -> bool:
        """Wait for URL to change from the original"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                lambda driver: driver.current_url != original_url
            )
        except TimeoutException:
            raise ElementNotFoundException(f"URL did not change from '{original_url}'", None, wait_timeout)
    
    def for_page_load_complete(self, timeout: Optional[int] = None) -> bool:
        """Wait for page to fully load"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            raise ElementNotFoundException("Page did not load completely", None, wait_timeout)
    
    def for_ajax_complete(self, timeout: Optional[int] = None) -> bool:
        """Wait for AJAX requests to complete"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                lambda driver: driver.execute_script("return jQuery.active == 0")
            )
        except TimeoutException:
            # jQuery might not be available, try alternative approach
            try:
                return WebDriverWait(self.driver, wait_timeout).until(
                    lambda driver: driver.execute_script("return window.performance.getEntriesByType('resource').every(r => r.responseEnd > 0)")
                )
            except TimeoutException:
                logger.warning("AJAX completion detection failed, continuing anyway")
                return True
    
    def for_element_stable(self, by: By, value: str, stability_time: float = 1.0, timeout: Optional[int] = None) -> WebElement:
        """Wait for element to be stable (not moving/changing)"""
        wait_timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, wait_timeout).until(
                self._element_stable_condition(by, value, stability_time)
            )
        except TimeoutException:
            raise ElementNotFoundException(f"Stable element with {by}={value}", (by, value), wait_timeout)
    
    def _element_stable_condition(self, by: By, value: str, stability_time: float):
        """Custom condition to check if element is stable"""
        def condition(driver):
            try:
                element = driver.find_element(by, value)
                initial_location = element.location
                initial_size = element.size
                
                # Wait for stability time
                import time
                time.sleep(stability_time)
                
                # Check if element is still the same
                current_location = element.location
                current_size = element.size
                
                return (initial_location == current_location and 
                       initial_size == current_size)
            except StaleElementReferenceException:
                return False
        return condition


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((StaleElementReferenceException, TimeoutException))
)
def retry_element_operation(operation: Callable, *args, **kwargs) -> Any:
    """Retry an element operation with exponential backoff"""
    return operation(*args, **kwargs)


class WaitConditions:
    """Static wait condition utilities"""
    
    @staticmethod
    def wait_for_form_ready(driver: WebDriver, form_id: str, timeout: int = 10) -> WebElement:
        """Wait for form to be ready for interaction"""
        wait = SmartWait(driver, timeout)
        return wait.for_element_present(By.ID, form_id)
    
    @staticmethod
    def wait_for_autocomplete_ready(driver: WebDriver, field_id: str, timeout: int = 5) -> bool:
        """Wait for autocomplete field to be ready"""
        wait = SmartWait(driver, timeout)
        try:
            # Wait for any loading indicators to disappear
            wait.for_element_present(By.ID, field_id)
            # Small delay for autocomplete to initialize
            import time
            time.sleep(0.1)
            return True
        except Exception:
            return False
    
    @staticmethod
    def wait_for_validation_errors(driver: WebDriver, timeout: int = 3) -> list:
        """Wait for and collect validation errors"""
        try:
            wait = SmartWait(driver, timeout)
            # Wait for validation errors to appear
            wait.for_element_present(By.CLASS_NAME, "invalid-feedback")
            
            # Collect all validation errors
            error_elements = driver.find_elements(By.CLASS_NAME, "invalid-feedback")
            errors = []
            for element in error_elements:
                if element.is_displayed():
                    errors.append(element.text.strip())
            return errors
        except TimeoutException:
            return []
    
    @staticmethod
    def wait_for_success_message(driver: WebDriver, timeout: int = 5) -> Optional[str]:
        """Wait for success message to appear"""
        try:
            wait = SmartWait(driver, timeout)
            success_element = wait.for_element_visible(By.CLASS_NAME, "alert-success")
            return success_element.text.strip()
        except TimeoutException:
            return None
    
    @staticmethod
    def wait_for_error_message(driver: WebDriver, timeout: int = 5) -> Optional[str]:
        """Wait for error message to appear"""
        try:
            wait = SmartWait(driver, timeout)
            error_element = wait.for_element_visible(By.CLASS_NAME, "alert-danger")
            return error_element.text.strip()
        except TimeoutException:
            return None


# Convenience functions for common wait operations
def wait_for_element(driver: WebDriver, by: By, value: str, timeout: int = 10) -> WebElement:
    """Wait for element to be present and visible"""
    wait = SmartWait(driver, timeout)
    return wait.for_element_visible(by, value)


def wait_for_clickable(driver: WebDriver, by: By, value: str, timeout: int = 10) -> WebElement:
    """Wait for element to be clickable"""
    wait = SmartWait(driver, timeout)
    return wait.for_element_clickable(by, value)


def wait_for_text(driver: WebDriver, text: str, timeout: int = 10) -> bool:
    """Wait for text to be present on page"""
    wait = SmartWait(driver, timeout)
    return wait.for_text_present(text)


def wait_for_url_change(driver: WebDriver, original_url: str, timeout: int = 10) -> bool:
    """Wait for URL to change from original"""
    wait = SmartWait(driver, timeout)
    return wait.for_url_changed_from(original_url) 