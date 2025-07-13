"""
Simple test to verify fixtures are working correctly.
"""

import pytest

def test_app_fixture_exists(app):
    """Test that the app fixture is available and working"""
    assert app is not None
    assert app.config['TESTING'] is True
    assert app.config['SQLALCHEMY_DATABASE_URI'] is not None

def test_test_app_fixture_exists(test_app):
    """Test that the test_app fixture is available and working"""
    assert test_app is not None
    assert test_app.config['TESTING'] is True

def test_client_fixture_exists(client):
    """Test that the client fixture is available and working"""
    assert client is not None

def test_seeded_db_fixture_exists(seeded_db):
    """Test that the seeded_db fixture is available and working"""
    assert seeded_db is not None
    assert 'user' in seeded_db
    assert 'agent' in seeded_db
    assert 'driver' in seeded_db 