from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets


# import flask login to check for an authenticated user and store current user
from flask_login import UserMixin, LoginManager

#import flask marshmallow to help create our Schemas
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager= LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    username = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self,email,first_name = '', last_name = '', id = '', password = '', username= '', token = '', date_created ='' ):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.username = username
        self.date_created = date_created
        self.email = email
        self.token = self.set_token(24)


    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(500))
    comics_appeared_in = db.Column(db.Integer)
    super_power = db.Column(db.String(120))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, description, comics_appeared_in, super_power,image, user_token):
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.user_token = user_token


    def __repr__(self):
        return f'The following Hero has been added: {self.name}'

    def set_id(self):
        return str(uuid.uuid4())


# Creation of API Schema via the Marshmallow Object
# Character schema
class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'comics_appeared_in', 'super_power','image' 'date_created')

# Initialize user and character schemas
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many=True)