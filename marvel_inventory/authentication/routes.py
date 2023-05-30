from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_inventory.forms import UserLoginForm
from marvel_inventory.models import User, db, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            date_created = form.date_created.data
            email = form.email.data
            password = form.password.data
            print(email, username)

            user = User(first_name=first_name, last_name=last_name, date_created=date_created, email=email,
                        password=password, username=username)
            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {username}', 'user-created')

            # Check if the flash message is present
            print(flash('user-created'))

            return redirect(url_for('auth.signin'))
        except Exception as e:
            # Print the exception message for debugging
            print(f"Exception: {str(e)}")
            flash('An error occurred while creating the user account', 'error')

    return render_template('signup.html', form=form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()

    if request.method == 'POST' and not form.validate_on_submit():
        print(form.errors)
        try:
            email = form.email.data
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                print(f"This is the logged user: {logged_user}")
                login_user(logged_user)
                flash('You were successfully logged in: Via Email/Password', 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your Email/Password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
        except Exception as e:
            # Print the exception message for debugging
            print(f"Exception: {str(e)}")
            flash('An error occurred while signing in', 'error')

    return render_template('signin.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
