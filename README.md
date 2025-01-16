PixelPalace

PixelPalace is a Python Flask-based web application that allows users to upload and delete photos. This project demonstrates the use of Flask for web development, along with integration of user authentication and photo management features.

Features

Add photos to the platform.

Delete photos as needed.

Secure user authentication with password hashing.

Requirements

To run PixelPalace, the following dependencies must be installed:

Python 3.8 or later

Flask

Flask-WTF

Passlib

Email Validator

Installation

Clone the Repository

git clone https://github.com/your-username/pixelPalace.git
cd pixelPalace

Set Up a Virtual Environment (Optional but Recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
Install the required Python packages using pip:

pip install flask flask-wtf passlib email-validator

Run the Application
Start the Flask development server:

flask run

The application will be accessible at http://127.0.0.1:5000/.

Usage

Adding Photos

Log in to the application.

Navigate to the "Add Photo" section.

Upload your desired photo.

Deleting Photos

View your uploaded photos.

Select the photo you want to delete.

Confirm the deletion.

Project Structure

app.py: The main application file.

templates/: Directory containing HTML templates.

static/: Directory for static files (e.g., CSS, JavaScript, images).

requirements.txt: List of dependencies for the project.

Dependencies

The following Python packages are required:

Flask: Web framework for building the application.

Flask-WTF: For handling forms securely.

Passlib: For secure password hashing.

Email Validator: To validate email addresses in forms.

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgments

Special thanks to the developers and contributors of Flask and its extensions for making web development in Python seamless.

