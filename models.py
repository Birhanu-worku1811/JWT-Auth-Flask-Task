from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User model that represents the 'users' table in the database.

    Attributes:
        id (str): Unique identifier for the user, generated as a UUID.
        username (str): The username of the user, must be unique.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
    """

    __tablename__ = 'users'

    # Define the columns of the 'users' table
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()), unique=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        """
        Returns a string representation of the User instance.

        This is useful for debugging purposes and represents the user by their username.
        """
        return f'<User {self.username}>'

    def set_password(self, password):
        """
        Hashes and sets the user's password.

        Args:
            password (str): The plain-text password to be hashed and set for the user.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Checks the given password against the stored hashed password.

        Args:
            password (str): The plain-text password to check.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username):
        """
        Retrieves a user from the database by their username.

        Args:
            username (str): The username to search for.

        Returns:
            User: The user instance if found, otherwise None.
        """
        return cls.query.filter_by(username=username).first()

    def save(self):
        """
        Saves the current user instance to the database.

        This method adds the user instance to the session and commits it to the database.
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes the current user instance from the database.

        This method removes the user instance from the session and commits the deletion.
        """
        db.session.delete(self)
        db.session.commit()
