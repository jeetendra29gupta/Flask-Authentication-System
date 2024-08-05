from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import logging
import bcrypt
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__)

# Set up logging
logging.basicConfig(
    filename='app_log.log',
    level=logging.INFO,  # Changed to INFO for more detailed logs
    format='%(asctime)s.%(msecs)03d : %(levelname)s : %(module)s - %(funcName)s : %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

# Configure application
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variable or default
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app_databases.db')
db = SQLAlchemy(app)


def hashing_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    logging.info("Password hashed successfully.")
    return hashed


def checking_passwords(password, hashed_password):
    result = bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    logging.info(f"Password check result: {result}")
    return result


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(100), unique=True, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email_id = request.form.get("email_id")
        user_password = request.form.get("user_password")
        user = User.query.filter_by(email_id=email_id).first()

        if not user or not checking_passwords(user_password, user.user_password):
            logging.error(f"Failed login attempt for email_id: {email_id}")
            flash("Invalid Email ID or Password.", "Error")
            return redirect(url_for("login"))

        session['email_id'] = email_id
        logging.info(f"User logged in: {email_id}")
        return redirect(url_for("dashboard"))

    return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email_id = request.form.get("email_id")
        user_password = request.form.get("user_password")

        if User.query.filter_by(email_id=email_id).first():
            logging.error(f"Signup attempt with existing email_id: {email_id}")
            flash(f"{email_id} already exists.", "Error")
            return redirect(url_for("signup"))

        try:
            hashed_password = hashing_password(user_password)
            new_user = User(email_id=email_id, user_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            logging.info(f"New user registered: {email_id}")
            flash("You're registered successfully.", "Success")
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            logging.error(f"Error occurred while registering user: {email_id}", exc_info=True)
            flash("Error occurred while registering. Please try again.", "Error")

    return render_template('signup.html')


@app.route('/dashboard')
def dashboard():
    if 'email_id' not in session:
        logging.info("Attempt to access dashboard without a valid session.")
        flash("Invalid Session. Please log in again.", "Error")
        return redirect(url_for("login"))

    email_id = session['email_id']
    user = User.query.filter_by(email_id=email_id).first()
    return render_template('dashboard.html', user=user)


@app.route('/logout')
def logout():
    email_id = session.pop('email_id', None)
    logging.info(f"User logged out: {email_id}")
    flash("Logged out successfully.", "Success")
    return redirect(url_for("login"))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8181, debug=True)
