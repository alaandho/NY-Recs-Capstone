from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from capstone_inventory.forms import UserLoginForm
from capstone_inventory.models import db, User, check_password_hash


auth = Blueprint('auth',__name__, template_folder='auth_templates')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        print(email, password)
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()
        flash(f'You have successfully created a user account {name}.', 'user-created')
        return redirect(url_for('auth.signin'))

    return render_template('signup.html', form = form)


@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(email, password)
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            flash('Welcome! Login Successful!', 'auth-success')
            return redirect(url_for('site.home'))
        else:
            flash('Incorrect Email/Password. Please try again.', 'auth-failed')
            return redirect(url_for('auth.signin'))

    return render_template('signin.html', form = form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'You are now logged out', 'auth-success')
    return redirect(url_for('site.home'))


def login_required(current_user):
    def logout():
        logout_user()
        return redirect(url_for('site.home'))
    if current_user.is_authenticated:
        return logout()

