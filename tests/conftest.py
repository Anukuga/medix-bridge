"""Pytest configuration and fixtures for testing the Flask application."""

import pytest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
from main import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test_secret_key"
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_cursor():
    """Create a mock database cursor."""
    cursor = MagicMock()
    cursor.execute = MagicMock()
    cursor.fetchone = MagicMock()
    cursor.fetchall = MagicMock()
    cursor.close = MagicMock()
    return cursor


@pytest.fixture
def mock_connection(mock_cursor):
    """Create a mock database connection."""
    connection = MagicMock()
    connection.cursor.return_value = mock_cursor
    connection.commit = MagicMock()
    connection.rollback = MagicMock()
    return connection


@pytest.fixture
def mock_mysql(mock_connection, mock_cursor):
    """Mock the MySQL connection."""
    with patch("main.mysql") as mock_mysql_obj:
        # Set up both mysql.connect and mysql.connection
        mock_mysql_obj.connect = mock_connection
        mock_mysql_obj.connection = mock_connection
        # Also ensure connection.cursor() returns our mock cursor
        mock_connection.cursor.return_value = mock_cursor
        yield mock_mysql_obj


@pytest.fixture
def sample_doctor():
    """Sample doctor data for testing."""
    return {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email_address": "john.doe@example.com",
        "password": generate_password_hash("password123"),
        "specialty": "Cardiology",
        "birth_date": "1980-01-01",
        "gender": "Male",
        "license_number": "LIC123",
        "nationality": "American",
        "phone_number": "1234567890",
        "work_address": "123 Main St",
    }


@pytest.fixture
def sample_patient():
    """Sample patient data for testing."""
    return {
        "id": 1,
        "doctor_id": 1,
        "first_name": "Jane",
        "last_name": "Smith",
        "birth_date": "1990-05-15",
        "gender": "Female",
        "email_address": "jane.smith@example.com",
        "health_insurance_number": "INS123",
        "file_upload": None,
    }


@pytest.fixture
def authenticated_session(client, mock_mysql, mock_cursor, sample_doctor):
    """Create an authenticated session for testing protected routes."""
    # Mock the database query for login
    mock_cursor.fetchone.return_value = sample_doctor

    # Perform login
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_id"] = sample_doctor["id"]

    return client
