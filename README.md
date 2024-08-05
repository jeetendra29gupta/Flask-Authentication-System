# Flask Authentication System

Welcome to the Flask Authentication System! This project demonstrates a basic user authentication system built using Flask, SQLAlchemy, and bcrypt for password hashing.

## Features

- **User Authentication:** Secure login and registration with hashed passwords.
- **Session Management:** Persistent user sessions with login and logout functionality.
- **Error Handling:** Detailed logging and error management for a robust experience.

## Tech Stack

- **Flask:** Web framework for building the web application.
- **SQLAlchemy:** ORM for database interactions.
- **bcrypt:** Library for hashing passwords securely.
- **SQLite:** Default database, but can be configured to use other databases.

## Getting Started

### Prerequisites

Make sure you have Python 3.x installed. You’ll also need to install the following Python packages:

- Flask
- Flask-SQLAlchemy
- bcrypt
- SQLAlchemy

### Usage
* Login: Navigate to /login to log in with your email and password.
* Signup: Navigate to /signup to register a new account.
* Dashboard: Access the user dashboard at /dashboard after logging in.
* Logout: Log out by navigating to /logout.

### Demo
You can see the live demo of the application here: 
[Flask Authentication System Demo](https://jeetendra29gupta.pythonanywhere.com/)


### You can install these packages using pip:

```bash
pip install Flask Flask-SQLAlchemy bcrypt
```

### Configuration

* Clone the repository:
```bash
git clone https://github.com/jeetendra29gupta/Flask-Authentication-System.git
cd Flask-Authentication-System
```

* Set Up Environment Variables:
Create a .env file in the root directory to store your environment variables:
```bash
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///app_databases.db
```

* Initialize the Database & Run the Application:Run the Flask application to create the database and tables:
```bash
python flask_authentication_system_main.py
```
The application will be available at http://localhost:8181.