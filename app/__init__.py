from flask import Flask
from .extensions import db
from flask_login import LoginManager
from .models import User
from .extensions import db, migrate

# Import blueprints here
from .routes import auth_bp, dashboard_bp, players_bp, teams_bp, games_bp, reports_bp
from app.routes.core import core_bp

import os

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basketball.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get("SECRET_KEY")

    db.init_app(app)
    migrate.init_app(app, db) 

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints here
    app.register_blueprint(core_bp) 
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(players_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(reports_bp)
   

    return app
