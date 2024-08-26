from marshmallow import fields, Schema

class UserSchema(Schema):
    """
    Schema for serializing and deserializing User objects.

    This schema is used to define how User objects are converted to and from JSON.
    It ensures that only the specified fields are included in the output.

    Fields:
        id (str): The unique identifier of the user.
        username (str): The username of the user.
        email (str): The email address of the user.
    """

    id = fields.String()
    username = fields.String()
    email = fields.String()
