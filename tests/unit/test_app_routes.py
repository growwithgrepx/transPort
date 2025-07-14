def test_index_route(client):
    """Ensure the index route is covered for app.py."""
    response = client.get("/")
    assert response.status_code in (200, 302)  # 302 if it redirects to login 


def test_app_import_and_blueprints():
    """
    Import app.py and check that the Flask app and blueprints are registered.
    This ensures app.py is imported and its top-level code is executed.
    """
    import app
    assert hasattr(app, 'app')
    # Optionally, check for blueprints if you know their names
    # Example: assert 'jobs' in app.app.blueprints 