from flask import Blueprint, render_template, redirect, request,url_for, flash
from flask_login import login_required, current_user
from marvel_inventory.forms import MarvelCharacterInfo
from marvel_inventory.models import Character, db



"""
    Note that in the below code,
    some arguments are specified when creating Blueprint objects.
    The first argument, 'site' is the Blueprint's name,
    which flask uses for routing.
    The second argument, __name__,  is the Blueprint's import name, 
    which flask uses to locate the Blueprint's resources
"""

site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    marvel_character = MarvelCharacterInfo()

    try:
        if request.method == "POST" and marvel_character.validate_on_submit():
            name = marvel_character.name.data
            description = marvel_character.description.data
            comics_appeared_in = marvel_character.comics_appeared_in.data
            super_power = marvel_character.super_power.data
            user_token = current_user.token

            character = Character(name, description, comics_appeared_in, super_power, user_token)

            db.session.add(character)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception("An error occurred while creating Character try again!")

    current_user_token = current_user.token

    characters = Character.query.filter_by(user_token=current_user_token).all()

    return render_template('profile.html', form=marvel_character, characters=characters)