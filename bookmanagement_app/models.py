from bookmanagement_app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index = True, unique = True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    user_password = db.Column(db.String(128))

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        '''Creates hashed password'''
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index= True, unique = True)
    author = db.Column(db.String(100), index = True)
    publisher = db.Column(db.String(100))
    year = db.Column(db.Integer)
    logged_by = db.Column(db.String(100))
    review = db.Column(db.String(300))

    def __repr__(self):
        return '<Book {}>'.format(self.title)

