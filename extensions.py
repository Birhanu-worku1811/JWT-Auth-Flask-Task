from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize the SQLAlchemy instance for database management
db = SQLAlchemy()

# Initialize the JWTManager instance for handling JWT-based authentication
jwt = JWTManager()
