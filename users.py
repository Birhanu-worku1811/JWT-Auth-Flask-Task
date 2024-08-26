from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import User
from schemas import UserSchema

# Create a Blueprint for user-related routes
user_bp = Blueprint("users", __name__)

@user_bp.get('/all')
@jwt_required()
def get_all_users():
    """
    Retrieve a paginated list of all users.

    This endpoint is restricted to users with 'is_staff' claim set to True.
    The users are retrieved in a paginated format, allowing control over
    how many users are displayed per page.

    Query Parameters:
        page (int): The page number to retrieve (default is 1).
        per_page (int): The number of users per page (default is 3).

    Returns:
        JSON response containing a list of users if the request is authorized.
        Otherwise, a 403 error indicating the user is not authorized.
    """
    claims = get_jwt()  # Retrieve claims from the JWT token

    # Check if the user has staff privileges
    if claims.get('is_staff') is True:
        # Get pagination parameters from the request
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=3, type=int)

        # Query the database for users with pagination
        users = User.query.paginate(page=page, per_page=per_page)

        # Serialize the user data to JSON format
        result = UserSchema().dump(users, many=True)

        return jsonify({
            "users": result,
        }), 200

    # Return an error if the user is not authorized
    return jsonify({
        "error": "You are not authorized to access this resource"
    }), 403
