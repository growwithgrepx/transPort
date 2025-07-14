"""
Comprehensive unit tests for utility functions and helper modules.
Tests focus on practical scenarios and real functionality.
"""

import pytest
import re
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class TestValidationUtils:
    """Test validation utility functions"""
    
    def test_email_validation_comprehensive(self):
        """Test comprehensive email validation scenarios"""
        from tests.unit.test_utils import is_valid_email
        
        # Valid email addresses
        valid_emails = [
            'user@example.com',
            'test.user@domain.co.uk',
            'admin@company.org',
            'user+tag@example.com',
            'user123@test-domain.net',
            'a@b.co',  # Minimal valid email
            'user.name@subdomain.example.com'
        ]
        
        for email in valid_emails:
            assert is_valid_email(email), f"Email should be valid: {email}"
        
        # Invalid email addresses
        invalid_emails = [
            '',  # Empty string
            None,  # None value
            'userexample.com',  # Missing @
            'user@',  # Missing domain
            '@example.com',  # Missing username
            'user@.com',  # Missing domain name
            'user..name@example.com',  # Double dots
            'user@example..com',  # Double dots in domain
            'user@example.',  # Trailing dot
            '.user@example.com',  # Leading dot
            'user name@example.com',  # Space in username
            'user@example com',  # Space in domain
            'user@example_com',  # Underscore in domain
            'a@b',  # Too short
            'a' * 100 + '@example.com',  # Username too long
            'user@' + 'a' * 100 + '.com',  # Domain too long
        ]
        
        for email in invalid_emails:
            assert not is_valid_email(email), f"Email should be invalid: {email}"
    
    def test_phone_validation_comprehensive(self):
        """Test comprehensive phone number validation"""
        from tests.unit.test_validation import validate_phone_number
        
        # Valid phone numbers
        valid_phones = [
            '123-456-7890',
            '(123) 456-7890',
            '1234567890',
            '+1-234-567-8901',
            '+44 20 7946 0958',
            '123.456.7890',
            '123 456 7890',
            '+1 (234) 567-8901'
        ]
        
        for phone in valid_phones:
            assert validate_phone_number(phone), f"Phone should be valid: {phone}"
        
        # Invalid phone numbers
        invalid_phones = [
            '',  # Empty string
            None,  # None value
            '123',  # Too short
            '12345678901234567890',  # Too long
            'abc-def-ghij',  # Non-numeric
            '123-456-789',  # Too short after cleaning
            '1234567890123456',  # Too long after cleaning
            '123-456-789a',  # Contains letters
        ]
        
        for phone in invalid_phones:
            assert not validate_phone_number(phone), f"Phone should be invalid: {phone}"
    
    def test_username_validation_comprehensive(self):
        """Test comprehensive username validation"""
        from tests.unit.test_validation import validate_username
        
        # Valid usernames
        valid_usernames = [
            'john_doe',
            'user123',
            'admin',
            'test_user_123',
            'a' * 20,  # Maximum length
            'user_name',
            'user123name',
            'USER123',
            'User_Name'
        ]
        
        for username in valid_usernames:
            assert validate_username(username), f"Username should be valid: {username}"
        
        # Invalid usernames
        invalid_usernames = [
            '',  # Empty string
            None,  # None value
            'ab',  # Too short
            'a' * 21,  # Too long
            'user-name',  # Contains hyphen
            'user name',  # Contains space
            'user.name',  # Contains dot
            'user@name',  # Contains @
            'user#name',  # Contains special character
            '123user',  # Starts with number (if not allowed)
            'user',  # Too short
        ]
        
        for username in invalid_usernames:
            assert not validate_username(username), f"Username should be invalid: {username}"


class TestBusinessLogicUtils:
    """Test business logic utility functions"""
    
    def test_parse_job_message_comprehensive(self):
        """Test comprehensive job message parsing"""
        # Import the function from app.py
        import sys
        import os
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        
        # Mock the app context to import the function
        with patch('flask.current_app'):
            from app import parse_job_message
            
            # Test valid message parsing
            valid_message = """
            Customer: John Doe
            Email: john@example.com
            Phone: 123-456-7890
            Pickup: Airport Terminal 1
            Dropoff: Downtown Hotel
            Date: 2024-01-15
            Time: 10:00 AM
            Service: Airport Transfer
            Vehicle: Sedan
            Payment: Credit Card
            """
            
            result = parse_job_message(valid_message)
            expected_fields = [
                'customer_name', 'customer_email', 'customer_mobile',
                'pickup_location', 'dropoff_location', 'pickup_date',
                'pickup_time', 'type_of_service', 'vehicle_type', 'payment_mode'
            ]
            
            for field in expected_fields:
                assert field in result, f"Field {field} should be parsed"
                assert result[field] is not None, f"Field {field} should not be None"
            
            assert result['customer_name'] == 'John Doe'
            assert result['customer_email'] == 'john@example.com'
            assert result['customer_mobile'] == '123-456-7890'
            assert result['pickup_location'] == 'Airport Terminal 1'
            assert result['dropoff_location'] == 'Downtown Hotel'
            assert result['pickup_date'] == '2024-01-15'
            assert result['pickup_time'] == '10:00 AM'
            assert result['type_of_service'] == 'Airport Transfer'
            assert result['vehicle_type'] == 'Sedan'
            assert result['payment_mode'] == 'Credit Card'
    
    def test_parse_job_message_edge_cases(self):
        """Test job message parsing edge cases"""
        with patch('flask.current_app'):
            from app import parse_job_message
            
            # Test empty message
            assert parse_job_message('') == {}
            assert parse_job_message(None) == {}
            
            # Test message with no valid fields
            assert parse_job_message('This is just a regular message') == {}
            
            # Test message with partial data
            partial_message = """
            Customer: John Doe
            Pickup: Airport
            """
            result = parse_job_message(partial_message)
            assert result['customer_name'] == 'John Doe'
            assert result['pickup_location'] == 'Airport'
            assert 'customer_email' not in result
            
            # Test message with extra whitespace
            whitespace_message = """
            Customer:    John Doe    
            Email:   john@example.com   
            """
            result = parse_job_message(whitespace_message)
            assert result['customer_name'] == 'John Doe'
            assert result['customer_email'] == 'john@example.com'
            
            # Test message with special characters
            special_message = """
            Customer: O'Connor-Smith
            Email: user+tag@example.com
            """
            result = parse_job_message(special_message)
            assert result['customer_name'] == "O'Connor-Smith"
            assert result['customer_email'] == 'user+tag@example.com'
    
    def test_date_validation_utils(self):
        """Test date validation utilities"""
        # Test valid date formats
        valid_dates = [
            '2024-01-15',
            '2024-12-31',
            '2023-02-28',
            '2024-02-29',  # Leap year
        ]
        
        for date_str in valid_dates:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                assert True  # Valid date
            except ValueError:
                assert False, f"Date should be valid: {date_str}"
        
        # Test invalid date formats
        invalid_dates = [
            '2024-13-01',  # Invalid month
            '2024-12-32',  # Invalid day
            '2023-02-29',  # Not leap year
            'invalid-date',
            '2024/01/15',  # Wrong format
            '01-15-2024',  # Wrong format
        ]
        
        for date_str in invalid_dates:
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
                assert False, f"Date should be invalid: {date_str}"
            except ValueError:
                assert True  # Invalid date
    
    def test_time_validation_utils(self):
        """Test time validation utilities"""
        # Test valid time formats
        valid_times = [
            '10:00 AM',
            '2:30 PM',
            '12:00 AM',
            '11:59 PM',
            '00:00',
            '23:59',
            '09:30',
        ]
        
        for time_str in valid_times:
            # Try different time formats
            try:
                if 'AM' in time_str or 'PM' in time_str:
                    datetime.strptime(time_str, '%I:%M %p')
                else:
                    datetime.strptime(time_str, '%H:%M')
                assert True  # Valid time
            except ValueError:
                assert False, f"Time should be valid: {time_str}"
        
        # Test invalid time formats
        invalid_times = [
            '25:00',  # Invalid hour
            '12:60',  # Invalid minute
            '13:00 AM',  # Invalid AM/PM
            'invalid-time',
            '10:00:30',  # Wrong format (with seconds)
        ]
        
        for time_str in invalid_times:
            try:
                if 'AM' in time_str or 'PM' in time_str:
                    datetime.strptime(time_str, '%I:%M %p')
                else:
                    datetime.strptime(time_str, '%H:%M')
                assert False, f"Time should be invalid: {time_str}"
            except ValueError:
                assert True  # Invalid time


class TestSecurityUtils:
    """Test security-related utility functions"""
    
    def test_password_validation(self):
        """Test password validation logic"""
        # Test password strength requirements
        def validate_password_strength(password):
            if not password:
                return False, "Password is required"
            if len(password) < 8:
                return False, "Password must be at least 8 characters"
            if len(password) > 128:
                return False, "Password must be less than 128 characters"
            if not re.search(r'[A-Z]', password):
                return False, "Password must contain uppercase letter"
            if not re.search(r'[a-z]', password):
                return False, "Password must contain lowercase letter"
            if not re.search(r'\d', password):
                return False, "Password must contain number"
            return True, "Password is strong"
        
        # Valid passwords
        valid_passwords = [
            'StrongPass123',
            'MySecureP@ss1',
            'ComplexPassword2024!',
        ]
        
        for password in valid_passwords:
            is_valid, message = validate_password_strength(password)
            assert is_valid, f"Password should be valid: {password} - {message}"
        
        # Invalid passwords
        invalid_passwords = [
            '',  # Empty
            'short',  # Too short
            'nouppercase123',  # No uppercase
            'NOLOWERCASE123',  # No lowercase
            'NoNumbers',  # No numbers
            'a' * 129,  # Too long
        ]
        
        for password in invalid_passwords:
            is_valid, message = validate_password_strength(password)
            assert not is_valid, f"Password should be invalid: {password} - {message}"
    
    def test_input_sanitization(self):
        """Test input sanitization utilities"""
        def sanitize_input(input_str):
            if not input_str:
                return ''
            # Remove potentially dangerous characters
            sanitized = re.sub(r'[<>"\']', '', str(input_str))
            # Trim whitespace
            sanitized = sanitized.strip()
            return sanitized
        
        # Test sanitization
        test_cases = [
            ('<script>alert("XSS")</script>', 'scriptalert(XSS)/script'),
            ('  Hello World  ', 'Hello World'),
            ('User\'s Name', 'Users Name'),
            ('<div>Content</div>', 'divContent/div'),
            ('', ''),
            (None, ''),
        ]
        
        for input_str, expected in test_cases:
            result = sanitize_input(input_str)
            assert result == expected, f"Sanitization failed for: {input_str}"
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        def safe_query_builder(field, value):
            # Simulate safe query building
            allowed_fields = ['customer_name', 'email', 'status']
            if field not in allowed_fields:
                raise ValueError(f"Invalid field: {field}")
            
            # In real implementation, this would use parameterized queries
            return f"SELECT * FROM users WHERE {field} = ?"
        
        # Valid queries
        valid_queries = [
            ('customer_name', 'John Doe'),
            ('email', 'john@example.com'),
            ('status', 'active'),
        ]
        
        for field, value in valid_queries:
            query = safe_query_builder(field, value)
            assert 'SELECT' in query
            assert field in query
            assert '?' in query  # Parameter placeholder
        
        # Invalid queries should raise exception
        with pytest.raises(ValueError):
            safe_query_builder('invalid_field', 'value')
        
        with pytest.raises(ValueError):
            safe_query_builder('DROP TABLE users', 'value')


class TestDataProcessingUtils:
    """Test data processing utility functions"""
    
    def test_pagination_utils(self):
        """Test pagination utility functions"""
        def paginate_data(data, page, per_page):
            if not data:
                return [], 0, 0, 0
            
            total = len(data)
            start = (page - 1) * per_page
            end = start + per_page
            
            paginated_data = data[start:end]
            total_pages = (total + per_page - 1) // per_page
            
            return paginated_data, total, page, total_pages
        
        # Test data
        test_data = list(range(1, 101))  # 1 to 100
        
        # Test first page
        result, total, page, total_pages = paginate_data(test_data, 1, 10)
        assert len(result) == 10
        assert result[0] == 1
        assert result[9] == 10
        assert total == 100
        assert page == 1
        assert total_pages == 10
        
        # Test last page
        result, total, page, total_pages = paginate_data(test_data, 10, 10)
        assert len(result) == 10
        assert result[0] == 91
        assert result[9] == 100
        
        # Test empty data
        result, total, page, total_pages = paginate_data([], 1, 10)
        assert len(result) == 0
        assert total == 0
        assert page == 1
        assert total_pages == 0
        
        # Test page beyond data
        result, total, page, total_pages = paginate_data(test_data, 15, 10)
        assert len(result) == 0  # No data for page 15
    
    def test_search_utils(self):
        """Test search utility functions"""
        def search_data(data, query, fields):
            if not query or not data:
                return data
            
            query = query.lower()
            results = []
            
            for item in data:
                for field in fields:
                    if hasattr(item, field):
                        value = getattr(item, field)
                        if value and query in str(value).lower():
                            results.append(item)
                            break
            
            return results
        
        # Test data class
        class TestItem:
            def __init__(self, name, email, description):
                self.name = name
                self.email = email
                self.description = description
        
        test_data = [
            TestItem('John Doe', 'john@example.com', 'Software Engineer'),
            TestItem('Jane Smith', 'jane@example.com', 'Product Manager'),
            TestItem('Bob Johnson', 'bob@example.com', 'Designer'),
        ]
        
        # Test search by name
        results = search_data(test_data, 'john', ['name'])
        assert len(results) == 1
        assert results[0].name == 'John Doe'
        
        # Test search by email
        results = search_data(test_data, 'jane@example.com', ['email'])
        assert len(results) == 1
        assert results[0].email == 'jane@example.com'
        
        # Test search across multiple fields
        results = search_data(test_data, 'engineer', ['name', 'description'])
        assert len(results) == 1
        assert results[0].description == 'Software Engineer'
        
        # Test case insensitive search
        results = search_data(test_data, 'JOHN', ['name'])
        assert len(results) == 1
        assert results[0].name == 'John Doe'
        
        # Test no results
        results = search_data(test_data, 'nonexistent', ['name'])
        assert len(results) == 0
        
        # Test empty query
        results = search_data(test_data, '', ['name'])
        assert len(results) == 3  # All items
    
    def test_sorting_utils(self):
        """Test sorting utility functions"""
        def sort_data(data, sort_by, sort_order='asc'):
            if not data:
                return data
            
            reverse = sort_order.lower() == 'desc'
            
            try:
                return sorted(data, key=lambda x: getattr(x, sort_by, ''), reverse=reverse)
            except (AttributeError, TypeError):
                return data
        
        # Test data class
        class TestItem:
            def __init__(self, name, age, score):
                self.name = name
                self.age = age
                self.score = score
        
        test_data = [
            TestItem('Alice', 25, 85),
            TestItem('Bob', 30, 92),
            TestItem('Charlie', 22, 78),
        ]
        
        # Test ascending sort by name
        results = sort_data(test_data, 'name', 'asc')
        assert results[0].name == 'Alice'
        assert results[1].name == 'Bob'
        assert results[2].name == 'Charlie'
        
        # Test descending sort by age
        results = sort_data(test_data, 'age', 'desc')
        assert results[0].age == 30
        assert results[1].age == 25
        assert results[2].age == 22
        
        # Test ascending sort by score
        results = sort_data(test_data, 'score', 'asc')
        assert results[0].score == 78
        assert results[1].score == 85
        assert results[2].score == 92
        
        # Test empty data
        results = sort_data([], 'name')
        assert results == []
        
        # Test invalid sort field
        results = sort_data(test_data, 'invalid_field')
        assert results == test_data  # Should return original data


class TestErrorHandlingUtils:
    """Test error handling utility functions"""
    
    def test_exception_logging(self):
        """Test exception logging utilities, ensure errors are logged and do not crash tests."""
        logged_exceptions = []
        def log_exception(exception, context=None):
            logged_exceptions.append({
                'exception': str(exception),
                'type': type(exception).__name__,
                'context': context
            })
        try:
            raise ValueError("Test value error")
        except ValueError as e:
            log_exception(e, "Test context")
        try:
            raise TypeError("Test type error")
        except TypeError as e:
            log_exception(e, "Another context")
        assert len(logged_exceptions) == 2, "Should log two exceptions"
        assert logged_exceptions[0]['type'] == 'ValueError', "First should be ValueError"
        assert logged_exceptions[1]['type'] == 'TypeError', "Second should be TypeError"
    
    def test_error_response_formatting(self):
        """Test error response formatting"""
        def format_error_response(error, status_code=500):
            return {
                'error': str(error),
                'status_code': status_code,
                'timestamp': datetime.now().isoformat()
            }
        
        # Test different error types
        error1 = ValueError("Invalid input")
        response1 = format_error_response(error1, 400)
        
        assert response1['error'] == 'Invalid input'
        assert response1['status_code'] == 400
        assert 'timestamp' in response1
        
        error2 = Exception("Internal server error")
        response2 = format_error_response(error2)
        
        assert response2['error'] == 'Internal server error'
        assert response2['status_code'] == 500
        assert 'timestamp' in response2
    
    def test_validation_error_aggregation(self):
        """Test validation error aggregation"""
        def aggregate_validation_errors(errors):
            if not errors:
                return {}
            
            aggregated = {}
            for field, error_list in errors.items():
                if isinstance(error_list, list):
                    aggregated[field] = error_list
                else:
                    aggregated[field] = [error_list]
            
            return aggregated
        
        # Test single error
        errors = {'username': 'Username is required'}
        result = aggregate_validation_errors(errors)
        assert result['username'] == ['Username is required']
        
        # Test multiple errors
        errors = {
            'username': ['Username is required', 'Username too short'],
            'email': 'Invalid email format'
        }
        result = aggregate_validation_errors(errors)
        assert result['username'] == ['Username is required', 'Username too short']
        assert result['email'] == ['Invalid email format']
        
        # Test empty errors
        result = aggregate_validation_errors({})
        assert result == {}
        
        result = aggregate_validation_errors(None)
        assert result == {}


class TestPerformanceUtils:
    """Test performance-related utility functions"""
    
    def test_caching_utils(self):
        """Test caching utility functions"""
        cache = {}
        
        def get_cached_value(key, default=None):
            return cache.get(key, default)
        
        def set_cached_value(key, value, ttl=None):
            cache[key] = {
                'value': value,
                'expires_at': datetime.now() + timedelta(seconds=ttl) if ttl else None
            }
        
        def is_cache_valid(key):
            if key not in cache:
                return False
            
            cached_item = cache[key]
            if cached_item['expires_at'] is None:
                return True
            
            return datetime.now() < cached_item['expires_at']
        
        # Test basic caching
        set_cached_value('test_key', 'test_value')
        assert get_cached_value('test_key') == {'value': 'test_value', 'expires_at': None}
        assert is_cache_valid('test_key')
        
        # Test cache miss
        assert get_cached_value('nonexistent_key') is None
        assert get_cached_value('nonexistent_key', 'default') == 'default'
        assert not is_cache_valid('nonexistent_key')
        
        # Test TTL
        set_cached_value('expiring_key', 'expiring_value', ttl=1)
        assert is_cache_valid('expiring_key')
        
        # Simulate time passing
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.now() + timedelta(seconds=2)
            assert not is_cache_valid('expiring_key')
    
    def test_batch_processing_utils(self):
        """Test batch processing utility functions"""
        def process_in_batches(items, batch_size, processor_func):
            results = []
            for i in range(0, len(items), batch_size):
                batch = items[i:i + batch_size]
                batch_results = processor_func(batch)
                results.extend(batch_results)
            return results
        
        # Test batch processing
        items = list(range(1, 11))  # 1 to 10
        
        def double_items(batch):
            return [x * 2 for x in batch]
        
        results = process_in_batches(items, 3, double_items)
        assert results == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
        # Test with different batch sizes
        results = process_in_batches(items, 5, double_items)
        assert results == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
        # Test with batch size larger than data
        results = process_in_batches(items, 20, double_items)
        assert results == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
        
        # Test empty items
        results = process_in_batches([], 5, double_items)
        assert results == []
    
    def test_memory_usage_utils(self):
        """Test memory usage utility functions"""
        def estimate_memory_usage(data):
            """Estimate memory usage of data structures"""
            if isinstance(data, str):
                return len(data.encode('utf-8'))
            elif isinstance(data, (int, float)):
                return 8  # Approximate size for numbers
            elif isinstance(data, list):
                return sum(estimate_memory_usage(item) for item in data)
            elif isinstance(data, dict):
                return sum(estimate_memory_usage(k) + estimate_memory_usage(v) 
                          for k, v in data.items())
            else:
                return 0
        
        # Test different data types
        assert estimate_memory_usage("Hello") == 5
        assert estimate_memory_usage(123) == 8
        assert estimate_memory_usage([1, 2, 3]) == 24
        assert estimate_memory_usage({'a': 1, 'b': 2}) == 18  # 1 + 8 + 1 + 8
        assert estimate_memory_usage([]) == 0
        assert estimate_memory_usage({}) == 0 