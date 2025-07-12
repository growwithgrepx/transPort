"""
Centralized locator management for the Selenium test framework.
Separates element locators from page logic for better maintainability.
"""

from selenium.webdriver.common.by import By
from typing import Tuple, Dict, Any


class Locator:
    """Represents a web element locator with metadata"""
    
    def __init__(self, by: By, value: str, name: str = None, description: str = None):
        self.by = by
        self.value = value
        self.name = name or value
        self.description = description
    
    def __str__(self):
        return f"{self.by}={self.value}"
    
    def __repr__(self):
        return f"Locator({self.by}, '{self.value}', name='{self.name}')"


class LoginPageLocators:
    """Locators for the Login page"""
    
    USERNAME_FIELD = Locator(By.ID, "username", "Username Field", "Username input field")
    PASSWORD_FIELD = Locator(By.ID, "password", "Password Field", "Password input field")
    SUBMIT_BUTTON = Locator(By.XPATH, "//button[@type='submit']", "Submit Button", "Login form submit button")
    ERROR_MESSAGE = Locator(By.CLASS_NAME, "alert-danger", "Error Message", "Login error message")
    SUCCESS_MESSAGE = Locator(By.CLASS_NAME, "alert-success", "Success Message", "Login success message")
    LOGIN_FORM = Locator(By.TAG_NAME, "form", "Login Form", "Login form container")


class JobsPageLocators:
    """Locators for the Jobs page"""
    
    # Table and navigation
    JOBS_TABLE = Locator(By.ID, "jobs-table", "Jobs Table", "Main jobs listing table")
    ADD_JOB_BUTTON = Locator(By.XPATH, "//a[contains(@href, '/jobs/add')]", "Add Job Button", "Button to add new job")
    SEARCH_INPUT = Locator(By.ID, "searchInput", "Search Input", "Job search input field")
    
    # Form elements
    JOB_FORM = Locator(By.ID, "jobForm", "Job Form", "Job creation/editing form")
    SUBMIT_BUTTON = Locator(By.XPATH, "//form[@id='jobForm']//button[@type='submit']", "Submit Button", "Form submit button")
    
    # Form fields
    AGENT_NAME_FIELD = Locator(By.ID, "agent_name", "Agent Name Field", "Agent name input field")
    SERVICE_NAME_FIELD = Locator(By.ID, "service_name", "Service Name Field", "Service name input field")
    VEHICLE_NAME_FIELD = Locator(By.ID, "vehicle_name", "Vehicle Name Field", "Vehicle name input field")
    DRIVER_NAME_FIELD = Locator(By.ID, "driver_name", "Driver Name Field", "Driver name input field")
    PICKUP_DATE_FIELD = Locator(By.ID, "pickup_date", "Pickup Date Field", "Pickup date input field")
    PICKUP_TIME_FIELD = Locator(By.ID, "pickup_time", "Pickup Time Field", "Pickup time input field")
    PICKUP_LOCATION_FIELD = Locator(By.ID, "pickup_location", "Pickup Location Field", "Pickup location input field")
    DROPOFF_LOCATION_FIELD = Locator(By.ID, "dropoff_location", "Dropoff Location Field", "Dropoff location input field")
    CUSTOMER_NAME_FIELD = Locator(By.ID, "customer_name", "Customer Name Field", "Customer name input field")
    CUSTOMER_EMAIL_FIELD = Locator(By.ID, "customer_email", "Customer Email Field", "Customer email input field")
    CUSTOMER_MOBILE_FIELD = Locator(By.ID, "customer_mobile", "Customer Mobile Field", "Customer mobile input field")
    REMARKS_FIELD = Locator(By.ID, "remarks", "Remarks Field", "Job remarks input field")
    STATUS_FIELD = Locator(By.ID, "status", "Status Field", "Job status select field")
    
    # Hidden/readonly fields
    AGENT_ID_FIELD = Locator(By.ID, "agent_id", "Agent ID Field", "Hidden agent ID field")
    
    # Validation and messages
    VALIDATION_ERRORS = Locator(By.CLASS_NAME, "invalid-feedback", "Validation Errors", "Form validation error messages")
    SUCCESS_MESSAGE = Locator(By.CLASS_NAME, "alert-success", "Success Message", "Success message after form submission")
    ERROR_MESSAGE = Locator(By.CLASS_NAME, "alert-danger", "Error Message", "Error message after form submission")
    
    # Table actions
    EDIT_BUTTON = Locator(By.XPATH, "//table[@id='jobs-table']//tr[1]//a[contains(@href, 'edit')]", "Edit Button", "Edit job button")
    DELETE_BUTTON = Locator(By.XPATH, "//button[contains(@class, 'btn-danger')]", "Delete Button", "Delete job button")
    
    # Advanced fields section
    ADVANCED_FIELDS = Locator(By.ID, "advanced-fields", "Advanced Fields", "Advanced fields section")


class DashboardLocators:
    """Locators for the Dashboard page"""
    
    DASHBOARD_CONTAINER = Locator(By.ID, "dashboard", "Dashboard Container", "Main dashboard container")
    NAVIGATION_MENU = Locator(By.CLASS_NAME, "navbar", "Navigation Menu", "Main navigation menu")
    LOGOUT_BUTTON = Locator(By.XPATH, "//a[contains(@href, '/logout')]", "Logout Button", "Logout link")


class CommonLocators:
    """Common locators used across multiple pages"""
    
    # Navigation
    NAVBAR = Locator(By.CLASS_NAME, "navbar", "Navigation Bar", "Main navigation bar")
    SIDEBAR = Locator(By.CLASS_NAME, "sidebar", "Sidebar", "Side navigation panel")
    
    # Messages
    ALERT_SUCCESS = Locator(By.CLASS_NAME, "alert-success", "Success Alert", "Success message alert")
    ALERT_DANGER = Locator(By.CLASS_NAME, "alert-danger", "Danger Alert", "Error message alert")
    ALERT_WARNING = Locator(By.CLASS_NAME, "alert-warning", "Warning Alert", "Warning message alert")
    ALERT_INFO = Locator(By.CLASS_NAME, "alert-info", "Info Alert", "Information message alert")
    
    # Loading states
    LOADING_SPINNER = Locator(By.CLASS_NAME, "spinner", "Loading Spinner", "Loading indicator")
    LOADING_OVERLAY = Locator(By.CLASS_NAME, "loading-overlay", "Loading Overlay", "Loading overlay")
    
    # Modal dialogs
    MODAL = Locator(By.CLASS_NAME, "modal", "Modal Dialog", "Modal dialog container")
    MODAL_CLOSE_BUTTON = Locator(By.CLASS_NAME, "close", "Modal Close Button", "Modal close button")
    
    # Form elements
    FORM = Locator(By.TAG_NAME, "form", "Form", "Generic form container")
    SUBMIT_BUTTON = Locator(By.XPATH, "//button[@type='submit']", "Submit Button", "Generic submit button")
    CANCEL_BUTTON = Locator(By.XPATH, "//button[@type='button' and contains(text(), 'Cancel')]", "Cancel Button", "Generic cancel button")


class LocatorRegistry:
    """Registry for managing all locators"""
    
    def __init__(self):
        self._locators = {}
        self._register_default_locators()
    
    def _register_default_locators(self):
        """Register all default locators"""
        self.register_page_locators("login", LoginPageLocators)
        self.register_page_locators("jobs", JobsPageLocators)
        self.register_page_locators("dashboard", DashboardLocators)
        self.register_page_locators("common", CommonLocators)
    
    def register_page_locators(self, page_name: str, locator_class):
        """Register locators for a specific page"""
        self._locators[page_name] = {}
        for attr_name in dir(locator_class):
            if not attr_name.startswith('_'):
                attr_value = getattr(locator_class, attr_name)
                if isinstance(attr_value, Locator):
                    self._locators[page_name][attr_name] = attr_value
    
    def get_locator(self, page_name: str, locator_name: str) -> Locator:
        """Get a specific locator by page and name"""
        if page_name not in self._locators:
            raise KeyError(f"Page '{page_name}' not found in locator registry")
        
        if locator_name not in self._locators[page_name]:
            raise KeyError(f"Locator '{locator_name}' not found in page '{page_name}'")
        
        return self._locators[page_name][locator_name]
    
    def get_page_locators(self, page_name: str) -> Dict[str, Locator]:
        """Get all locators for a specific page"""
        if page_name not in self._locators:
            raise KeyError(f"Page '{page_name}' not found in locator registry")
        
        return self._locators[page_name].copy()
    
    def list_pages(self) -> list:
        """List all registered pages"""
        return list(self._locators.keys())
    
    def list_locators(self, page_name: str) -> list:
        """List all locators for a specific page"""
        if page_name not in self._locators:
            raise KeyError(f"Page '{page_name}' not found in locator registry")
        
        return list(self._locators[page_name].keys())


# Global locator registry instance
locator_registry = LocatorRegistry()


def get_locator(page_name: str, locator_name: str) -> Locator:
    """Convenience function to get a locator"""
    return locator_registry.get_locator(page_name, locator_name)


def get_page_locators(page_name: str) -> Dict[str, Locator]:
    """Convenience function to get all locators for a page"""
    return locator_registry.get_page_locators(page_name) 