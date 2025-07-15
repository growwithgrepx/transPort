import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class VehiclesPage(BasePage):
    """Page Object Model for the Vehicles page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.vehicles_url = f"{base_url}/vehicles"

    def load(self):
        self.driver.get(self.vehicles_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicles-table"))
        )
        logger.info(f"Loaded vehicles page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "card") or contains(@class, "container") or contains(text(), "Vehicle")]'))
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//tbody[@id="vehicles-table-body"]/ancestor::table'))
            )
            return True
        except TimeoutException:
            logger.error("Vehicles table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_vehicle_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add vehicle")] | //button[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add vehicle")]'))
            ).click()
        except TimeoutException:
            logger.error("Add Vehicle button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicleForm"))
        )
        return self

    def fill_vehicle_form(self, vehicle_data):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicleForm"))
        )
        for field_name, value in vehicle_data.items():
            try:
                field = self.driver.find_element(By.ID, field_name)
                field.clear()
                field.send_keys(str(value))
            except Exception as e:
                logger.warning(f"Error filling field {field_name}: {str(e)}")
                continue
        return self

    def submit_vehicle_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='vehicleForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "vehicles-table"))
        )
        return self

    def is_vehicle_in_table(self, vehicle_name):
        try:
            table = self.driver.find_element(By.ID, "vehicles-table")
            return vehicle_name.lower() in table.text.lower()
        except Exception:
            return False

    def create_vehicle(self, vehicle_data):
        self.click_add_vehicle_button()
        self.fill_vehicle_form(vehicle_data)
        self.submit_vehicle_form()
        return self 