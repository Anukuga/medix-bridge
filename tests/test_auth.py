"""Tests for authentication routes (signin, signup, logout)."""


class TestSignin:
    """Tests for the signin/login route."""

    def test_signin_get(self, client):
        """Test GET request to signin page."""
        response = client.get("/signin")
        assert response.status_code == 200

    def test_signin_via_login_route(self, client):
        """Test that /login route also works."""
        response = client.get("/login")
        assert response.status_code == 200

    def test_signin_post_success(self, client, mock_mysql, mock_cursor, sample_doctor):
        """Test successful login with correct credentials."""
        mock_cursor.fetchone.return_value = sample_doctor

        response = client.post(
            "/signin",
            data={
                "email_address": "john.doe@example.com",
                "password": "password123",
            },
            follow_redirects=True,
        )

        # Should redirect to dashboard
        assert response.status_code == 200
        # Check session was set
        with client.session_transaction() as sess:
            assert sess.get("logged_in") is True
            assert sess.get("user_id") == sample_doctor["id"]

    def test_signin_post_invalid_email(self, client, mock_mysql, mock_cursor):
        """Test login with non-existent email."""
        mock_cursor.fetchone.return_value = None

        response = client.post(
            "/signin",
            data={
                "email_address": "nonexistent@example.com",
                "password": "password123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should not be logged in
        with client.session_transaction() as sess:
            assert sess.get("logged_in") is None

    def test_signin_post_invalid_password(
        self, client, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test login with incorrect password."""
        mock_cursor.fetchone.return_value = sample_doctor

        response = client.post(
            "/signin",
            data={
                "email_address": "john.doe@example.com",
                "password": "wrongpassword",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should not be logged in
        with client.session_transaction() as sess:
            assert sess.get("logged_in") is None


class TestSignup:
    """Tests for the signup/register route."""

    def test_signup_get(self, client):
        """Test GET request to signup page."""
        response = client.get("/signup")
        assert response.status_code == 200

    def test_signup_via_register_route(self, client):
        """Test that /register route also works."""
        response = client.get("/register")
        assert response.status_code == 200

    def test_signup_post_success(self, client, mock_mysql, mock_cursor):
        """Test successful user registration."""
        response = client.post(
            "/signup",
            data={
                "first_name": "Jane",
                "last_name": "Smith",
                "birth_date": "1990-01-01",
                "gender": "Female",
                "license_number": "LIC456",
                "nationality": "Canadian",
                "email_address": "jane.smith@example.com",
                "phone_number": "9876543210",
                "work_address": "456 Oak Ave",
                "specialty": "Pediatrics",
                "password": "securepass123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should redirect to signin page
        assert mock_cursor.execute.called
        assert mock_mysql.connection.commit.called


class TestLogout:
    """Tests for the logout route."""

    def test_logout(self, authenticated_session):
        """Test logout clears session."""
        # First verify we're logged in
        with authenticated_session.session_transaction() as sess:
            assert sess.get("logged_in") is True

        # Logout
        response = authenticated_session.get("/logout", follow_redirects=True)
        assert response.status_code == 200

        # Verify session is cleared
        with authenticated_session.session_transaction() as sess:
            assert sess.get("logged_in") is None
            assert sess.get("user_id") is None
