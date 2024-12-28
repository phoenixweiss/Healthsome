"""
Authentication Blueprint for the Healthsome application.

This module handles user authentication, including login, registration, and logout functionality.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from helpers.db_helpers import query_db, execute_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login.

    If the method is POST, validate user credentials and log in the user.
    If the method is GET, render the login page.

    Returns:
        str: Redirect to main page on success or render login template on failure.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle user registration.

    If the method is POST, validate input and create a new user.
    If the method is GET, render the registration page.

    Returns:
        str: Redirect to login page on success or render registration template on failure.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirmation = request.form['confirmation']

        if password != confirmation:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        existing_user = query_db('SELECT * FROM users WHERE username = ?', (username,), one=True)
        if existing_user:
            flash('Username already taken.', 'error')
            return render_template('auth/register.html')

        hashed_password = generate_password_hash(password)
        execute_db('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                   (username, hashed_password))
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    """
    Handle user logout.

    Clears the session and redirects to the login page.

    Returns:
        str: Redirect to the login page.
    """
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
