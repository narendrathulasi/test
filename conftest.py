"""
Pytest configuration and fixtures for the test suite.
"""
import pytest
import subprocess
import time
import requests
import threading
from mock_service import app, offers_db, user_segments_db
from api.cart_api import CartAPI


@pytest.fixture(scope='session')
def mock_server():
    """
    Start the mock server in a separate thread for the entire test session.
    """
    # Clear databases before starting
    offers_db.clear()
    user_segments_db.clear()
    
    # Use port 5001 to avoid conflicts with AirPlay Receiver on macOS
    port = 5001
    
    # Start Flask app in a separate thread
    def run_server():
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to be ready
    max_retries = 10
    for _ in range(max_retries):
        try:
            response = requests.get(f'http://localhost:{port}/health', timeout=1)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(0.5)
    else:
        pytest.fail("Mock server failed to start")
    
    yield
    
    # Cleanup (server thread will be killed when test session ends)


@pytest.fixture(scope='session')
def api_client(mock_server):
    """
    Create API client instance for the test session.
    """
    return CartAPI(base_url='http://localhost:5001')


@pytest.fixture(autouse=True)
def cleanup_before_test():
    """
    Clean up offers and user segments before each test.
    """
    offers_db.clear()
    user_segments_db.clear()
    yield
    # Optional: cleanup after test if needed

