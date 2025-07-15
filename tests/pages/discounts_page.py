import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class DiscountsPage(BasePage):
    """Page Object Model for the Discounts page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.discounts_url = f"{base_url}/discounts"

    def load(self):
        self.driver.get(self.discounts_url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "discounts-table"))
        )
        logger.info(f"Loaded discounts page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[contains(@class, "card") or contains(@class, "container") or contains(text(), "Discount")]'))
            )
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"card-body")]/div[contains(@class,"table-responsive")]/table'))
            )
            return True
        except TimeoutException:
            logger.error("Discounts table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_discount_button(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add discount")] | //button[contains(@class, "btn") and contains(translate(text(), "ADD", "add"), "add discount")]'))
            ).click()
        except TimeoutException:
            logger.error("Add Discount button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "discountForm"))
        )
        return self

    def fill_discount_form(self, discount_data):
        form = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "discountForm"))
        )
        field_map = {
            "name": "name",
            "amount": "amount",
            "type": "type",
            # Add more mappings as needed based on the actual form
        }
        for key, value in discount_data.items():
            field_id = field_map.get(key, key)
            try:
                input_elem = form.find_element(By.XPATH, f'.//*[@id="{field_id}"] | .//*[@name="{field_id}"]')
                input_elem.clear()
                input_elem.send_keys(value)
            except Exception as e:
                logger.error(f"Field {field_id} not found in discount form. Error: {e}")
                raise

    def submit_discount_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='discountForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "discounts-table"))
        )
        return self

    def discount_in_table(self, code):
        try:
            row = self.driver.find_element(By.XPATH, f'//div[contains(@class,"card-body")]/div[contains(@class,"table-responsive")]/table//tr[td[text()="{code}"]]')
            return row is not None
        except NoSuchElementException:
            return False

    def create_discount(self, discount_data):
        self.click_add_discount_button()
        self.fill_discount_form(discount_data)
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/button[contains(@type, "submit") and (contains(text(), "Save") or contains(text(), "Add") or contains(text(), "Submit"))]'))
        )
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"card-body")]/div[contains(@class,"table-responsive")]/table'))
        )
        return self 