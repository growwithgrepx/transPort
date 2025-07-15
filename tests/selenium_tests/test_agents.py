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
        assert agents_page.is_agent_in_table(agent_data["name"]), f"Agent {agent_data['name']} should appear in the agents table." 