import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class ServicesPage(BasePage):
    """Page Object Model for the Services page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.services_url = f"{base_url}/services"

    def load(self):
        self.driver.get(self.services_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "services-table"))
        )
        logger.info(f"Loaded services page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "card") or contains(@class, "container") or contains(text(), "Service")]'))
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//tbody[@id="services-table-body"]/ancestor::table'))
            )
            return True
        except TimeoutException:
            logger.error("Services table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_service_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add service")] | //button[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add service")]'))
            ).click()
        except TimeoutException:
            logger.error("Add Service button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "serviceForm"))
        )
        return self

    def fill_service_form(self, service_data):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "serviceForm"))
        )
        for field_name, value in service_data.items():
            try:
                field = self.driver.find_element(By.ID, field_name)
                field.clear()
                field.send_keys(str(value))
            except Exception as e:
                logger.warning(f"Error filling field {field_name}: {str(e)}")
                continue
        return self

    def submit_service_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='serviceForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "services-table"))
        )
        return self

    def service_in_table(self, service_name):
        try:
            row = self.driver.find_element(By.XPATH, f'//tbody[@id="services-table-body"]/tr[td[text()="{service_name}"]]')
            return row is not None
        except NoSuchElementException:
            return False

    def create_service(self, service_data):
        self.click_add_service_button()
        self.fill_service_form(service_data)
        self.submit_service_form()
        return self 