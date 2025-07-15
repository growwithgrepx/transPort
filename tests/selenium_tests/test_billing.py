import pytest
from tests.pages.login_page import LoginPage
from tests.pages.billing_page import BillingPage

@pytest.mark.feature("billing")
class TestBillingCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_billing_page_loads(self, live_server, browser):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        assert billing_page.is_loaded(), "Billing page should load and display the billing table."

    @pytest.mark.regression
    @pytest.mark.parametrize("billing_data", [
        {"customer": "Customer A", "amount": "100.00", "date": "2023-01-01"},
        {"customer": "Customer B", "amount": "200.00", "date": "2023-02-01"},
    ])
    def test_create_billing(self, live_server, browser, billing_data):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.create_billing(billing_data)
        assert billing_page.is_billing_in_table(billing_data["customer"]), f"Billing {billing_data['customer']} should appear in the billing table."

    def test_edit_billing(self, live_server, browser):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.create_billing({"customer": "EditMe", "amount": "123.45", "date": "2023-03-01"})
        billing_page.edit_billing("EditMe", {"customer": "Edited Customer", "amount": "543.21", "date": "2023-04-01"})
        assert billing_page.is_billing_in_table("Edited Customer"), "Edited billing should appear in the table."

    def test_delete_billing(self, live_server, browser):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.create_billing({"customer": "DeleteMe", "amount": "123.45", "date": "2023-03-01"})
        billing_page.delete_billing("DeleteMe")
        assert not billing_page.is_billing_in_table("DeleteMe"), "Deleted billing should not appear in the table."

    def test_search_billing(self, live_server, browser):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.create_billing({"customer": "Searchable", "amount": "123.45", "date": "2023-03-01"})
        billing_page.search_billing("Searchable")
        assert billing_page.is_billing_in_table("Searchable"), "Search should return the correct billing."

    def test_billing_form_validation(self, live_server, browser):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.click_add_billing_button()
        billing_page.fill_billing_form({"customer": "", "amount": ""})  # Intentionally invalid
        billing_page.submit_billing_form()
        assert billing_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 