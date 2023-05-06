from flask import Flask
from core.models import User
from sqlalchemy import text
from core.extensions import db, login_manager, csrf
from flask_cors import CORS
from flask_migrate import Migrate
from core.views.auth import auth_bp
from core.views.index import main_bp

def create_app(config): 
    app = Flask(__name__, template_folder='views/templates')
    app.config.from_object(config)

    # Initialize CORS, Flask-Login, CSRF protection, and SQLAlchemy
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)

    # Set the login view for Flask-Login
    login_manager.login_view = 'auth.login'

    # Define the user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        try:
            result = db.engine.execute(text("SELECT 1"))
            print("Database connection successful:", result.scalar() == 1)
        except Exception as e:
            print("Database connection failed:", e)
        
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    return app