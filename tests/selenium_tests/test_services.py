import pytest
from tests.pages.login_page import LoginPage
from tests.pages.services_page import ServicesPage

@pytest.mark.feature("services")
class TestServicesCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_services_page_loads(self, live_server, browser):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        assert services_page.is_loaded(), "Services page should load and display the services table."

    @pytest.mark.regression
    @pytest.mark.parametrize("service_data", [
        {"name": "Service A", "description": "Desc A", "status": "Active"},
        {"name": "Service B", "description": "Desc B", "status": "Inactive"},
    ])
    def test_create_service(self, live_server, browser, service_data):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.create_service(service_data)
        assert services_page.is_service_in_table(service_data["name"]), f"Service {service_data['name']} should appear in the services table." 