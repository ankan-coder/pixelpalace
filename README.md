
# PixelPalace

PixelPalace is a Python Flask-based application that allows users to add and delete photos seamlessly. This project uses Flask for web development and several other essential Python libraries.

## Features
- Add photos to your gallery.
- Delete photos from your gallery.
- Secure user authentication.
- Email validation for user inputs.

## Requirements

Before running the project, ensure you have the following installed:

1. Python (3.6 or higher)
2. Pip (Python package manager)

Required Python packages (install via pip):
- `flask`
- `flask-wtf`
- `passlib`
- `email-validator`

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/pixelPalace.git
   cd pixelPalace
   ```

2. **Create a Virtual Environment**  
   Create and activate a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install Dependencies**  
   Install the required Python packages:
   ```bash
   pip install flask flask-wtf passlib email-validator
   ```

4. **Run the Application**  
   Start the Flask development server:
   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000`.

## Usage

- Visit the home page of PixelPalace.
- Add photos to your gallery using the upload feature.
- Delete photos as needed with the delete option.

## Troubleshooting

- If you encounter the error `Exception: Install 'email_validator' for email validation support`, make sure you have installed `email-validator` using pip.

## Contributing

Feel free to contribute to PixelPalace! Fork the repository, create a new branch, and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
