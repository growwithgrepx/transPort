import pytest
from tests.pages.login_page import LoginPage
from tests.pages.vehicles_page import VehiclesPage

@pytest.mark.feature("vehicles")
class TestVehiclesCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_vehicles_page_loads(self, live_server, browser):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        assert vehicles_page.is_loaded(), "Vehicles page should load and display the vehicles table."

    @pytest.mark.regression
    @pytest.mark.parametrize("vehicle_data", [
        {"registration": "AAA111", "make": "Toyota", "model": "Hiace", "year": "2020"},
        {"registration": "BBB222", "make": "Ford", "model": "Transit", "year": "2021"},
    ])
    def test_create_vehicle(self, live_server, browser, vehicle_data):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.create_vehicle(vehicle_data)
        assert vehicles_page.is_vehicle_in_table(vehicle_data["registration"]), f"Vehicle {vehicle_data['registration']} should appear in the vehicles table."

    def test_edit_vehicle(self, live_server, browser):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.create_vehicle({"registration": "EDIT123", "make": "Test", "model": "Edit", "year": "2022"})
        vehicles_page.edit_vehicle("EDIT123", {"registration": "EDITED123", "make": "Test", "model": "Edited", "year": "2023"})
        assert vehicles_page.is_vehicle_in_table("EDITED123"), "Edited vehicle should appear in the table."

    def test_delete_vehicle(self, live_server, browser):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.create_vehicle({"registration": "DEL123", "make": "Test", "model": "Del", "year": "2022"})
        vehicles_page.delete_vehicle("DEL123")
        assert not vehicles_page.is_vehicle_in_table("DEL123"), "Deleted vehicle should not appear in the table."

    def test_search_vehicle(self, live_server, browser):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.create_vehicle({"registration": "SEARCH123", "make": "Test", "model": "Search", "year": "2022"})
        vehicles_page.search_vehicle("SEARCH123")
        assert vehicles_page.is_vehicle_in_table("SEARCH123"), "Search should return the correct vehicle."

    def test_vehicle_form_validation(self, live_server, browser):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.click_add_vehicle_button()
        vehicles_page.fill_vehicle_form({"registration": "", "make": ""})  # Intentionally invalid
        vehicles_page.submit_vehicle_form()
        assert vehicles_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 