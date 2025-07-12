# Test Screenshot Management

This document describes the automated screenshot management system for Selenium tests.

## Overview

The Selenium test framework automatically captures screenshots and HTML page sources when tests fail. These artifacts are stored in the `test_screenshots/` folder to help with debugging test failures.

## Folder Structure

```
test_screenshots/
├── *.png          # Screenshots captured during test failures
├── *.html         # HTML page sources captured during test failures
└── ...
```

## Screenshot Types

- **PNG files**: Visual screenshots of the browser state when tests fail
- **HTML files**: Page source HTML captured at the time of failure

## Automatic Organization

All screenshots are automatically saved to the `test_screenshots/` folder by:

1. **BasePage.take_screenshot()**: Automatically saves to `test_screenshots/` folder
2. **screenshot_helper.save_debug_artifacts()**: Saves both PNG and HTML files
3. **Test failure handlers**: Capture screenshots on exceptions

## Cleanup Management

### Manual Cleanup

Use the cleanup script to remove old screenshots:

```bash
# Show what would be deleted (dry run)
python scripts/cleanup_screenshots.py --dry-run

# Remove files older than 3 days (default)
python scripts/cleanup_screenshots.py --execute

# Remove files older than 3 days
python scripts/cleanup_screenshots.py --days 3 --execute

# Keep only 20 most recent files
python scripts/cleanup_screenshots.py --max-files 20 --execute

# Windows batch file
scripts/cleanup_screenshots.bat --dry-run
scripts/cleanup_screenshots.bat --execute
```

### Cleanup Options

- `--days N`: Remove files older than N days (default: 3)
- `--max-files N`: Keep only N most recent files (default: 20)
- `--dry-run`: Show what would be deleted without actually deleting
- `--execute`: Actually perform the deletion (default is dry-run)

### Status Check

Check the current status of the screenshots folder:

```bash
python scripts/screenshot_status.py
```

This shows:
- Total file count and size
- File types breakdown
- Oldest and newest files
- Recent files with ages and sizes

## Git Integration

The `test_screenshots/` folder is automatically excluded from Git tracking via `.gitignore`. This prevents:

- Committing large binary files to the repository
- Cluttering the repository with test artifacts
- Sharing sensitive information that might be visible in screenshots

## Best Practices

### For Developers

1. **Check screenshots after test failures**: Screenshots provide valuable debugging information
2. **Clean up regularly**: Run cleanup script weekly to prevent folder bloat
3. **Review before deletion**: Use `--dry-run` to see what will be deleted
4. **Keep recent failures**: Don't delete screenshots from recent test runs

### For CI/CD

1. **Archive on failure**: Copy screenshots to artifacts before cleanup
2. **Set retention policy**: Configure cleanup to run automatically
3. **Monitor disk usage**: Set alerts for large screenshot folders

## Configuration

### Default Settings

- **Retention**: 7 days
- **Max files**: 50
- **Folder**: `test_screenshots/`
- **File types**: `.png`, `.html`

### Customization

You can modify the default settings in:
- `scripts/cleanup_screenshots.py`: Change default retention and file limits
- `tests/pages/base_page.py`: Modify screenshot saving behavior
- `tests/utils/screenshot_helper.py`: Adjust debug artifact capture

## Troubleshooting

### Common Issues

1. **Permission errors**: Ensure write access to `test_screenshots/` folder
2. **Large folder size**: Run cleanup script regularly
3. **Missing screenshots**: Check if test is properly calling screenshot methods

### Debug Commands

```bash
# Check folder status
python scripts/screenshot_status.py

# See what cleanup would do
python scripts/cleanup_screenshots.py --dry-run

# Force cleanup of all files (use with caution)
python scripts/cleanup_screenshots.py --days 0 --execute
```

## Integration with Test Framework

The screenshot system integrates seamlessly with the existing test framework:

- **Automatic capture**: Screenshots are taken on test failures
- **Page Object Model**: BasePage provides screenshot methods
- **Error handling**: Screenshots are captured in exception handlers
- **Debug artifacts**: Both visual and HTML artifacts are saved

This ensures comprehensive debugging information is available when tests fail. 