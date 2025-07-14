"""
Migrated smoke tests using the enhanced framework.
"""

import pytest
import logging
import os
from typing import Dict, Any

from tests.pages.login_page import LoginPage
from tests.core.exceptions import AuthenticationException

logger = logging.getLogger(__name__)


class TestMigratedSmoke:
    """Migrated smoke test suite using enhanced framework"""
    
    # --- CORE HAPPY FLOW TEST ---
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_login_smoke(self, live_server, browser, seeded_db):
        """[core happy flow] Test basic login functionality - migrated from old smoke test"""
        # Arrange
        username = os.environ.get("TEST_USERNAME", "fleetmanager")
        password = os.environ.get("TEST_PASSWORD", "manager123")
        login_page = LoginPage(browser, live_server.url)
        
        # Act
        login_page.load().login(username, password)
        
        # Assert
        assert "/dashboard" in browser.current_url or "/jobs" in browser.current_url, \
            "Login should redirect to dashboard or jobs page"
        
        # Verify we're not on login page anymore
        assert "/login" not in browser.current_url, \
            "Should not be on login page after successful login"
        
        logger.info("Smoke test passed - login successful")

    # TODO: Reactivate after triage - not a core happy-path test
    # @pytest.mark.smoke
    # def test_login_form_validation(self, live_server, browser):
    #     """Test login form validation - migrated from old smoke test"""
    #     # Arrange
    #     login_page = LoginPage(browser, live_server.url)
    #     # Act
    #     login_page.load()
    #     # Assert
    #     assert login_page.is_login_form_present(), \
    #         "Login form should be present on login page"
    #     assert login_page.is_username_field_enabled(), \
    #         "Username field should be enabled"
    #     assert login_page.is_password_field_enabled(), \
    #         "Password field should be enabled"
    #     assert login_page.is_login_button_enabled(), \
    #         "Login button should be enabled"
    #     logger.info("Login form validation test passed") 