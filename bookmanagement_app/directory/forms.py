from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import InputRequired, Email, EqualTo

from ..models import Book

class BookForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    author = StringField('Author', validators=[InputRequired()])
    publisher = StringField('Publisher', validators=[InputRequired()])
    year = StringField('Year', validators=[InputRequired()])
    logged_by = StringField('Logger')
    review = StringField('Review')
    submit = SubmitField('Submit')

class AddReview(FlaskForm):
    review = StringField('Review') 
    submit = SubmitField('Submit')
