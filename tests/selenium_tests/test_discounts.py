import pytest
from tests.pages.login_page import LoginPage
from tests.pages.discounts_page import DiscountsPage

@pytest.mark.feature("discounts")
class TestDiscountsCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_discounts_page_loads(self, live_server, browser):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        assert discounts_page.is_loaded(), "Discounts page should load and display the discounts table."

    @pytest.mark.regression
    @pytest.mark.parametrize("discount_data", [
        {"code": "DISC10", "percent": "10.0"},
        {"code": "DISC20", "percent": "20.0"},
    ])
    def test_create_discount(self, live_server, browser, discount_data):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.create_discount(discount_data)
        assert discounts_page.is_discount_in_table(discount_data["code"]), f"Discount {discount_data['code']} should appear in the discounts table." 