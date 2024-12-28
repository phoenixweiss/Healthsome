"""
Healthsome Flask App

Initializes Flask, sets up blueprints, and configures context processors.
"""

from flask import Flask, session, render_template
from flask_session import Session

from config import Config
from helpers.db_helpers import query_db
from helpers.datetime_helpers import to_iso_format
from modules.auth import bp as auth_bp
from modules.main import bp as main_bp
from modules.metrics.blood_pressure import bp as blood_pressure_bp
from modules.metrics.medications import bp as medications_bp
from modules.metrics.weight import bp as weight_bp

def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: Configured Flask application instance.
    """
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # Set up server-side session management
    Session(flask_app)

    # Register blueprints for modular routing and logic
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(blood_pressure_bp)
    flask_app.register_blueprint(weight_bp)
    flask_app.register_blueprint(medications_bp)

    # Add username to global template context
    @flask_app.context_processor
    def inject_user():
        """
        Add the currently logged-in user's username to the template context.

        Returns:
            dict: Dictionary containing the current user's username or None if not logged in.
        """
        user_id = session.get('user_id')
        if user_id:
            user = query_db(
                "SELECT username FROM users WHERE id = ?", (user_id,), one=True)
            if user:
                return {'current_user': user['username']}
        return {'current_user': None}

    # Register custom Jinja2 filters
    flask_app.jinja_env.filters['to_iso_format'] = to_iso_format

    # Register custom error handlers
    @flask_app.errorhandler(404)
    def page_not_found(error):
        """
        Custom handler for 404 errors (Page Not Found).

        Args:
            error (Exception): The exception object.

        Returns:
            Tuple: Rendered HTML template and HTTP status code.
        """
        return render_template('error.html', error_message="Page not found.", error_code=404), 404

    @flask_app.errorhandler(500)
    def internal_server_error(error):
        """
        Custom handler for 500 errors (Internal Server Error).

        Args:
            error (Exception): The exception object.

        Returns:
            Tuple: Rendered HTML template and HTTP status code.
        """
        return render_template('error.html', error_message="Internal server error.", error_code=500), 500

    return flask_app

if __name__ == "__main__":
    # Create the application instance
    app = create_app()

    # Run the Flask development server in debug mode
    app.run(debug=True)
