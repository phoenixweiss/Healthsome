# Healthsome

#### Video Demo: https://youtu.be/INIBr1H8LsQ

#### Description:

Healthsome is a web application developed by Pavel Tkachev as the final project for CS50x 2024. It helps users effortlessly manage their health metrics and track progress over time. With an intuitive interface and essential features, it simplifies monitoring blood pressure, weight, and medications.

#### Author

Name:    PAVEL TKACHEV
Github:  phoenixweiss
Edx:     phoenixweiss

## Key Features

- **Health Tracking**: Log and manage:
  - **Blood Pressure**: Record systolic, diastolic values, and pulse.
  - **Weight**: Track daily changes with precision.
  - **Medications**: Monitor dosages and track medication intake.
- **Easy Setup**: Simple installation and configuration using SQLite and environment variables.
- **User Accounts**: Login and registration to manage personal data securely.
- **Demo Data**: Option to pre-fill the application with sample data for testing.

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Visualization**: Chart.js, Bootstrap 5.3

## Installation Guide

1. Clone the repository:

   ```bash
   git clone git@github.com:phoenixweiss/Healthsome.git
   cd Healthsome
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows (PowerShell):

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in a `.env` file:

   ```env
   SECRET_KEY="YourSecretKey"
   SCHEMA_FILE=schema.sql
   DB_FILE=healthsome.db
   USERNAME=admin
   PASSWORD=pass
   ```

5. Initialize the database:

   ```bash
   python create_db.py
   ```

   If a database already exists, you will be prompted to recreate it.

6. Optionally, populate demo data:

   ```bash
   python populate_demo_data.py
   ```

## How to Run

1. Start the application:

   ```bash
   python app.py
   ```

2. Access it in your browser at:

   ```bash
   http://127.0.0.1:5000/
   ```

## Project Structure

- **`app.py`**: Entry point for the application.
- **`modules/`**: Contains blueprints for modular functionality:
  - **Authentication**: User login and registration.
  - **Metrics**: Logic for blood pressure, weight, and medications.
- **`helpers/`**: Utility scripts for database and time handling.
- **`templates/`**: HTML templates for rendering the user interface.
- **`static/`**: Contains CSS and other static assets.
- **`create_db.py`**: Initializes the database schema.
- **`populate_demo_data.py`**: Adds sample data for testing purposes.

## About Healthsome and CS50

Healthsome, developed by Pavel Tkachev, is the final project for CS50x 2024. This application reflects the core lessons of the course, including web development, database management, and Python programming. The project was completed in line with CS50's Academic Honesty principles and demonstrates the practical use of the skills gained.

CS50, taught by David J. Malan at Harvard University, is an introduction to computer science that covers programming fundamentals and foundational concepts. Through its partnership with edX, the course brings Harvard-level education to learners worldwide. I completed CS50x via edX, gaining valuable knowledge and experience throughout the course.

For more about CS50, visit [CS50's website](https://cs50.harvard.edu/x/2024/).

Thank you, CS50, for the knowledge, inspiration, and opportunity.
