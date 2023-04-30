from flask import Flask, request, jsonify, current_app
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from .models.models import User
from .auth import auth_bp

db = SQLAlchemy()

def create_app(config): 
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Flask-Login, CSRF protection, and SQLAlchemy
    login_manager = LoginManager(app)
    csrf = CSRFProtect(app)
    db.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = 'auth.login'

    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    app.register_blueprint(auth_bp)

    return app

