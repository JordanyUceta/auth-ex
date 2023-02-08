from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length

class RegisterForm(FlaskForm): 
    """register form"""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])

class LoginForm(FlaskForm): 
    """login form"""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class DeleteForm(FlaskForm): 
    """this form is intentionally blank"""

class FeedbackForm(FlaskForm): 
    """feedback form"""
    title = StringField('Title', validators=[InputRequired(), Length(max=150)])
    content = StringField('Content', validators=[InputRequired()])
