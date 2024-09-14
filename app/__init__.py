from flask import Flask
from .config.db_config import DBConfig

db_config = DBConfig()

db = None

def create_app():
    app = Flask(__name__)
    app.secret_key = 'sadfmasfmasflas'

    global db
    db = db_config.get_sqlalchemy_config(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

mysql_db = db_config.get_mysql_db()
