"""
Unit tests for utility functions.
These are genuine unit tests with no external dependencies.
"""

def add(a, b):
    """Simple addition function for testing"""
    return a + b

def is_valid_email(email):
    """Basic email validation function for testing"""
    if not email or "@" not in email or "." not in email or len(email) < 6:
        return False
    # Check that @ is not at the beginning or end
    parts = email.split("@")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        return False
    # Check that there's a domain with a dot
    domain = parts[1]
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    return True

def test_add_positive_numbers():
    """Test addition with positive numbers"""
    assert add(2, 3) == 5
    assert add(10, 20) == 30
    assert add(0, 5) == 5

def test_add_negative_numbers():
    """Test addition with negative numbers"""
    assert add(-2, -3) == -5
    assert add(-10, 5) == -5
    assert add(0, -5) == -5

def test_valid_email():
    """Test valid email addresses"""
    assert is_valid_email("user@example.com")
    assert is_valid_email("test.user@domain.co.uk")
    assert is_valid_email("admin@company.org")

def test_invalid_email():
    """Test invalid email addresses"""
    assert not is_valid_email("userexample.com")  # Missing @
    assert not is_valid_email("user@")  # Missing domain
    assert not is_valid_email("@example.com")  # Missing username
    assert not is_valid_email("a@b")  # Too short 