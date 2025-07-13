# Test Utilities

This directory contains utilities for managing and maintaining the test infrastructure.

## Database Management Utility

The `manage_test_db.py` script provides comprehensive test database management capabilities.

### Features

- **Database Inspection**: View database contents, sizes, and integrity
- **Cleanup Operations**: Remove old or corrupted test databases
- **Integrity Verification**: Check database health and structure
- **Report Generation**: Create detailed reports in JSON or text format
- **CI/CD Integration**: Automated database maintenance in workflows

### Usage

#### Basic Commands

```bash
# List all test databases
python tests/manage_test_db.py list

# List with detailed information
python tests/manage_test_db.py list --detailed

# Inspect the most recent database
python tests/manage_test_db.py inspect

# Inspect with sample data
python tests/manage_test_db.py inspect --detailed

# Inspect a specific database
python tests/manage_test_db.py inspect test_selenium_abc123.db

# Clean up all databases
python tests/manage_test_db.py cleanup

# Clean up databases older than 3 days
python tests/manage_test_db.py cleanup --days 3

# Generate JSON report
python tests/manage_test_db.py report

# Generate text report
python tests/manage_test_db.py report --format text

# Verify database integrity
python tests/manage_test_db.py verify
```

#### Integration with Test Runner

The database management utility is integrated into the main test runner:

```bash
# Run tests and manage databases
python tests/config/run_tests.py --manage-db

# Run all tests with automatic database management
python tests/config/run_tests.py --all
```

### Database Information

The utility provides comprehensive information about each test database:

- **File Information**: Path, size, creation/modification dates
- **Integrity Status**: SQLite integrity check results
- **Table Structure**: List of tables and record counts
- **Sample Data**: Preview of actual data (when using --detailed)

### Cleanup Strategy

The utility implements a smart cleanup strategy:

- **Age-based Cleanup**: Remove databases older than specified days
- **Integrity-based Cleanup**: Identify and flag corrupted databases
- **Size Monitoring**: Track database growth and report anomalies

### Reports

Generated reports include:

- **Summary Statistics**: Total databases, sizes, averages
- **Individual Database Details**: Complete information for each database
- **Timestamps**: When reports were generated
- **Error Tracking**: Any issues encountered during analysis

### CI/CD Integration

The utility is automatically run in GitHub Actions workflows:

1. **Pre-test**: Database integrity verification
2. **Post-test**: Cleanup of old databases
3. **Reporting**: Generation of database status reports

### Error Handling

The utility includes robust error handling:

- **Graceful Degradation**: Continues operation even if some databases fail
- **Detailed Error Messages**: Clear indication of what went wrong
- **Recovery Suggestions**: Recommendations for fixing issues

### Configuration

The utility automatically detects:

- Test database location (`tests/test_selenium*.db`)
- Report output directory (`tests/reports/`)
- Application models and configuration

### Best Practices

1. **Regular Cleanup**: Run cleanup weekly to prevent disk space issues
2. **Pre-test Verification**: Verify database integrity before running tests
3. **Post-test Analysis**: Generate reports after test runs to track database health
4. **Monitoring**: Use reports to identify patterns in database usage

### Troubleshooting

Common issues and solutions:

- **Import Errors**: Ensure the application models are accessible
- **Permission Errors**: Check file permissions in the tests directory
- **Database Locking**: Close any open database connections before cleanup
- **Path Issues**: Verify the utility is run from the correct directory 