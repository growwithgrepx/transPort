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
        {"name": "DISC10", "amount": "10.0", "type": "Percent"},
        {"name": "DISC20", "amount": "20.0", "type": "Flat"},
    ])
    def test_create_discount(self, live_server, browser, discount_data):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.create_discount(discount_data)
        assert discounts_page.discount_in_table(discount_data["name"]), f"Discount {discount_data['name']} should appear in the discounts table."

    def test_edit_discount(self, live_server, browser):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.create_discount({"name": "EditMe", "amount": "5.0", "type": "Percent"})
        discounts_page.edit_discount("EditMe", {"name": "Edited Discount", "amount": "15.0", "type": "Flat"})
        assert discounts_page.discount_in_table("Edited Discount"), "Edited discount should appear in the table."

    def test_delete_discount(self, live_server, browser):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.create_discount({"name": "DeleteMe", "amount": "5.0", "type": "Percent"})
        discounts_page.delete_discount("DeleteMe")
        assert not discounts_page.discount_in_table("DeleteMe"), "Deleted discount should not appear in the table."

    def test_search_discount(self, live_server, browser):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.create_discount({"name": "Searchable", "amount": "5.0", "type": "Percent"})
        discounts_page.search_discount("Searchable")
        assert discounts_page.discount_in_table("Searchable"), "Search should return the correct discount."

    def test_discount_form_validation(self, live_server, browser):
        discounts_page = DiscountsPage(browser, live_server.url)
        discounts_page.load()
        discounts_page.click_add_discount_button()
        discounts_page.fill_discount_form({"name": "", "amount": ""})  # Intentionally invalid
        discounts_page.submit_discount_form()
        assert discounts_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 