import pytest
from tests.pages.login_page import LoginPage
from tests.pages.drivers_page import DriversPage

@pytest.mark.feature("drivers")
class TestDriversCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_drivers_page_loads(self, live_server, browser):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        assert drivers_page.is_loaded(), "Drivers page should load and display the drivers table."

    @pytest.mark.regression
    @pytest.mark.parametrize("driver_data", [
        {"name": "Driver A", "phone": "11111111"},
        {"name": "Driver B", "phone": "22222222"},
    ])
    def test_create_driver(self, live_server, browser, driver_data):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        drivers_page.create_driver(driver_data)
        assert drivers_page.is_driver_in_table(driver_data["name"]), f"Driver {driver_data['name']} should appear in the drivers table."

    def test_edit_driver(self, live_server, browser):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        drivers_page.create_driver({"name": "EditMe", "phone": "12345678"})
        drivers_page.edit_driver("EditMe", {"name": "Edited Driver", "phone": "87654321"})
        assert drivers_page.is_driver_in_table("Edited Driver"), "Edited driver should appear in the table."

    def test_delete_driver(self, live_server, browser):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        drivers_page.create_driver({"name": "DeleteMe", "phone": "12345678"})
        drivers_page.delete_driver("DeleteMe")
        assert not drivers_page.is_driver_in_table("DeleteMe"), "Deleted driver should not appear in the table."

    def test_search_driver(self, live_server, browser):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        drivers_page.create_driver({"name": "Searchable", "phone": "12345678"})
        drivers_page.search_driver("Searchable")
        assert drivers_page.is_driver_in_table("Searchable"), "Search should return the correct driver."

    def test_driver_form_validation(self, live_server, browser):
        drivers_page = DriversPage(browser, live_server.url)
        drivers_page.load()
        drivers_page.click_add_driver_button()
        drivers_page.fill_driver_form({"name": "", "phone": ""})  # Intentionally invalid
        drivers_page.submit_driver_form()
        assert drivers_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 