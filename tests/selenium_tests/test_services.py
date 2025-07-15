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
        {"name": "Service A", "description": "Desc A", "price": "100"},
        {"name": "Service B", "description": "Desc B", "price": "200"},
    ])
    def test_create_service(self, live_server, browser, service_data):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.create_service(service_data)
        assert services_page.service_in_table(service_data["name"]), f"Service {service_data['name']} should appear in the services table."

    def test_edit_service(self, live_server, browser):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.create_service({"name": "EditMe", "description": "Edit", "price": "123"})
        services_page.edit_service("EditMe", {"name": "Edited Service", "description": "Edited", "price": "456"})
        assert services_page.service_in_table("Edited Service"), "Edited service should appear in the table."

    def test_delete_service(self, live_server, browser):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.create_service({"name": "DeleteMe", "description": "Del", "price": "123"})
        services_page.delete_service("DeleteMe")
        assert not services_page.service_in_table("DeleteMe"), "Deleted service should not appear in the table."

    def test_search_service(self, live_server, browser):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.create_service({"name": "Searchable", "description": "Search", "price": "123"})
        services_page.search_service("Searchable")
        assert services_page.service_in_table("Searchable"), "Search should return the correct service."

    def test_service_form_validation(self, live_server, browser):
        services_page = ServicesPage(browser, live_server.url)
        services_page.load()
        services_page.click_add_service_button()
        services_page.fill_service_form({"name": "", "description": ""})  # Intentionally invalid
        services_page.submit_service_form()
        assert services_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 