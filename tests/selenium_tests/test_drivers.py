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