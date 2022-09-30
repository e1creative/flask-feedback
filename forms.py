"""Models for forms"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Optional, NumberRange, URL, AnyOf, Email


class UserForm(FlaskForm):
    """Form for registering/editing a user"""

    username = StringField('User Name', validators=[InputRequired(message="Username cannot be blank")])
    password = PasswordField('Password', validators=[InputRequired(message="Password cannot be blank")])
    email = EmailField('Email', validators=[InputRequired(message="Email cannot be blank"), Email(message="Please enter a proper email address")])
    first_name = StringField('First Name', validators=[InputRequired(message="First name is required")])
    last_name = StringField('Last Name', validators=[InputRequired(message="Last name is required")])

class LoginForm(FlaskForm):
    """Form for registering/editing a user"""

    username = StringField('User Name', validators=[InputRequired(message="Username cannot be blank")])
    password = PasswordField('Password', validators=[InputRequired(message="Password cannot be blank")])
    

class FeedbackForm(FlaskForm):
    """Form for adding/editing feedback"""

    title = StringField('Title', validators=[InputRequired(message="Title cannot be blank")])
    content = StringField('Content', validators=[InputRequired(message="Content cannot be blank")])

