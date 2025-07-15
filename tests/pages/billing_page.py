import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class BillingPage(BasePage):
    """Page Object Model for the Billing page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.billing_url = f"{base_url}/billing"

    def load(self):
        self.driver.get(self.billing_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "billing-table"))
        )
        logger.info(f"Loaded billing page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "billing-table"))
            )
            return True
        except TimeoutException:
            logger.error("Billing table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_billing_button(self):
        try:
            add_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-success') and contains(., 'Add Billing')]") )
            )
            add_btn.click()
        except TimeoutException:
            logger.error("Add Billing button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        except Exception as e:
            logger.error(f"Unexpected error clicking Add Billing button: {e}\nPage source:\n{self.driver.page_source}")
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "billingForm"))
        )
        return self

    def fill_billing_form(self, billing_data):
        form = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "billingForm"))
        )
        field_map = {
            "customer": "customer",
            "amount": "amount",
            "date": "date",
            # Add more mappings as needed based on the actual form
        }
        for key, value in billing_data.items():
            field_id = field_map.get(key, key)
            try:
                input_elem = form.find_element(By.XPATH, f'.//*[@id="{field_id}"] | .//*[@name="{field_id}"]')
                input_elem.clear()
                input_elem.send_keys(value)
            except Exception as e:
                logger.error(f"Field {field_id} not found in billing form. Error: {e}")
                raise

    def submit_billing_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='billingForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "billing-table"))
        )
        return self

    def is_billing_in_table(self, billing_name):
        try:
            table = self.driver.find_element(By.ID, "billing-table")
            return billing_name.lower() in table.text.lower()
        except Exception:
            return False

    def create_billing(self, billing_data):
        self.click_add_billing_button()
        self.fill_billing_form(billing_data)
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/button[contains(@type, "submit") and (contains(text(), "Save") or contains(text(), "Add") or contains(text(), "Submit"))]'))
        )
        submit_btn.click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[contains(@class,"card-body")]/div[contains(@class,"table-responsive")]/table'))
        )
        return self 

    def edit_billing(self, old_name, new_data):
        row = self.driver.find_element(By.XPATH, f'//table[@id="billing-table"]//tr[td[contains(text(),"{old_name}")]]')
        edit_btn = row.find_element(By.XPATH, './/a[contains(@href, "edit")]')
        edit_btn.click()
        self.fill_billing_form(new_data)
        self.submit_billing_form()

    def delete_billing(self, name):
        row = self.driver.find_element(By.XPATH, f'//table[@id="billing-table"]//tr[td[contains(text(),"{name}")]]')
        delete_btn = row.find_element(By.XPATH, './/a[contains(@href, "delete")]')
        delete_btn.click()
        WebDriverWait(self.driver, 5).until(EC.staleness_of(row))

    def search_billing(self, query):
        search_box = self.driver.find_element(By.ID, "search-box")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys("\n")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "billing-table"), query)
        )

    def is_validation_error_displayed(self):
        return "This field is required" in self.driver.page_source or "required" in self.driver.page_source.lower() 