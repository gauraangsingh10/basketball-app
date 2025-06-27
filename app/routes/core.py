from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from flask_login import current_user
from app.models import Team, db
from flask import redirect, url_for, flash

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('index.html')




@core_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@core_bp.route('/healthcheck')
def healthcheck():
    return "OK", 200


