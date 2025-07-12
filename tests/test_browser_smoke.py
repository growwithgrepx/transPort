import pytest
import os
from .pages.login_page import LoginPage
import logging

logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("seeded_db")
def test_login_smoke(live_server, browser):
    username = os.environ.get("TEST_USERNAME", "fleetmanager")
    password = os.environ.get("TEST_PASSWORD", "manager123")
    login_page = LoginPage(browser, live_server)
    login_page.load()
    try:
        login_page.login(username, password)
        assert "/dashboard" in browser.current_url
    except Exception as e:
        logger.error(f"Smoke test failed: {e}")
        browser.save_screenshot("test_screenshots/smoke_failure.png")
        raise 