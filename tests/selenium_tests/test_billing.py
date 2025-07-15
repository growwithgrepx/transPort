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
        {"name": "Billing A", "amount": "100.00", "currency": "USD"},
        {"name": "Billing B", "amount": "200.00", "currency": "EUR"},
    ])
    def test_create_billing(self, live_server, browser, billing_data):
        billing_page = BillingPage(browser, live_server.url)
        billing_page.load()
        billing_page.create_billing(billing_data)
        assert billing_page.is_billing_in_table(billing_data["name"]), f"Billing {billing_data['name']} should appear in the billing table." 