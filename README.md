# JWT Authentication With Flask

## Introduction

This project is a Flask-based web application that implements JWT (JSON Web Token) authentication. It allows users to register, log in, and access protected endpoints. The application includes token expiration and refresh mechanisms, and it provides an easy-to-use UI for testing the API.

## Features

- **User Registration**: Users can register with a username, email, and password.
- **User Login**: Users can log in and receive JWT access and refresh tokens.
- **Token Management**: JWT tokens are used for authentication, with access tokens expiring after 10 minutes and refresh tokens expiring after one week.
- **Protected Endpoints**: Endpoints require valid JWT tokens for access.
- **Token Verification**: An endpoint to verify the validity of a JWT token.
- **UI for Testing**: A web-based UI is provided for testing each API endpoint.

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/flask-jwt-authentication.git
   cd flask-jwt-authentication
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
    ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. create .env file and add the following:
   ```bash
   FLASK_SECRET_KEY=your_secret_key
   FLASK_DEBUG=True
   FLASK_SQLALCHEMY_DATABASE_URI=sqlite:///db.sqlite3
   FLASK_SQLALCHEMY_ECHO=True
   FLASK_JWT_SECRET_KEY=04749e6e732bb7a09aa11428
   ```
5. Export the flask app:
   ```bash
    export FLASK_APP=main.py
   ```
6. **Migrate the database**:
    You can create the database and tables using the Flask shell. Run the following command:
    ```bash
    flask shell
    ```
    Inside the Flask shell, execute:
    ```python
    from models import User
    db.create_all()
    ```
    Alternatively, if you are using Flask-Migrate, you can run:
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```
7. **Run the application**:
    ```bash
    flask run
    ```
8. **Access the application**:
    The application will be available at `http://127.0.0.1:5000/`.

### API Documentation

#### Register User:
* Endpoint: `/register`
* Method: `POST`
* Description: Register a new user.
* Request Body:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
* Response:
  ```json
  {
    "message": "User registered"
  }
  ```

#### Login User:
* Endpoint: `/login`
* Method: `POST`
* Description:Login user.
* Request Body:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
* Response:
  ```json
  {
            "message": "logged in",
            "tokens": {
                "access_token": "access_token",
                "refresh_token": "refresh_token"
            }
        }
  ```
  

#### Profile:
* Endpoint: `/profile`
* Method: `GET`
* Description: get user details.
* Authorization Header: Bearer token required.
* Response:
  ```json
  {
        "message": "You are authenticated",
        "user_details": {
            "username": "authenticated username",
            "email": "authenticated user email"
        }
    }
  ```
  

#### Refresh:
* Endpoint: `/refresh`
* Method: `GET`
* Description: refresh access token.
* Authorization Header: Bearer token required.
* Response:
  ```json
  {
  "access_token": "new_access_token"
  }
  ```
# UI
The project includes a simple web-based UI for testing the API endpoints. To access the UI, simply navigate to the root URL (http://127.0.0.1:5000/) after starting the Flask server.