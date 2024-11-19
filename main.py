from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__, static_folder="app/static", template_folder="app/templates")
app.secret_key = 'your_secret_key'

# MySQL Configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "medixbridge"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_UNIX_SOCKET"] = "/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"

mysql = MySQL(app)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Retrieve form data
        email_address = request.form["email_address"]
        password = request.form["password"]

        # Query the database for user
        cur = mysql.connection.cursor(cursorclass=DictCursor)
        cur.execute("SELECT * FROM doctors_db WHERE email_address = %s", (email_address,))
        user = cur.fetchone()
        cur.close()

        # Check if user exists and password matches
        if user and check_password_hash(user["password"], password):
            # Set session and redirect to a dashboard or home page
            session["logged_in"] = True
            session["user_id"] = user["id"]
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))  # Replace 'dashboard' with your actual route

        flash("Invalid email or password.", "danger")
        return redirect(url_for("signin"))

    # Render the signin page
    return render_template("signin.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # Retrieve form data
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        birth_date = request.form["birth_date"]
        email_address = request.form["email_address"]
        phone_number = request.form["phone_number"]
        work_address = request.form["work_address"]
        specialty = request.form["specialty"]
        password = request.form["password"]

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        cur = mysql.connection.cursor(cursorclass=DictCursor)
        cur.execute(
            """
            INSERT INTO doctors_db (first_name, last_name, email_address, phone_number, work_address, specialty, birth_date, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
            (
                first_name,
                last_name,
                email_address,
                phone_number,
                work_address,
                specialty,
                birth_date,
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
    cur = mysql.connection.cursor(cursorclass=DictCursor)
    cur.execute("SELECT last_name FROM doctors_db WHERE id = %s", (user_id,))
    doctor = cur.fetchone()
    cur.close()
    
    # Check if doctor data is retrieved successfully
    if not doctor:
        flash("User not found.", "danger")
        return redirect(url_for("signin"))

    # Render the dashboard template with the doctor's last name
    return render_template("dashboard.html", doctor_last_name=doctor["last_name"])


if __name__ == "__main__":
    app.run(debug=True)
