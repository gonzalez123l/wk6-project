from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired,Email

class UserLoginForm(FlaskForm):
    # email, password, submit_button
    first_name = StringField('first_name', validators = [DataRequired()])
    last_name = StringField('last_name', validators = [DataRequired()])
    username = StringField('username', validators= [DataRequired()])
    date_created = DateField('date_created (YYYY-MM-DD)', validators = [DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit_button = SubmitField()

class MarvelCharacterInfo(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    comics_appeared_in = IntegerField('Comics Appeared In', validators=[DataRequired()])
    super_power = StringField('Super Power', validators=[DataRequired()])
    submit_button = SubmitField('Submit')