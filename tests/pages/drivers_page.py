import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class DriversPage(BasePage):
    """Page Object Model for the Drivers page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.drivers_url = f"{base_url}/drivers"

    def load(self):
        self.driver.get(self.drivers_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "drivers-table"))
        )
        logger.info(f"Loaded drivers page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "drivers-table"))
            )
            return True
        except TimeoutException:
            logger.error("Drivers table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_driver_button(self):
        try:
            add_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-success') and contains(., 'Add Driver')]") )
            )
            add_btn.click()
        except TimeoutException:
            logger.error("Add Driver button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        except Exception as e:
            logger.error(f"Unexpected error clicking Add Driver button: {e}\nPage source:\n{self.driver.page_source}")
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "driverForm"))
        )
        return self

    def fill_driver_form(self, driver_data):
        form = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "driverForm"))
        )
        field_map = {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "license": "license",
            # Add more mappings as needed based on the actual form
        }
        for key, value in driver_data.items():
            field_id = field_map.get(key, key)
            try:
                input_elem = form.find_element(By.XPATH, f'.//*[@id="{field_id}"] | .//*[@name="{field_id}"]')
                input_elem.clear()
                input_elem.send_keys(value)
            except Exception as e:
                logger.error(f"Field {field_id} not found in driver form. Error: {e}")
                raise

    def submit_driver_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='driverForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "drivers-table"))
        )
        return self

    def is_driver_in_table(self, driver_name):
        try:
            table = self.driver.find_element(By.ID, "drivers-table")
            return driver_name.lower() in table.text.lower()
        except Exception:
            return False

    def create_driver(self, driver_data):
        self.click_add_driver_button()
        self.fill_driver_form(driver_data)
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/button[contains(@type, "submit") and (contains(text(), "Save") or contains(text(), "Add") or contains(text(), "Submit"))]'))
        )
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="drivers-table"]//table'))
        )
        return self 

    def edit_driver(self, old_name, new_data):
        row = self.driver.find_element(By.XPATH, f'//*[@id="drivers-table"]//tr[td[contains(text(),"{old_name}")]]')
        edit_btn = row.find_element(By.XPATH, './/a[contains(@href, "edit")]')
        edit_btn.click()
        self.fill_driver_form(new_data)
        self.submit_driver_form()

    def delete_driver(self, name):
        row = self.driver.find_element(By.XPATH, f'//*[@id="drivers-table"]//tr[td[contains(text(),"{name}")]]')
        delete_btn = row.find_element(By.XPATH, './/a[contains(@href, "delete")]')
        delete_btn.click()
        WebDriverWait(self.driver, 5).until(EC.staleness_of(row))

    def search_driver(self, query):
        search_box = self.driver.find_element(By.ID, "search-box")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys("\n")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "drivers-table"), query)
        )

    def is_validation_error_displayed(self):
        return "This field is required" in self.driver.page_source or "required" in self.driver.page_source.lower() 