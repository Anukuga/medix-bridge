"""Tests for patient management routes."""


class TestRegisterPatient:
    """Tests for the register-patient route."""

    def test_register_patient_requires_login(self, client):
        """Test that register-patient redirects when not logged in."""
        response = client.get("/register-patient", follow_redirects=True)
        assert response.status_code == 200

    def test_register_patient_get(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test GET request to register-patient page."""
        mock_cursor.fetchone.return_value = {
            "id": sample_doctor["id"],
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }

        response = authenticated_session.get("/register-patient")
        assert response.status_code == 200

    def test_register_patient_post_success(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test successful patient registration."""
        # Mock doctor fetch
        mock_cursor.fetchone.return_value = {
            "id": sample_doctor["id"],
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }

        response = authenticated_session.post(
            "/register-patient",
            data={
                "first_name": "Patient",
                "last_name": "One",
                "birth_date": "1995-03-20",
                "gender": "Male",
                "nationality": "American",
                "health_insurance_number": "INS001",
                "email": "patient.one@example.com",
                "phone_number": "5551234567",
                "address": "789 Patient St",
                "emergency_contact_name": "Emergency Contact",
                "emergency_contact_number": "5559876543",
                "height": "175",
                "weight": "70",
                "blood_group": "O+",
                "genotype": "AA",
                "allergies": "None",
                "chronic_diseases": "None",
                "disabilities": "None",
                "vaccines": "All",
                "medications": "None",
                "doctors_note": "Healthy patient",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert mock_cursor.execute.called
        assert mock_mysql.connection.commit.called

    def test_register_patient_doctor_not_found(
        self, authenticated_session, mock_mysql, mock_cursor
    ):
        """Test register-patient when doctor doesn't exist."""
        mock_cursor.fetchone.return_value = None

        response = authenticated_session.get("/register-patient", follow_redirects=True)
        assert response.status_code == 200


class TestMyPatients:
    """Tests for the my-patients route."""

    def test_my_patients_requires_login(self, client):
        """Test that my-patients redirects when not logged in."""
        response = client.get("/my-patients", follow_redirects=True)
        assert response.status_code == 200

    def test_my_patients_get(
        self,
        authenticated_session,
        mock_mysql,
        mock_cursor,
        sample_doctor,
        sample_patient,
    ):
        """Test GET request to my-patients page."""
        # First call returns patients list
        # Second call returns doctor info
        mock_cursor.fetchall.return_value = [
            {
                "patient_id": sample_patient["id"],
                "first_name": sample_patient["first_name"],
                "last_name": sample_patient["last_name"],
                "birth_date": sample_patient["birth_date"],
                "gender": sample_patient["gender"],
                "email_address": sample_patient["email_address"],
                "health_insurance_number": sample_patient["health_insurance_number"],
            }
        ]
        mock_cursor.fetchone.return_value = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }

        response = authenticated_session.get("/my-patients")
        assert response.status_code == 200

    def test_my_patients_empty_list(
        self, authenticated_session, mock_mysql, mock_cursor, sample_doctor
    ):
        """Test my-patients with no patients."""
        mock_cursor.fetchall.return_value = []
        mock_cursor.fetchone.return_value = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }

        response = authenticated_session.get("/my-patients")
        assert response.status_code == 200


class TestDeletePatient:
    """Tests for the delete-patient route."""

    def test_delete_patient_requires_login(self, client):
        """Test that delete-patient redirects when not logged in."""
        response = client.post("/delete-patient/1", follow_redirects=True)
        assert response.status_code == 200

    def test_delete_patient_success(
        self, authenticated_session, mock_mysql, mock_cursor
    ):
        """Test successful patient deletion."""
        response = authenticated_session.post(
            "/delete-patient/1",
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert mock_cursor.execute.called
        assert mock_mysql.connection.commit.called


class TestEditPatient:
    """Tests for the edit-patient route."""

    def test_edit_patient_requires_login(self, client):
        """Test that edit-patient redirects when not logged in."""
        response = client.get("/edit-patient/1", follow_redirects=True)
        assert response.status_code == 200

    def test_edit_patient_get(
        self,
        authenticated_session,
        mock_mysql,
        mock_cursor,
        sample_doctor,
        sample_patient,
    ):
        """Test GET request to edit-patient page."""
        # First call returns doctor info
        # Second call returns patient info
        doctor_data = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }
        patient_data = {**sample_patient}

        mock_cursor.fetchone.side_effect = [doctor_data, patient_data]

        response = authenticated_session.get("/edit-patient/1")
        assert response.status_code == 200

    def test_edit_patient_post_success(
        self,
        authenticated_session,
        mock_mysql,
        mock_cursor,
        sample_doctor,
        sample_patient,
    ):
        """Test POST request to update patient."""
        # Mock doctor fetch (first call)
        # After redirect, need to fetch doctor again and patient data
        doctor_data = {
            "first_name": sample_doctor["first_name"],
            "last_name": sample_doctor["last_name"],
            "specialty": sample_doctor["specialty"],
        }
        # Create complete patient data with all required fields including file_upload
        patient_data = {
            **sample_patient,
            "file_upload": None,  # Ensure file_upload key exists
        }
        # First fetchone: doctor before update
        # After redirect: doctor fetch, then patient fetch
        mock_cursor.fetchone.side_effect = [
            doctor_data,  # Initial doctor fetch
            doctor_data,  # Doctor fetch after redirect
            patient_data,  # Patient fetch after redirect
        ]

        response = authenticated_session.post(
            "/edit-patient/1",
            data={
                "first_name": "Updated",
                "last_name": "Patient",
                "birth_date": "1995-03-20",
                "gender": "Male",
                "nationality": "American",
                "health_insurance_number": "INS001",
                "email": "updated@example.com",
                "phone_number": "5551234567",
                "address": "789 Patient St",
                "emergency_contact_name": "Emergency Contact",
                "emergency_contact_number": "5559876543",
                "height": "180",
                "weight": "75",
                "blood_group": "O+",
                "genotype": "AA",
                "allergies": "None",
                "chronic_diseases": "None",
                "disabilities": "None",
                "vaccines": "All",
                "medications": "None",
                "doctors_note": "Updated note",
            },
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert mock_cursor.execute.called
        assert mock_mysql.connection.commit.called

    def test_edit_patient_doctor_not_found(
        self, authenticated_session, mock_mysql, mock_cursor
    ):
        """Test edit-patient when doctor doesn't exist."""
        mock_cursor.fetchone.return_value = None

        response = authenticated_session.get("/edit-patient/1", follow_redirects=True)
        assert response.status_code == 200
