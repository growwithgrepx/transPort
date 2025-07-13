# TransPort Test Suite

This directory contains all test-related files for the TransPort Flask application, organized for clean separation and CI/CD integration.

## 📁 Directory Structure

```
tests/
├── config/                 # Test configuration files
│   ├── pytest.ini         # Pytest configuration
│   └── run_tests.py       # Test runner script
├── reports/               # Test reports and artifacts
│   ├── test_report.md     # Comprehensive test report
│   ├── test_execution.log # Test execution logs
│   ├── htmlcov/          # HTML coverage reports
│   └── coverage.xml      # XML coverage reports
├── unit/                  # Unit tests
│   ├── test_models.py     # Model tests
│   ├── test_app_logic.py  # Application logic tests
│   ├── test_blueprints.py # Blueprint tests
│   ├── test_extensions.py # Extension tests
│   ├── test_integration.py # Integration tests
│   └── test_utils_comprehensive.py # Utility tests
├── selenium/              # Selenium browser tests
├── pages/                 # Page object models
├── core/                  # Core test framework
├── fixtures/              # Test fixtures and factories
├── utils/                 # Test utilities
├── conftest.py           # Pytest configuration
└── README.md             # This file
```

## 🚀 Quick Start

### Running Tests

From the project root:

```bash
# Run all tests
python run_tests.py --all

# Run unit tests only
python run_tests.py --unit

# Run integration tests
python run_tests.py --integration

# Run Selenium tests
python run_tests.py --selenium

# Run with coverage
python run_tests.py --coverage

# Run specific test
python run_tests.py --test tests/unit/test_models.py::TestUserModel::test_user_creation
```

### Direct Pytest Usage

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/selenium/

# Run with markers
pytest -m unit
pytest -m integration
pytest -m selenium

# Run with coverage
pytest --cov=app --cov=models --cov-report=html
```

## 📊 Test Categories

### Unit Tests (`tests/unit/`)
- **Models**: Database model tests (User, Job, Driver, etc.)
- **Application Logic**: Route handlers, decorators, utilities
- **Blueprints**: Blueprint-specific functionality
- **Extensions**: Database and other extensions
- **Integration**: Cross-component integration tests
- **Utilities**: Helper function tests

### Selenium Tests (`tests/selenium/`)
- **Browser Automation**: End-to-end user interface tests
- **Page Objects**: Reusable page interaction patterns
- **Cross-browser**: Multi-browser compatibility tests

### Test Framework (`tests/core/`)
- **Base Classes**: Common test functionality
- **Wait Conditions**: Custom wait strategies
- **Exceptions**: Test-specific exceptions
- **Locators**: Element locator strategies

## 🎯 Test Coverage Goals

- **Target**: 90% line coverage
- **Current**: 49.33% (as of latest run)
- **Focus Areas**: 
  - Application routes and handlers
  - Business logic and validation
  - Database operations
  - Error handling

## 🔧 Configuration

### Pytest Configuration (`tests/config/pytest.ini`)
- Test discovery patterns
- Coverage settings
- Markers and options
- Environment variables

### Test Runner (`tests/config/run_tests.py`)
- Comprehensive test execution
- Coverage report generation
- Environment setup
- Dependency management

## 📈 Coverage Reports

Reports are generated in `tests/reports/`:

- **HTML Reports**: `tests/reports/htmlcov/`
- **XML Reports**: `tests/reports/coverage.xml`
- **Text Reports**: Console output with missing lines

## 🏷️ Test Markers

```python
@pytest.mark.unit          # Unit tests
@pytest.mark.integration   # Integration tests
@pytest.mark.selenium      # Browser tests
@pytest.mark.slow          # Slow running tests
@pytest.mark.smoke         # Smoke tests
@pytest.mark.regression    # Regression tests
@pytest.mark.security      # Security tests
@pytest.mark.performance   # Performance tests
```

## 🧪 Test Data Management

### Fixtures (`tests/fixtures/`)
- **Factories**: Model instance creation
- **Data**: Test data sets
- **Mocks**: Mock objects and services

### Database Management
- **Test Database**: Isolated SQLite database
- **Migrations**: Test-specific schema
- **Cleanup**: Automatic cleanup between tests

## 🔄 CI/CD Integration

### GitHub Actions (`.github/workflows/tests.yml`)
- **Automated Testing**: Runs on push/PR
- **Multi-Python**: Tests on Python 3.9, 3.10, 3.11
- **Coverage Upload**: Integrates with Codecov
- **Artifact Storage**: Preserves test results
- **PR Comments**: Automatic test result comments

### Pipeline Stages
1. **Unit Tests**: Fast, isolated tests
2. **Integration Tests**: Cross-component tests
3. **Selenium Tests**: Browser automation
4. **Coverage Analysis**: Coverage reporting
5. **Artifact Upload**: Result preservation

## 🐛 Debugging Tests

### Common Issues
1. **Database Conflicts**: UNIQUE constraint violations
2. **Authentication**: Missing user context
3. **API Changes**: SQLAlchemy 2.x compatibility
4. **Missing Dependencies**: Import errors

### Debug Commands
```bash
# Run with verbose output
pytest -v -s

# Run single test with debugger
pytest tests/unit/test_models.py::TestUserModel::test_user_creation -s

# Check test environment
python run_tests.py --check-env

# Clean test artifacts
python run_tests.py --clean
```

## 📝 Writing Tests

### Test Structure
```python
import pytest
from tests.fixtures.factories import UserFactory

class TestUserModel:
    def test_user_creation(self, db_session):
        """Test user creation with valid data"""
        user = UserFactory()
        assert user.id is not None
        assert user.email is not None
```

### Best Practices
1. **Descriptive Names**: Clear test method names
2. **Arrange-Act-Assert**: Structured test layout
3. **Isolation**: Each test is independent
4. **Fixtures**: Reusable test data
5. **Documentation**: Clear test descriptions

### Test Data
```python
# Use factories for consistent test data
user = UserFactory(email="test@example.com")

# Use parametrized tests for multiple scenarios
@pytest.mark.parametrize("email,valid", [
    ("test@example.com", True),
    ("invalid-email", False),
])
def test_email_validation(email, valid):
    # Test implementation
```

## 🔒 Security Testing

### Test Categories
- **SQL Injection**: Database query security
- **XSS Prevention**: Cross-site scripting protection
- **CSRF Protection**: Cross-site request forgery
- **Authentication**: User authentication flows
- **Authorization**: Role-based access control

### Security Test Examples
```python
def test_sql_injection_prevention(client):
    """Test that SQL injection attempts are blocked"""
    response = client.get('/jobs?search=1; DROP TABLE users;')
    assert response.status_code == 400

def test_xss_prevention(client):
    """Test that XSS attempts are sanitized"""
    response = client.post('/jobs', data={
        'message': '<script>alert("xss")</script>'
    })
    assert '<script>' not in response.data.decode()
```

## 📊 Performance Testing

### Metrics
- **Response Time**: API endpoint performance
- **Database Queries**: Query optimization
- **Memory Usage**: Memory leak detection
- **Concurrent Users**: Load testing

### Performance Test Examples
```python
import time

def test_job_search_performance(client):
    """Test that job search completes within acceptable time"""
    start_time = time.time()
    response = client.get('/jobs?search=test')
    end_time = time.time()
    
    assert response.status_code == 200
    assert (end_time - start_time) < 1.0  # Less than 1 second
```

## 🧹 Maintenance

### Regular Tasks
1. **Update Dependencies**: Keep test dependencies current
2. **Review Coverage**: Identify uncovered code
3. **Refactor Tests**: Improve test quality
4. **Update Documentation**: Keep docs current

### Cleanup Commands
```bash
# Clean test artifacts
python run_tests.py --clean

# Remove coverage data
coverage erase

# Clean pytest cache
pytest --cache-clear
```

## 📞 Support

For test-related issues:
1. Check the test report in `tests/reports/test_report.md`
2. Review test execution logs
3. Consult this documentation
4. Check CI/CD pipeline results

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [Factory Boy Documentation](https://factoryboy.readthedocs.io/)
- [Selenium Documentation](https://selenium-python.readthedocs.io/) 