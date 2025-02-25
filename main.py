from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
    send_from_directory,
)
from flask_pymysql import MySQL
from pymysql.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash
import base64
import os

app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app.secret_key = "your_secret_key"

# MySQL Configuration
app.config["pymysql_kwargs"] = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "port": 8080,
    "db": "medixbridge",
    "unix_socket": "/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock",
    "cursorclass": DictCursor,
}

mysql = MySQL(app)


FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./frontend")


@app.route("/")
def serve_index():
    """Serve the index.html file as the root page"""
    return send_file(os.path.join(FRONTEND_DIR, "index.html"))


@app.route("/<path:filename>")
def serve_static(filename):
    """Serve static files from the frontend directory"""
    return send_from_directory(FRONTEND_DIR, filename)


@app.route("/signin", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Retrieve form data
        email_address = request.form["email_address"]
        password = request.form["password"]

        # Query the database for user
        connection = mysql.connect
        cur = connection.cursor()
        cur.execute(
            "SELECT * FROM doctors_db WHERE email_address = %s", (email_address,)
        )
        user = cur.fetchone()
        cur.close()

        # Check if user exists and password matches
        if user and check_password_hash(user["password"], password):
            # Set session and redirect to a dashboard or home page
            session["logged_in"] = True
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect(
                url_for("dashboard")
            )  # Replace 'dashboard' with your actual route

        flash("Invalid email or password.", "danger")
        return redirect(url_for("signin"))

    # Render the signin page
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
@app.route("/register", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        birth_date = request.form["birth_date"]
        gender = request.form["gender"]
        license_number = request.form["license_number"]
        nationality = request.form["nationality"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]
        work_address = request.form["work_address"]
        specialty = request.form["specialty"]
        password = request.form["password"]

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        connection = mysql.connect
        cur = connection.cursor()
        cur.execute(
            """
            INSERT INTO doctors_db 
            (first_name, last_name, birth_date, gender, license_number, nationality, 
            email_address, phone_number, work_address, specialty, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                first_name,
                last_name,
                birth_date,
                gender,
                license_number,
                nationality,
                email_address,
                phone_number,
                work_address,
                specialty,
                hashed_password,
            ),
        )
        mysql.connection.commit()
        cur.close()

        # Set a flash message and redirect to the login page
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("signin"))

    # Render the signup page
    return render_template("signup.html")


@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for("signin"))

    user_id = session["user_id"]

    # Query the database to fetch the doctor's information
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT first_name, last_name, specialty 
        FROM doctors_db 
        WHERE id = %s
    """,
        (user_id,),
    )
    doctor = cur.fetchone()
    cur.close()

    # Check if doctor data is retrieved successfully
    if not doctor:
        flash("User not found.", "danger")
        return redirect(url_for("signin"))

    # Render the dashboard template with the doctor's data
    return render_template(
        "dashboard.html",
        doctor_first_name=doctor["first_name"],
        doctor_last_name=doctor["last_name"],
        doctor_specialty=doctor["specialty"],
    )


@app.route("/my-profile", methods=["GET", "POST"])
def my_profile():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to access your profile.", "warning")
        return redirect(url_for("signin"))

    user_id = session["user_id"]

    if request.method == "POST":
        # Get updated form data from the request
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        gender = request.form.get("gender")
        email_address = request.form.get("email_address")
        phone_number = request.form.get("phone_number")
        work_address = request.form.get("work_address")
        specialty = request.form.get("specialty")
        nationality = request.form.get("nationality")
        license_number = request.form.get("license_number")

        # Update the user's data in the database
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """
                UPDATE doctors_db
                SET first_name = %s, last_name = %s, birth_date = %s, gender = %s, 
                    email_address = %s, phone_number = %s, work_address = %s, 
                    specialty = %s, nationality = %s, license_number = %s
                WHERE id = %s
                """,
                (
                    first_name,
                    last_name,
                    birth_date,
                    gender,
                    email_address,
                    phone_number,
                    work_address,
                    specialty,
                    nationality,
                    license_number,
                    user_id,
                ),
            )
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            raise e
        finally:
            cur.close()

        # Display a success message
        flash("Profile updated successfully!", "success")
        return redirect(url_for("my_profile"))

    # Query the database to fetch the user's current profile data
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT first_name, last_name, birth_date, gender, email_address, 
               phone_number, work_address, specialty, nationality, license_number
        FROM doctors_db WHERE id = %s
        """,
        (user_id,),
    )
    user_profile = cur.fetchone()
    cur.close()

    if not user_profile:
        flash("User profile not found.", "danger")
        return redirect(url_for("dashboard"))

    # Render the my-profile page with user profile data
    return render_template("my-profile.html", user_profile=user_profile)


@app.route("/update-password", methods=["POST"])
def update_password():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to update your password.", "warning")
        return redirect(url_for("signin"))

    # Fetch the logged-in user's ID
    user_id = session["user_id"]

    # Retrieve form data
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    # Check if new password and confirm password match
    if new_password != confirm_password:
        flash("New password and confirm password do not match.", "danger")
        return redirect(url_for("my_profile"))

    try:
        # Fetch user's current password hash from the database
        connection = mysql.connect
        cur = connection.cursor()
        cur.execute("SELECT password FROM doctors_db WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()

        if not user:
            flash("User not found.", "danger")
            return redirect(url_for("signin"))

        # Verify the old password
        if not check_password_hash(user["password"], old_password):
            return {"error": "Incorrect old password"}, 400

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update the password in the database
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE doctors_db SET password = %s WHERE id = %s",
            (hashed_password, user_id),
        )
        mysql.connection.commit()
        cur.close()

        flash("Password updated successfully!", "success")
        return redirect(url_for("my_profile"))

    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect(url_for("my_profile"))


@app.route("/register-patient", methods=["GET", "POST"])
def register_patient():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to register a patient.", "warning")
        return redirect(url_for("signin"))

    # Fetch doctor's details using the PRIMARY_KEY `id` from doctors_db
    user_id = session[
        "user_id"
    ]  # Assuming `user_id` is stored in the session upon login
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT id, first_name, last_name, specialty 
        FROM doctors_db 
        WHERE id = %s
        """,
        (user_id,),
    )
    doctor = cur.fetchone()
    cur.close()

    if not doctor:
        flash("Doctor's details could not be found.", "danger")
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        # Retrieve form data
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birth_date = request.form.get("birth_date")
        gender = request.form.get("gender")
        nationality = request.form.get("nationality")
        health_insurance_number = request.form.get("health_insurance_number")
        email_address = request.form.get("email")
        phone_number = request.form.get("phone_number")
        address = request.form.get("address")
        emergency_contact_name = request.form.get("emergency_contact_name")
        emergency_contact_number = request.form.get("emergency_contact_number")
        height = request.form.get("height")
        weight = request.form.get("weight")
        blood_group = request.form.get("blood_group")
        genotype = request.form.get("genotype")
        allergies = request.form.get("allergies")
        chronic_diseases = request.form.get("chronic_diseases")
        disabilities = request.form.get("disabilities")
        vaccines = request.form.get("vaccines")
        medications = request.form.get("medications")
        doctors_note = request.form.get("doctors_note")

        # Insert patient data into the database along with the doctor_id
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                """
                INSERT INTO patients_db (
                    doctor_id, first_name, last_name, birth_date, gender, nationality, health_insurance_number,
                    email_address, phone_number, address, emergency_contact_name, emergency_contact_number,
                    height, weight, blood_group, genotype, allergies, chronic_diseases, disabilities,
                    vaccines, medications, doctors_note
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    doctor["id"],
                    first_name,
                    last_name,
                    birth_date,
                    gender,
                    nationality,
                    health_insurance_number,
                    email_address,
                    phone_number,
                    address,
                    emergency_contact_name,
                    emergency_contact_number,
                    height,
                    weight,
                    blood_group,
                    genotype,
                    allergies,
                    chronic_diseases,
                    disabilities,
                    vaccines,
                    medications,
                    doctors_note,
                ),
            )
            mysql.connection.commit()
            flash("Patient registered successfully!", "success")
        except Exception as e:
            mysql.connection.rollback()
            flash(f"An error occurred: {e}", "danger")
        finally:
            cur.close()

        return redirect(url_for("register_patient"))

    # Render the registration form with doctor's details
    return render_template(
        "register-patient.html",
        doctor_first_name=doctor["first_name"],
        doctor_last_name=doctor["last_name"],
        doctor_specialty=doctor["specialty"],
    )


@app.route("/my-patients", methods=["GET", "POST"])
def my_patients():
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to view your patients.", "warning")
        return redirect(url_for("signin"))

    # Fetch the doctor's ID from the session
    user_id = session["user_id"]

    # Query to retrieve patients associated with the logged-in doctor
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT 
            patients_db.id AS patient_id,
            patients_db.first_name,
            patients_db.last_name,
            patients_db.birth_date,
            patients_db.gender,
            patients_db.email_address,
            patients_db.health_insurance_number
        FROM 
            patients_db
        WHERE 
            patients_db.doctor_id = %s
        """,
        (user_id,),
    )
    patients = cur.fetchall()
    cur.close()

    # Calculate the total number of patients
    total_patients = len(patients)

    # Fetch doctor details for the header
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT first_name, last_name, specialty 
        FROM doctors_db 
        WHERE id = %s
        """,
        (user_id,),
    )
    doctor = cur.fetchone()
    cur.close()

    if not doctor:
        flash("Unable to fetch doctor information.", "danger")
        return redirect(url_for("dashboard"))

    # Render the my-patients.html template
    return render_template(
        "my-patients.html",
        doctor_first_name=doctor["first_name"],
        doctor_last_name=doctor["last_name"],
        doctor_specialty=doctor["specialty"],
        total_patients=total_patients,
        patients=patients,
    )


@app.route("/delete-patient/<int:patient_id>", methods=["POST"])
def delete_patient(patient_id):
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to delete a patient.", "warning")
        return redirect(url_for("signin"))

    doctor_id = session["user_id"]

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "DELETE FROM patients_db WHERE id = %s AND doctor_id = %s",
            (patient_id, doctor_id),
        )
        mysql.connection.commit()
        cur.close()

        flash("Patient deleted successfully!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"An error occurred while deleting the patient: {e}", "danger")

    return redirect(url_for("my_patients"))


@app.route("/edit-patient/<int:patient_id>", methods=["GET", "POST"])
def edit_patient(patient_id):
    if "logged_in" not in session or not session["logged_in"]:
        flash("Please log in to edit a patient's details.", "warning")
        return redirect(url_for("signin"))

    doctor_id = session["user_id"]  # Retrieve logged-in doctor's ID

    # Fetch the logged-in doctor's details
    connection = mysql.connect
    cur = connection.cursor()
    cur.execute(
        """
        SELECT first_name, last_name, specialty
        FROM doctors_db
        WHERE id = %s
        """,
        (doctor_id,),
    )
    doctor = cur.fetchone()

    if not doctor:
        flash("Doctor details could not be retrieved.", "danger")
        return redirect(url_for("signin"))

    # Handle POST request for updating the patient's data
    if request.method == "POST":
        try:
            data = request.form
            uploaded_file = request.files.get("file_upload")  # Get uploaded file

            # Convert file to BLOB (bytes) if a file was uploaded
            file_blob = (
                uploaded_file.read()
                if uploaded_file and uploaded_file.filename
                else None
            )

            # Prepare data
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            birth_date = data.get("birth_date", None)
            gender = data.get("gender", "")
            nationality = data.get("nationality", "")
            health_insurance_number = data.get("health_insurance_number", "")
            email_address = data.get("email", "")
            phone_number = data.get("phone_number", "")
            address = data.get("address", "")
            emergency_contact_name = data.get("emergency_contact_name", "")
            emergency_contact_number = data.get("emergency_contact_number", "")
            height = float(data.get("height", 0)) if data.get("height") else None
            weight = float(data.get("weight", 0)) if data.get("weight") else None
            blood_group = data.get("blood_group", "")
            genotype = data.get("genotype", "")
            allergies = data.get("allergies", "")
            chronic_diseases = data.get("chronic_diseases", "")
            disabilities = data.get("disabilities", "")
            vaccines = data.get("vaccines", "")
            medications = data.get("medications", "")
            doctors_note = data.get("doctors_note", "")

            # Create a new cursor
            cur = mysql.connection.cursor()

            # Update patient details
            if file_blob:
                cur.execute(
                    """
                    UPDATE patients_db
                    SET first_name = %s, last_name = %s, birth_date = %s, gender = %s, 
                        nationality = %s, health_insurance_number = %s, email_address = %s, 
                        phone_number = %s, address = %s, emergency_contact_name = %s, 
                        emergency_contact_number = %s, height = %s, weight = %s, blood_group = %s, 
                        genotype = %s, allergies = %s, chronic_diseases = %s, disabilities = %s, 
                        vaccines = %s, medications = %s, doctors_note = %s, file_upload = %s
                    WHERE id = %s AND doctor_id = %s
                    """,
                    (
                        first_name,
                        last_name,
                        birth_date,
                        gender,
                        nationality,
                        health_insurance_number,
                        email_address,
                        phone_number,
                        address,
                        emergency_contact_name,
                        emergency_contact_number,
                        height,
                        weight,
                        blood_group,
                        genotype,
                        allergies,
                        chronic_diseases,
                        disabilities,
                        vaccines,
                        medications,
                        doctors_note,
                        file_blob,
                        patient_id,
                        doctor_id,
                    ),
                )
            else:
                cur.execute(
                    """
                    UPDATE patients_db
                    SET first_name = %s, last_name = %s, birth_date = %s, gender = %s, 
                        nationality = %s, health_insurance_number = %s, email_address = %s, 
                        phone_number = %s, address = %s, emergency_contact_name = %s, 
                        emergency_contact_number = %s, height = %s, weight = %s, blood_group = %s, 
                        genotype = %s, allergies = %s, chronic_diseases = %s, disabilities = %s, 
                        vaccines = %s, medications = %s, doctors_note = %s
                    WHERE id = %s AND doctor_id = %s
                    """,
                    (
                        first_name,
                        last_name,
                        birth_date,
                        gender,
                        nationality,
                        health_insurance_number,
                        email_address,
                        phone_number,
                        address,
                        emergency_contact_name,
                        emergency_contact_number,
                        height,
                        weight,
                        blood_group,
                        genotype,
                        allergies,
                        chronic_diseases,
                        disabilities,
                        vaccines,
                        medications,
                        doctors_note,
                        patient_id,
                        doctor_id,
                    ),
                )

            mysql.connection.commit()
            flash("Patient details updated successfully!", "success")
            return redirect(url_for("edit_patient", patient_id=patient_id))
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
            return redirect(url_for("edit_patient", patient_id=patient_id))
        finally:
            cur.close()

    # Handle GET request to fetch patient data
    cur.execute(
        """
        SELECT * FROM patients_db
        WHERE id = %s AND doctor_id = %s
        """,
        (patient_id, doctor_id),
    )
    patient = cur.fetchone()
    cur.close()

    # Convert BLOB to Base64 for rendering in HTML
    file_data = None
    if patient["file_upload"]:
        file_data = base64.b64encode(patient["file_upload"]).decode("utf-8")

    return render_template(
        "edit-patient.html",
        patient=patient,
        patient_id=patient_id,
        file_data=file_data,  # Send encoded file to the frontend
        doctor_first_name=doctor["first_name"],
        doctor_last_name=doctor["last_name"],
        doctor_specialty=doctor["specialty"],
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("signin"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
    # NOTE: Change to    app.run(debug=True)    when running locally
    # ssh -L 5000:localhost:5000 remote-laptop-username@remote-laptop-ip
    # http://localhost:5001/ or http://remote-laptop-ip:5000/ in your browser
