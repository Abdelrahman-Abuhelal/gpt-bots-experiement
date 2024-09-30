# app/__init__.py
from flask import Flask
from .config.db_config import DBConfig
from .extensions import db  # Import the db instance

db_config = DBConfig()


def create_app():
    app = Flask(__name__)
    app.secret_key = "sadfmasfmasflas"

    # Configure SQLAlchemy
    db_config.configure_sqlalchemy(app)
    db.init_app(app)

    # Configure MySQL instance
    global mysql_db
    mysql_db = db_config.configure_mysql()  # Store the MySQL DB instance

    # Debugging: Print mysql_db to verify it's not None
    print(f"MySQL DB instance: {mysql_db}")  # Check if mysql_db is initialized

    # Import and register blueprints for chatbot and CV extractor routes
    from .routes.chatbot_routes import main as chatbot_routes
    from .routes.cv_extractor_routes import main as cv_extractor_routes

    app.register_blueprint(chatbot_routes)
    app.register_blueprint(cv_extractor_routes)

    with app.app_context():
        db.create_all()

    return app
