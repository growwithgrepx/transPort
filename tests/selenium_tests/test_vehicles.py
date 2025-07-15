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
        {"name": "Vehicle A", "number": "AAA111", "type": "Van", "status": "Active"},
        {"name": "Vehicle B", "number": "BBB222", "type": "Truck", "status": "Inactive"},
    ])
    def test_create_vehicle(self, live_server, browser, vehicle_data):
        vehicles_page = VehiclesPage(browser, live_server.url)
        vehicles_page.load()
        vehicles_page.create_vehicle(vehicle_data)
        assert vehicles_page.is_vehicle_in_table(vehicle_data["name"]), f"Vehicle {vehicle_data['name']} should appear in the vehicles table." 