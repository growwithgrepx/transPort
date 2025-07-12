"""
Migrated CRUD tests using the enhanced framework.
Fixed edit button selector and improved error handling.
"""

import pytest
import logging
from typing import Dict, Any
from selenium.webdriver.common.by import By

from .pages.login_page_v2 import LoginPage
from .pages.jobs_page_v2 import JobsPage
from .core.exceptions import (
    AuthenticationException,
    FormValidationException,
    ElementNotFoundException,
    DataNotFoundException
)

logger = logging.getLogger(__name__)


class TestMigratedJobsCRUD:
    """Migrated CRUD test suite using enhanced framework"""
    
    @pytest.fixture(autouse=True)
    def setup_login(self, live_server, browser, seeded_db):
        """Setup login for all jobs tests"""
        login_page = LoginPage(browser, live_server)
        login_page.load()
        login_page.login("fleetmanager", "manager123")
        return login_page

    # --- CORE HAPPY FLOW TEST ---
    @pytest.mark.smoke
    @pytest.mark.critical
    def test_jobs_crud_operations(self, live_server, browser, seeded_db):
        """[core happy flow] Test basic job creation - minimal happy path"""
        # Arrange
        jobs_page = JobsPage(browser, live_server)
        jobs_page.load()

        # Get seeded data
        agent = seeded_db['agent']
        service = seeded_db['service']
        vehicle = seeded_db['vehicle']
        driver = seeded_db['driver']

        # Minimal job data for happy path
        job_data = {
            "agent_name": agent.name,
            "service_name": service.name,
            "pickup_date": "2025-07-12",
            "pickup_time": "10:00",
            "pickup_location": "Test Pickup Location",
            "dropoff_location": "Test Dropoff Location",
            "vehicle_name": f"{vehicle.name} ({vehicle.number})",
            "driver_name": f"{driver.name} ({driver.phone})"
        }

        # Get initial jobs count
        initial_count = jobs_page.get_jobs_count()

        # --- CREATE ---
        logger.info("Starting job creation test...")

        # Create job using fluent interface
        jobs_page.click_add_job_button() \
                 .wait_for_job_form() \
                 .fill_agent_name(job_data["agent_name"]) \
                 .fill_service_name(job_data["service_name"]) \
                 .fill_vehicle_name(job_data["vehicle_name"]) \
                 .fill_driver_name(job_data["driver_name"]) \
                 .fill_pickup_date(job_data["pickup_date"]) \
                 .fill_pickup_time(job_data["pickup_time"]) \
                 .fill_pickup_location(job_data["pickup_location"]) \
                 .fill_dropoff_location(job_data["dropoff_location"]) \
                 .click_submit_button()

        # Always reload jobs page after submit to ensure we see the new job
        jobs_page.load()

        # Verify job count increased
        final_count = jobs_page.get_jobs_count()
        assert final_count > initial_count, f"Job count should increase from {initial_count} to {final_count}"

        # Verify job appears in table
        search_criteria = {
            "pickup_location": job_data["pickup_location"],
            "dropoff_location": job_data["dropoff_location"]
        }
        assert jobs_page.is_job_in_table(search_criteria), "Created job should appear in jobs table" 