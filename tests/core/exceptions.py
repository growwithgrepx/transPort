"""
Custom exception hierarchy for the Selenium test framework.
Provides better error categorization and handling for different failure types.
"""

class TestFrameworkException(Exception):
    """Base exception for all test framework errors"""
    pass


class ElementNotFoundException(TestFrameworkException):
    """Raised when an element cannot be found on the page"""
    def __init__(self, element_name, locator, timeout=None):
        self.element_name = element_name
        self.locator = locator
        self.timeout = timeout
        super().__init__(f"Element '{element_name}' not found with locator {locator} after {timeout}s")


class ElementNotClickableException(TestFrameworkException):
    """Raised when an element is found but not clickable"""
    def __init__(self, element_name, locator):
        self.element_name = element_name
        self.locator = locator
        super().__init__(f"Element '{element_name}' with locator {locator} is not clickable")


class PageLoadTimeoutException(TestFrameworkException):
    """Raised when a page fails to load within the expected time"""
    def __init__(self, page_name, timeout):
        self.page_name = page_name
        self.timeout = timeout
        super().__init__(f"Page '{page_name}' failed to load within {timeout}s")


class FormValidationException(TestFrameworkException):
    """Raised when form validation fails"""
    def __init__(self, form_name, validation_errors):
        self.form_name = form_name
        self.validation_errors = validation_errors
        super().__init__(f"Form '{form_name}' validation failed: {validation_errors}")


class NavigationException(TestFrameworkException):
    """Raised when navigation to a page fails"""
    def __init__(self, from_page, to_page, reason=None):
        self.from_page = from_page
        self.to_page = to_page
        self.reason = reason
        super().__init__(f"Navigation from '{from_page}' to '{to_page}' failed: {reason}")


class AuthenticationException(TestFrameworkException):
    """Raised when authentication fails"""
    def __init__(self, username, reason=None):
        self.username = username
        self.reason = reason
        super().__init__(f"Authentication failed for user '{username}': {reason}")


class DataNotFoundException(TestFrameworkException):
    """Raised when expected data is not found in the application"""
    def __init__(self, data_type, search_criteria):
        self.data_type = data_type
        self.search_criteria = search_criteria
        super().__init__(f"Data of type '{data_type}' not found with criteria: {search_criteria}")


class BrowserStateException(TestFrameworkException):
    """Raised when browser is in an unexpected state"""
    def __init__(self, expected_state, actual_state):
        self.expected_state = expected_state
        self.actual_state = actual_state
        super().__init__(f"Browser in unexpected state. Expected: {expected_state}, Actual: {actual_state}")


class RetryableException(TestFrameworkException):
    """Base class for exceptions that can be retried"""
    pass


class NetworkException(RetryableException):
    """Raised for network-related issues that might be transient"""
    def __init__(self, operation, reason):
        self.operation = operation
        self.reason = reason
        super().__init__(f"Network error during {operation}: {reason}")


class StaleElementException(RetryableException):
    """Raised when an element becomes stale between operations"""
    def __init__(self, element_name):
        self.element_name = element_name
        super().__init__(f"Element '{element_name}' became stale during operation") 