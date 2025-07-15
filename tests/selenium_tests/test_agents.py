import pytest
from tests.pages.login_page import LoginPage
from tests.pages.agents_page import AgentsPage

@pytest.mark.feature("agents")
class TestAgentsCRUD:
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        login_page = LoginPage(browser, live_server.url)
        login_page.load()
        login_page.login("fleetmanager", "manager123")

    @pytest.mark.smoke
    def test_agents_page_loads(self, live_server, browser):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        assert agents_page.is_loaded(), "Agents page should load and display the agents table."

    @pytest.mark.regression
    @pytest.mark.parametrize("agent_data", [
        {"name": "Agent A", "email": "a@example.com"},
        {"name": "Agent B", "email": "b@example.com"},
    ])
    def test_create_agent(self, live_server, browser, agent_data):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        agents_page.create_agent(agent_data)
        assert agents_page.agent_in_table(agent_data["name"]), f"Agent {agent_data['name']} should appear in the agents table."

    def test_edit_agent(self, live_server, browser):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        agents_page.create_agent({"name": "EditMe", "email": "editme@example.com"})
        agents_page.edit_agent("EditMe", {"name": "Edited Agent", "email": "edited@example.com"})
        assert agents_page.agent_in_table("Edited Agent"), "Edited agent should appear in the table."

    def test_delete_agent(self, live_server, browser):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        agents_page.create_agent({"name": "DeleteMe", "email": "deleteme@example.com"})
        agents_page.delete_agent("DeleteMe")
        assert not agents_page.agent_in_table("DeleteMe"), "Deleted agent should not appear in the table."

    def test_search_agent(self, live_server, browser):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        agents_page.create_agent({"name": "Searchable", "email": "searchable@example.com"})
        agents_page.search_agent("Searchable")
        assert agents_page.agent_in_table("Searchable"), "Search should return the correct agent."

    def test_agent_form_validation(self, live_server, browser):
        agents_page = AgentsPage(browser, live_server.url)
        agents_page.load()
        agents_page.click_add_agent_button()
        agents_page.fill_agent_form({"name": "", "email": ""})  # Intentionally invalid
        agents_page.submit_agent_form()
        assert agents_page.is_validation_error_displayed(), "Validation error should be displayed for empty fields." 