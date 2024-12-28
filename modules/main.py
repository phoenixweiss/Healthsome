"""
Main Blueprint for the Healthsome application.

This module defines the main routes for the application, handling requests to the home page and the About page.
"""

from flask import Blueprint, render_template, session

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """
    Handle requests to the home page.

    Returns:
        str: Rendered HTML template for the home page if user is logged in,
        otherwise redirects to the login page.
    """
    if 'user_id' in session:
        return render_template('index.html')
    return render_template('auth/login.html')

@bp.route('/about')
def about():
    """
    Handle requests to the About page.

    Returns:
        str: Rendered HTML template for the About page.
    """
    return render_template('about.html')
