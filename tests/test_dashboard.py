"""Tests for dashboard and profile routes."""


class TestDashboard:
    """Tests for the dashboard route."""

    def test_dashboard_requires_login(self, client):
        """Test that dashboard redirects when not logged in."""
        response = client.get("/dashboard", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to signin

    def test_dashboard_with_auth(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test dashboard access when logged in."""
        mock_cursor.fetchone.return_value = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }

        response = authenticated_session.get("/dashboard")
        assert response.status_code == 200

    def test_dashboard_user_not_found(
        self, authenticated_session, mock_mysql, mock_cursor
    ):
        """Test dashboard when user doesn't exist in database."""
        mock_cursor.fetchone.return_value = None

        response = authenticated_session.get("/dashboard", follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to signin


class TestMyProfile:
    """Tests for the my-profile route."""

    def test_my_profile_requires_login(self, client):
        """Test that my-profile redirects when not logged in."""
        response = client.get("/my-profile", follow_redirects=True)
        assert response.status_code == 200

    def test_my_profile_get(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test GET request to my-profile page."""
        mock_cursor.fetchone.return_value = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "birth_date": sample_doctor["birth_date"],
            "gender": sample_doctor["gender"],
            "email_address": sample_doctor["email_address"],
            "phone_number": sample_doctor["phone_number"],
            "work_address": sample_doctor["work_address"],
            "specialty": sample_doctor["specialty"],
            "nationality": sample_doctor["nationality"],
            "license_number": sample_doctor["license_number"],
        }

        response = authenticated_session.get("/my-profile")
        assert response.status_code == 200

    def test_my_profile_post_update(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test POST request to update profile."""
        mock_cursor.fetchone.return_value = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "birth_date": sample_doctor["birth_date"],
            "gender": sample_doctor["gender"],
            "email_address": sample_doctor["email_address"],
            "phone_number": sample_doctor["phone_number"],
            "work_address": sample_doctor["work_address"],
            "specialty": sample_doctor["specialty"],
            "nationality": sample_doctor["nationality"],
            "license_number": sample_doctor["license_number"],
        }

        response = authenticated_session.post(
            "/my-profile",
            data={
                "first_name": "John",
                "last_name": "Updated",
                "birth_date": "1980-01-01",
                "gender": "Male",
                "email_address": "john.updated@example.com",
                "phone_number": "1111111111",
                "work_address": "456 New St",
                "specialty": "Neurology",
                "nationality": "American",
                "license_number": "LIC999",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert mock_cursor.execute.called
        assert mock_mysql.connection.commit.called

    def test_my_profile_not_found(self, authenticated_session, mock_mysql, mock_cursor):
        """Test my-profile when user profile doesn't exist."""
        mock_cursor.fetchone.return_value = None

        response = authenticated_session.get("/my-profile", follow_redirects=True)
        assert response.status_code == 200


class TestUpdatePassword:
    """Tests for the update-password route."""

    def test_update_password_requires_login(self, client):
        """Test that update-password redirects when not logged in."""
        response = client.post("/update-password", follow_redirects=True)
        assert response.status_code == 200

    def test_update_password_success(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test successful password update."""
        # First call returns user with old password for verification
        # After redirect to my_profile, it needs user profile data
        user_profile = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "birth_date": sample_doctor["birth_date"],
            "gender": sample_doctor["gender"],
            "email_address": sample_doctor["email_address"],
            "phone_number": sample_doctor["phone_number"],
            "work_address": sample_doctor["work_address"],
            "specialty": sample_doctor["specialty"],
            "nationality": sample_doctor["nationality"],
            "license_number": sample_doctor["license_number"],
        }
        # First fetchone: get password for verification
        # Second fetchone: get user profile after redirect
        mock_cursor.fetchone.side_effect = [
            {"password": sample_doctor["password"]},
            user_profile,
        ]

        response = authenticated_session.post(
            "/update-password",
            data={
                "old_password": "password123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert mock_cursor.execute.called

    def test_update_password_mismatch(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test password update with mismatched new passwords."""
        response = authenticated_session.post(
            "/update-password",
            data={
                "old_password": "password123",
                "new_password": "newpassword123",
                "confirm_password": "differentpassword",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        # Should not update password

    def test_update_password_wrong_old_password(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test password update with incorrect old password."""
        mock_cursor.fetchone.return_value = {"password": sample_doctor["password"]}

        response = authenticated_session.post(
            "/update-password",
            data={
                "old_password": "wrongoldpassword",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123",
            },
        )

        # Should return 400 error
        assert response.status_code == 400