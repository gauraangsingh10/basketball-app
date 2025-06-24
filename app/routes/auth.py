from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User
from ..extensions import db
from itsdangerous import URLSafeTimedSerializer
import os

auth_bp = Blueprint('auth', __name__)
serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash("Invalid credentials")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('dashboard.dashboard'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if user:
            token = user.get_reset_token(os.environ.get("SECRET_KEY"))
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash(f'Password reset link (simulate): {reset_url}', 'info')
        else:
            flash('No account found with that username.', 'danger')
    return render_template('forgot_password.html')

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token, os.environ.get("SECRET_KEY"))
    if not user:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html')

