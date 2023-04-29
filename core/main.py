from flask import Flask, request, jsonify, current_app
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from .models import User
from .auth import auth_bp

def create_app(config): 
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Flask-Login and CSRF protection
    login_manager = LoginManager(app)
    csrf = CSRFProtect(app)

    # Set the login view for Flask-Login
    login_manager.login_view = 'login'

    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    app.register_blueprint(auth_bp)

    return app
