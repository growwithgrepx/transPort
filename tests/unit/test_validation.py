"""
Unit tests for data validation functions.
These are genuine unit tests with no external dependencies.
"""

def validate_phone_number(phone):
    """Basic phone number validation"""
    if not phone:
        return False
    # Remove common separators
    cleaned = ''.join(filter(str.isdigit, phone))
    return len(cleaned) >= 10 and len(cleaned) <= 15

def validate_username(username):
    """Basic username validation"""
    if not username:
        return False
    # Username should be 3-20 characters, alphanumeric and underscore only
    import re
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return bool(re.match(pattern, username))

def test_validate_phone_number_valid():
    """Test valid phone numbers"""
    assert validate_phone_number("123-456-7890")
    assert validate_phone_number("(123) 456-7890")
    assert validate_phone_number("1234567890")
    assert validate_phone_number("+1-234-567-8901")

def test_validate_phone_number_invalid():
    """Test invalid phone numbers"""
    assert not validate_phone_number("")
    assert not validate_phone_number("123")
    assert not validate_phone_number("12345678901234567890")  # Too long
    assert not validate_phone_number("abc-def-ghij")

def test_validate_username_valid():
    """Test valid usernames"""
    assert validate_username("john_doe")
    assert validate_username("user123")
    assert validate_username("admin")
    assert validate_username("test_user_123")

def test_validate_username_invalid():
    """Test invalid usernames"""
    assert not validate_username("")
    assert not validate_username("ab")  # Too short
    assert not validate_username("this_username_is_way_too_long_for_validation")
    assert not validate_username("user-name")  # Contains hyphen
    assert not validate_username("user name")  # Contains space 