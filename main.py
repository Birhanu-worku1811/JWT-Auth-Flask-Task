from flask import Flask, jsonify, render_template
from datetime import timedelta
from extensions import db, jwt
from models import User
from auth import register_user, login_user, profile, refresh_access, verify_token
from users import user_bp


def create_app():
    """
    Factory function to create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)

    # Load configuration from environment variables with a common prefix
    app.config.from_prefixed_env()

    # Set JWT token expiration times
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(weeks=1)

    # Initialize database and JWT manager with the app
    db.init_app(app)
    jwt.init_app(app)

    # Register authentication routes directly with their respective endpoints
    app.add_url_rule('/register', view_func=register_user, methods=['POST'])
    app.add_url_rule('/login', view_func=login_user, methods=['POST'])
    app.add_url_rule('/profile', view_func=profile, methods=['GET'])
    app.add_url_rule('/refresh', view_func=refresh_access, methods=['GET'])
    app.add_url_rule('/verify', view_func=verify_token, methods=['GET'])  # New verify endpoint

    # Register the user-related blueprint with a URL prefix
    app.register_blueprint(user_bp, url_prefix='/users')

    # Serve the index.html UI as the home page
    @app.route('/')
    def index():
        """
        Renders the main UI page.

        Returns:
            str: The rendered HTML of the index page.
        """
        return render_template('index.html')

    # Load user from the JWT token
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """
        Callback function to load a user from the JWT token.

        Args:
            _jwt_header (dict): The JWT header (unused).
            jwt_data (dict): The decoded JWT data containing the user identity.

        Returns:
            User: The user object associated with the JWT identity, or None if not found.
        """
        identity = jwt_data['sub']
        return User.query.get(identity)

    return app
