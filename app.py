import os  # Import the os module for operating system related operations
from datetime import datetime, timedelta  # Import the datetime module for date and time manipulation
from flask import Flask, render_template, request, redirect, flash, url_for, session, abort  # Import Flask modules for web application development
from flask_wtf import FlaskForm  # Import Flask-WTF module for handling forms in Flask
from wtforms import StringField, PasswordField, FileField  # Import modules for defining form fields
from wtforms.validators import DataRequired, Email, EqualTo  # Import modules for form field validation
from werkzeug.utils import secure_filename  # Import the secure_filename function for securely handling file uploads
from passlib.hash import sha256_crypt  # Import the sha256_crypt module for password hashing
from flask import send_from_directory  # Import send_from_directory for serving static files
import sqlite3  # Import the sqlite3 module for working with SQLite databases
from flask import g  # Import the g object for global variables in Flask
import secrets  # Import the secrets module for generating secure tokens

app = Flask(__name__)  # Create a Flask application instance
app.secret_key = 'a9db0889727b689e8b58ccfb639ac124cbec017db2192661'  # Set the secret key for the application
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Set the upload folder for file uploads
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Define the allowed file extensions

# Database configuration
DB_PATH = 'pp_users.db'  # Set the path to the SQLite database file
with sqlite3.connect(DB_PATH) as conn:
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, username TEXT UNIQUE, password TEXT)")  # Create the 'users' table if it doesn't exist

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # Set the lifetime of a session

# Flask-WTF form definitions
class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])  # Define a name field in the signup form
    email = StringField('Email', validators=[DataRequired(), Email()])  # Define an email field in the signup form
    username = StringField('Username', validators=[DataRequired()])  # Define a username field in the signup form
    password = PasswordField('Password', validators=[DataRequired()])  # Define a password field in the signup form
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])  # Define a confirm password field in the signup form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])  # Define a username field in the login form
    password = PasswordField('Password', validators=[DataRequired()])  # Define a password field in the login form

@app.before_request
def make_session_permanent():
    session.permanent = True  # Make the session permanent
    app.permanent_session_lifetime = timedelta(minutes=5)  # Set the lifetime of the session

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')  # Render the 'index.html' template

@app.route('/aboutUs')
def aboutUs():
    return render_template('aboutus.html')  # Render the 'aboutus.html' template

@app.route('/ourTeam')
def ourTeam():
    return render_template('ourTeam.html')  # Render the 'ourTeam.html' template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()  # Create an instance of the SignupForm
    if form.validate_on_submit():
        name = form.name.data  # Get the name from the form
        email = form.email.data  # Get the email from the form
        username = form.username.data  # Get the username from the form
        password = form.password.data  # Get the password from the form

        # Check if the email already exists in the database
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user_email = cursor.fetchone()
            if user_email:
                flash('Email already exists!')  # Display a flash message
                return redirect(url_for('signup'))  # Redirect to the signup page

            cursor.execute(
                "SELECT * FROM users WHERE username = ?", (username,))
            user_username = cursor.fetchone()
            if user_username:
                flash('Username already exists!')  # Display a flash message
                return redirect(url_for('signup'))  # Redirect to the signup page

            # Create a folder for the user
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
            os.makedirs(user_folder)

            password_hash = sha256_crypt.encrypt(password)  # Hash the password
            conn.execute(
                "INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                (name, email, username, password_hash)  # Insert user data into the 'users' table
            )
            conn.commit()

        flash('Signup successful! Please login.')  # Display a flash message
        return redirect(url_for('login'))  # Redirect to the login page

    return render_template('signup.html', form=form)  # Render the 'signup.html' template

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Create an instance of the LoginForm
    if form.validate_on_submit():
        username = form.username.data  # Get the username from the form
        password = form.password.data  # Get the password from the form

        # Open a new connection and retrieve user details from the database
        with sqlite3.connect(DB_PATH) as conn:
            result = conn.execute(
                "SELECT * FROM users WHERE username=?", (username,))
            user = result.fetchone()

        if user is not None and sha256_crypt.verify(password, user[4]):  # Verify the password
            session['username'] = user[3]  # Store the username in the session
            return redirect(url_for('gallery'))  # Redirect to the gallery page
        else:
            flash('Invalid username or password')  # Display a flash message

    return render_template('login.html', form=form)  # Render the 'login.html' template

@app.before_request
def load_user():
    if 'username' in session:
        with sqlite3.connect(DB_PATH) as conn:
            result = conn.execute(
                "SELECT name FROM users WHERE username=?", (session['username'],))
            user = result.fetchone()
            g.user = user[0] if user else None

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if 'username' in session:
        username = session['username']  # Get the username from the session
        # Open a new connection and retrieve user details from the database
        with sqlite3.connect(DB_PATH) as conn:
            result = conn.execute(
                "SELECT * FROM users WHERE username=?", (username,))
            user = result.fetchone()

        user_folder = os.path.join(
            app.config['UPLOAD_FOLDER'], username)  # Get the user's folder path
        # Get the list of user-uploaded images from the user's folder and sort them based on modification time
        image_files = os.listdir(user_folder)
        image_files = sorted(image_files, key=lambda f: os.path.getmtime(
            os.path.join(user_folder, f)), reverse=True)

        if request.method == 'POST':
            if 'image' not in request.files:
                flash('No file part')  # Display a flash message
                return redirect(request.url)  # Redirect to the current URL

            images = request.files.getlist('image')  # Get the list of uploaded images from the request

            for image in images:
                if image.filename == '':
                    flash('No selected file')  # Display a flash message
                    return redirect(request.url)  # Redirect to the current URL

                if allowed_file(image.filename):  # Check if the file has an allowed extension
                    filename = secure_filename(image.filename)  # Securely handle the filename
                    image.save(os.path.join(user_folder, filename))  # Save the image to the user's folder

            flash('Images uploaded successfully')  # Display a flash message
            return redirect(request.url)  # Redirect to the current URL

        return render_template('gallery.html', username=g.user, image_files=image_files)  # Render the 'gallery.html' template

    return redirect(url_for('login'))  # Redirect to the login page

@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('login'))  # Redirect to the login page

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in app.config['ALLOWED_EXTENSIONS']  # Check if the file has an allowed extension

@app.route('/uploads/<username>/<filename>')
def serve_image(username, filename):
    # Generate a secure access token for the image
    access_token = secrets.token_urlsafe(16)

    # Store the access token and corresponding filename in a session
    session['access_tokens'] = session.get('access_tokens', {})
    session['access_tokens'][access_token] = (username, filename)

    # Serve the image file using send_from_directory
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    return send_from_directory(user_folder, filename)

@app.route('/get_image/<access_token>')
def get_image(access_token):
    # Retrieve the filename associated with the access token
    filename = session['access_tokens'].get(access_token)

    if filename:
        # Serve the requested image
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        # Handle invalid access token
        abort(404)

@app.route('/delete', methods=['POST'])
def delete_image():
    # Get the filename of the image to be deleted from the request
    filename = request.form['filename']

    # Get the username from the session
    username = session['username']

    # Construct the path to the image file
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    file_path = os.path.join(user_folder, filename)

    # Check if the file exists and delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        flash('Image deleted successfully')  # Display a flash message
    else:
        flash('Image not found')  # Display a flash message

    return redirect(url_for('gallery'))  # Redirect to the gallery page

if __name__ == '__main__':
    app.run(debug=True)
