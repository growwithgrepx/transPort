# transPort Admin Portal

This is a Flask-based admin portal to manage jobs, drivers, agents, billing, and discounts, replacing the previous Excel workflow.

## Features
- Admin login/logout
- Password reset
- Manage Jobs, Drivers, Agents, Billing, Discounts
- SQLite database
- Bootstrap-based UI (customizable)

## Setup

1. **Install dependencies:**
   ```bash
   pip install flask flask_sqlalchemy werkzeug
   ```

2. **Run the app:**
   ```bash
   python app.py
   ```

3. **First time setup:**
   - The database will be created automatically on first run.
   - You may need to manually add an admin user to the database using a Python shell.

## Folder Structure
- `app.py` - Main Flask app
- `models.py` - Database models
- `templates/` - HTML templates
- `static/css/` - Custom CSS

## Customization
- Edit `static/css/style.css` for custom styles.
- Extend templates in `templates/` for new pages or features.

## Environment Variable Management

This project uses environment-specific .env files for configuration:

- `.env.development` — for local development
- `.env.test` — for running tests

The application loads the appropriate file based on the `FLASK_ENV` environment variable. For example:

- `FLASK_ENV=development` loads `.env.development`
- `FLASK_ENV=test` loads `.env.test`

If the specific file does not exist, it falls back to `.env`.

**Never commit your .env files to version control.**

Example usage:

```bash
# For development
export FLASK_ENV=development
flask run

# For tests
export FLASK_ENV=test
pytest
```

Each .env file should define a unique `DATABASE_URL` for its environment to prevent accidental data loss or corruption. 

## Automated Headless Browser Testing Framework

This project uses a robust, production-ready Selenium-based testing framework with the following features:

- **In-memory SQLite database** for test isolation (no external DB required)
- **Headless browser automation** (Chrome/Chromium, with fallback)
- **Page Object Model** for maintainable test code
- **Explicit waits, retries, and error handling** for resilience
- **Automatic screenshot and log capture on failure**
- **Dockerized test environment** for local and CI/CD use
- **Comprehensive GitHub Actions pipeline**

### Directory Structure

```
tests/
├── conftest.py                 # Shared fixtures
├── test_browser_smoke.py       # Critical path tests
├── test_browser_regression.py  # Feature tests
├── test_browser_integration.py # End-to-end tests
├── pages/                      # Page object models
│   ├── __init__.py
│   ├── login_page.py
│   └── dashboard_page.py
├── fixtures/                   # Test data
│   ├── test_data.py
│   └── factories.py
└── utils/                      # Test utilities
    ├── __init__.py
    ├── wait_conditions.py
    └── screenshot_helper.py
```

### Running Tests Locally

```bash
pip install -r requirements.txt
pytest tests/ -v --tb=short
```

### Running in Docker

A `Dockerfile` is provided for running tests in a containerized environment. See the `Dockerfile` and `.github/workflows/selenium.yml` for details.

### CI/CD Integration

Tests are run automatically on every push and pull request using GitHub Actions. Screenshots and logs are uploaded as artifacts on failure.

## Test & Report Workflow

### Running All Tests Locally

```bash
pip install -r requirements.txt
pytest -v --tb=short
```

### Running Specific Test Categories

```bash
pytest tests/unit/         # Unit tests only
pytest tests/selenium_tests/     # Selenium browser tests only
```

### Generating Test Reports Locally

After running tests with `--junitxml` output (or using the CI artifacts), you can generate summary reports:

```bash
# Unit test report
python scripts/generate_unit_report.py --xml <path-to-unit-xml> --cov <path-to-coverage-xml> --out <output-summary-file>

# Selenium test report
python scripts/generate_selenium_report.py --xml <path-to-selenium-xml> --out <output-summary-file>
```

All arguments are optional; defaults match the CI layout.

### Standard Test Flow (Local & CI)
- All test configuration is in the root `pytest.ini`.
- Use `pytest` directly for all test runs.
- Test dependencies are managed in `requirements.txt`.
- Test reports are generated using the scripts in `scripts/`.
- CI runs the same commands as local development for consistency.

### Environment Setup
- Use `.env.test` for test-specific environment variables.
- The test database is isolated and reset for each run.

### Cleaning Up Test Artifacts
- Screenshots and logs are stored in `test_screenshots/` and `logs/`.
- Use `python scripts/cleanup_screenshots.py --execute` to clean up old screenshots.

--- 