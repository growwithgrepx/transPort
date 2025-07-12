"""
Configuration management for the enhanced test framework.
Centralized settings for different environments and test categories.
"""

import os
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class BrowserConfig:
    """Browser configuration settings"""
    headless: bool = True
    window_size: str = "1920,1080"
    implicit_wait: int = 10
    page_load_timeout: int = 30
    script_timeout: int = 30
    accept_insecure_certs: bool = True
    disable_gpu: bool = True
    no_sandbox: bool = True
    disable_dev_shm_usage: bool = True


@dataclass
class WaitConfig:
    """Wait configuration settings"""
    default_timeout: int = 10
    short_timeout: int = 5
    long_timeout: int = 20
    poll_frequency: float = 0.5
    retry_attempts: int = 3
    retry_delay: float = 1.0


@dataclass
class TestConfig:
    """Test configuration settings"""
    screenshot_on_failure: bool = True
    screenshot_on_success: bool = False
    capture_html_on_failure: bool = True
    max_screenshot_age_days: int = 3
    max_screenshots: int = 20
    parallel_execution: bool = False
    parallel_workers: int = 4


@dataclass
class EnvironmentConfig:
    """Environment-specific configuration"""
    base_url: str
    database_url: str
    test_username: str
    test_password: str
    admin_username: str
    admin_password: str


class TestFrameworkConfig:
    """Main configuration class for the test framework"""
    
    def __init__(self):
        self.browser = BrowserConfig()
        self.wait = WaitConfig()
        self.test = TestConfig()
        self.environments = self._load_environment_configs()
        self.current_environment = os.getenv('TEST_ENV', 'test')
    
    def _load_environment_configs(self) -> Dict[str, EnvironmentConfig]:
        """Load environment-specific configurations"""
        return {
            'test': EnvironmentConfig(
                base_url='http://127.0.0.1:5001',
                database_url='sqlite:///:memory:',
                test_username='fleetmanager',
                test_password='manager123',
                admin_username='admin',
                admin_password='admin123'
            ),
            'development': EnvironmentConfig(
                base_url='http://localhost:5000',
                database_url='sqlite:///dev.db',
                test_username='fleetmanager',
                test_password='manager123',
                admin_username='admin',
                admin_password='admin123'
            ),
            'staging': EnvironmentConfig(
                base_url=os.getenv('STAGING_URL', 'https://staging.example.com'),
                database_url=os.getenv('STAGING_DATABASE_URL', ''),
                test_username=os.getenv('STAGING_TEST_USER', 'testuser'),
                test_password=os.getenv('STAGING_TEST_PASS', 'testpass'),
                admin_username=os.getenv('STAGING_ADMIN_USER', 'admin'),
                admin_password=os.getenv('STAGING_ADMIN_PASS', 'adminpass')
            ),
            'production': EnvironmentConfig(
                base_url=os.getenv('PRODUCTION_URL', 'https://example.com'),
                database_url=os.getenv('PRODUCTION_DATABASE_URL', ''),
                test_username=os.getenv('PRODUCTION_TEST_USER', ''),
                test_password=os.getenv('PRODUCTION_TEST_PASS', ''),
                admin_username=os.getenv('PRODUCTION_ADMIN_USER', ''),
                admin_password=os.getenv('PRODUCTION_ADMIN_PASS', '')
            )
        }
    
    def get_environment_config(self, env_name: str = None) -> EnvironmentConfig:
        """Get configuration for a specific environment"""
        env = env_name or self.current_environment
        if env not in self.environments:
            raise ValueError(f"Environment '{env}' not found in configuration")
        return self.environments[env]
    
    def get_current_environment_config(self) -> EnvironmentConfig:
        """Get configuration for the current environment"""
        return self.get_environment_config(self.current_environment)
    
    def set_environment(self, env_name: str):
        """Set the current environment"""
        if env_name not in self.environments:
            raise ValueError(f"Environment '{env_name}' not found in configuration")
        self.current_environment = env_name
    
    def get_browser_options(self) -> Dict[str, Any]:
        """Get browser options for Selenium WebDriver"""
        options = {
            'headless': self.browser.headless,
            'window_size': self.browser.window_size,
            'implicit_wait': self.browser.implicit_wait,
            'page_load_timeout': self.browser.page_load_timeout,
            'script_timeout': self.browser.script_timeout,
            'accept_insecure_certs': self.browser.accept_insecure_certs,
            'disable_gpu': self.browser.disable_gpu,
            'no_sandbox': self.browser.no_sandbox,
            'disable_dev_shm_usage': self.browser.disable_dev_shm_usage
        }
        
        # Override with environment variables if present
        if os.getenv('SELENIUM_HEADLESS'):
            options['headless'] = os.getenv('SELENIUM_HEADLESS').lower() == 'true'
        
        if os.getenv('SELENIUM_WINDOW_SIZE'):
            options['window_size'] = os.getenv('SELENIUM_WINDOW_SIZE')
        
        return options
    
    def get_test_categories(self) -> Dict[str, List[str]]:
        """Get test categories and their markers"""
        return {
            'smoke': ['smoke', 'critical'],
            'regression': ['regression'],
            'critical': ['critical'],
            'integration': ['integration'],
            'ui': ['ui', 'visual'],
            'performance': ['performance', 'slow'],
            'security': ['security'],
            'api': ['api']
        }
    
    def get_retry_config(self) -> Dict[str, Any]:
        """Get retry configuration for flaky tests"""
        return {
            'max_attempts': self.wait.retry_attempts,
            'delay': self.wait.retry_delay,
            'backoff_multiplier': 2.0,
            'max_delay': 10.0
        }
    
    def get_screenshot_config(self) -> Dict[str, Any]:
        """Get screenshot configuration"""
        return {
            'on_failure': self.test.screenshot_on_failure,
            'on_success': self.test.screenshot_on_success,
            'capture_html': self.test.capture_html_on_failure,
            'max_age_days': self.test.max_screenshot_age_days,
            'max_count': self.test.max_screenshots,
            'directory': 'test_screenshots'
        }
    
    def get_parallel_config(self) -> Dict[str, Any]:
        """Get parallel execution configuration"""
        return {
            'enabled': self.test.parallel_execution,
            'workers': self.test.parallel_workers,
            'scope': 'function'
        }


# Global configuration instance
config = TestFrameworkConfig()


def get_config() -> TestFrameworkConfig:
    """Get the global configuration instance"""
    return config


def get_env_config() -> EnvironmentConfig:
    """Get the current environment configuration"""
    return config.get_current_environment_config()


def get_browser_options() -> Dict[str, Any]:
    """Get browser options for Selenium WebDriver"""
    return config.get_browser_options()


def get_wait_config() -> WaitConfig:
    """Get wait configuration"""
    return config.wait


def get_test_config() -> TestConfig:
    """Get test configuration"""
    return config.test 