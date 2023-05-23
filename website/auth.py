from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return 'login'

@auth.route('/sign-up')
def sign_up():
    return 'Sign Up'

@auth.route('/logout')
def logout():
    return 'logout'