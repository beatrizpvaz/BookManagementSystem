from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo

from ..models import User

class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('confirm_password')])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email is already in use.')
    
    def validate_username(self, field):
        if User.query.filter_by(username = field.data).first():
            raise ValidationError('Username is already in use.')

class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')