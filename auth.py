from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    current_user,
    get_jwt_identity,
    verify_jwt_in_request
)
from models import User

# Register User
def register_user():
    """
    Endpoint to register a new user.

    This function handles the registration of a new user. It checks if a user
    with the given username already exists. If not, it creates a new user,
    hashes their password, saves the user to the database, and returns a success message.

    Returns:
        Response: JSON response indicating success or failure.
    """
    data = request.get_json()

    user = User.get_user_by_username(data['username'])

    if user is not None:
        return jsonify({
            "message": "User already exists"
        }), 403

    # Create a new user instance
    new_user = User(
        username=data['username'],
        email=data['email'],
    )

    # Set the password for the new user
    new_user.set_password(password=data.get('password'))

    # Save the new user to the database
    new_user.save()

    return jsonify({
        "message": "User registered"
    }), 201

# Login User
def login_user():
    """
    Endpoint to authenticate a user and issue JWT tokens.

    This function authenticates a user by checking their username and password.
    If the credentials are correct, it generates and returns a JWT access token
    and a refresh token.

    Returns:
        Response: JSON response containing JWT tokens or an error message.
    """
    data = request.get_json()

    # Retrieve the user by username
    user = User.get_user_by_username(username=data.get('username'))

    # Check if the user exists and if the password is correct
    if user and user.check_password(password=data.get('password')):

        # Create access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            "message": "logged in",
            "tokens": {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }), 200

    return jsonify({
        "error": "Invalid credentials"
    }), 400

# Who Am I
@jwt_required()
def profile():
    """
    Endpoint to retrieve the authenticated user's details.

    This function requires a valid JWT token and returns the username and
    email of the currently authenticated user.

    Returns:
        Response: JSON response containing user details or an error message.
    """
    return jsonify({
        "message": "You are authenticated",
        "user_details": {
            "username": current_user.username,
            "email": current_user.email,
        }
    }), 200

# Refresh Access Token
@jwt_required(refresh=True)
def refresh_access():
    """
    Endpoint to refresh the access token using a valid refresh token.

    This function requires a valid refresh token and generates a new access token
    for the user.

    Returns:
        Response: JSON response containing the new access token.
    """
    identity = get_jwt_identity()

    # Generate a new access token
    new_access_token = create_access_token(identity=identity)

    return jsonify({
        "access_token": new_access_token
    })

# Verify Token
def verify_token():
    """
    Endpoint to verify the validity of the JWT token.

    This function checks if the provided JWT token is valid. If the token is valid,
    it returns a success message. Otherwise, it returns an error message.

    Returns:
        Response: JSON response indicating whether the token is valid or not.
    """
    try:
        verify_jwt_in_request()
        return jsonify({
            "message": "Token is valid"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Token is invalid or expired",
            "details": str(e)
        }), 401
