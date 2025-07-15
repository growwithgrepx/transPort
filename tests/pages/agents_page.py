import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage

logger = logging.getLogger(__name__)

class AgentsPage(BasePage):
    """Page Object Model for the Agents page"""
    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)
        self.agents_url = f"{base_url}/agents"

    def load(self):
        self.driver.get(self.agents_url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "agents-table"))
        )
        logger.info(f"Loaded agents page: {self.driver.current_url}")
        return self

    def wait_for_page_ready(self, timeout=20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_loaded(self):
        try:
            self.wait_for_page_ready()
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, "agents-table"))
            )
            return True
        except TimeoutException:
            logger.error("Agents table not found on page load. Page source:\n%s", self.driver.page_source)
            return False

    def click_add_agent_button(self):
        try:
            add_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'btn-success') and contains(., 'Add Agent')]") )
            )
            add_btn.click()
        except TimeoutException:
            logger.error("Add Agent button not found or not clickable. Page source:\n%s", self.driver.page_source)
            raise
        except Exception as e:
            logger.error(f"Unexpected error clicking Add Agent button: {e}\nPage source:\n{self.driver.page_source}")
            raise
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "agentForm"))
        )
        return self

    def fill_agent_form(self, agent_data):
        form = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "agentForm"))
        )
        # Map test data keys to actual form field IDs/names as per form_debug.html
        field_map = {
            "name": "name",
            "email": "email",
            "phone": "phone",
            "address": "address",
            # Add more mappings as needed based on the actual form
        }
        for key, value in agent_data.items():
            field_id = field_map.get(key, key)
            try:
                input_elem = form.find_element(By.XPATH, f'.//*[@id="{field_id}"] | .//*[@name="{field_id}"]')
                input_elem.clear()
                input_elem.send_keys(value)
            except Exception as e:
                logger.error(f"Field {field_id} not found in agent form. Error: {e}")
                raise

    def submit_agent_form(self):
        submit_btn = self.driver.find_element(By.XPATH, "//form[@id='agentForm']//button[@type='submit']")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
        submit_btn.click()
        # Wait for redirect or table update
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "agents-table"))
        )
        return self

    def agent_in_table(self, agent_name):
        # Use XPath to find agent row
        try:
            row = self.driver.find_element(By.XPATH, f'//*[@id="agents-table"]//table//tr[td[text()="{agent_name}"]]')
            return row is not None
        except NoSuchElementException:
            return False

    def create_agent(self, agent_data):
        self.click_add_agent_button()
        self.fill_agent_form(agent_data)
        # Wait for submit button and click
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, './/button[contains(@type, "submit") and (contains(text(), "Save") or contains(text(), "Add") or contains(text(), "Submit"))]'))
        )
        submit_btn.click()
        # Wait for the table to update or a success message
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="agents-table"]//table'))
        )
        return self

    def edit_agent(self, old_name, new_data):
        # Find the row for old_name, click the edit button, fill the form, submit
        row = self.driver.find_element(By.XPATH, f'//*[@id="agents-table"]//tr[td[text()="{old_name}"]]')
        edit_btn = row.find_element(By.XPATH, './/a[contains(@href, "edit")]')
        edit_btn.click()
        self.fill_agent_form(new_data)
        self.submit_agent_form()

    def delete_agent(self, name):
        row = self.driver.find_element(By.XPATH, f'//*[@id="agents-table"]//tr[td[text()="{name}"]]')
        delete_btn = row.find_element(By.XPATH, './/a[contains(@href, "delete")]')
        delete_btn.click()
        # Confirm the deletion if a modal/dialog appears (customize as needed)
        WebDriverWait(self.driver, 5).until(EC.staleness_of(row))

    def search_agent(self, query):
        search_box = self.driver.find_element(By.ID, "search-box")
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys("\n")
        WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.ID, "agents-table"), query)
        )

    def is_validation_error_displayed(self):
        # Looks for a generic required field error
        return "This field is required" in self.driver.page_source or "required" in self.driver.page_source.lower() 