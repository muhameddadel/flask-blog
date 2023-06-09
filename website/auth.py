from flask import Blueprint, flash, render_template, redirect, url_for, request
from . import db
from .models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect!', category='danger')
        else:
            flash("Email dose not exists!", category='danger')
    
    return render_template('login.html', user=current_user)


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        if email_exists:
            flash("Email is alreay exists!", category='danger')
        elif username_exists:
            flash("Username is already exists!", category='danger')
        elif password1 != password2:
            flash("Password don't match", category='danger')
        elif len(username) < 2:
            flash('Username is too short!', category="danger")
        elif len(password1) < 6:
            flash("Password is too short!", category="danger")
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))