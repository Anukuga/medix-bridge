# MedixBridge Portal

A comprehensive web-based platform for healthcare professionals to manage patient data, including registration, editing, and file uploads, with secure authentication and responsive design.

---

## Features

- **User Authentication**: Secure signup and login with hashed passwords.
- **Patient Management**:
  - Register new patients with detailed personal and medical information.
  - Edit patient details, including file upload (stored as BLOB in MySQL).
  - View and manage the list of registered patients.
- **File Handling**: Upload and download patient-related files.
- **Responsive UI**: Built with Bootstrap for seamless functionality across devices.
- **Validation**: Client-side and server-side validation for forms.

---

## Technologies Used

- **Backend**: Flask, MySQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: `werkzeug.security` for password hashing
- **Database**: MySQL with `flask-mysqldb`
- **File Handling**: BLOB storage in MySQL

---

## Installation

### Prerequisites
- Python 3.13
- MySQL 9.0+ (running on port 8080)
- Virtual environment tool (e.g., `venv`)

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd MedixBridge
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MySQL database**:
   - Ensure your MySQL server is running on port `8080`.
   - Create a database: `CREATE DATABASE medixbridge;`
   - Update the `app.config` in `main.py` with your database credentials and port.
   - Run the SQL schema file to set up tables:
     ```bash
     mysql -u <username> -p -P 8080 medixbridge < schema.sql
     ```

5. **Run the application**:
   ```bash
   flask run --host=127.0.0.1 --port=5001
   ```

---

## Usage

1. Access the portal at `http://127.0.0.1:5001/`.
2. **Signup** to create a new account.
3. **Login** to manage patients:
   - Register new patients.
   - Edit details and upload files.
   - View and download uploaded files.
4. Logout securely after use.

---

## Folder Structure

```
MedixBridge/
├── app/
│   ├── static/          # Static assets (CSS, JS, Images)
│   │   ├── css/         # Stylesheets
│   │   ├── img/         # Images
│   │   ├── js/          # JavaScript
│   │   └── lib/         # Additional libraries (if any)
│   ├── templates/       # HTML templates
├── frontend/            # Frontend-only assets
│   ├── css/             # Frontend CSS
│   ├── fonts/           # Font files
│   ├── images/          # Frontend images
│   └── js/              # Frontend JavaScript
├── venv/                # Virtual environment (not included in repo)
├── .gitignore           # Git ignored files
├── main.py              # Flask application entry point
├── README.md            # Project documentation
└── requirements.txt     # Python dependencies
```

---

## Configuration Notes

- Ensure that MySQL is configured to use port `8080`. Update the `my.cnf` file with the following configuration if necessary:
  ```ini
  [mysqld]
  port = 8080
  bind-address = 127.0.0.1
  ```
- The Flask app will run on port `5001`. You can modify this in the `flask run` command if needed.

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a Pull Request.

---

