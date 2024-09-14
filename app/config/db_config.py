# config/db_config.py
from flask_sqlalchemy import SQLAlchemy
from langchain_community.utilities.sql_database import SQLDatabase

class DBConfig:
    def get_sqlalchemy_config(self, app):
        """
        Configure and initialize SQLAlchemy for the Flask app.
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///chat.db"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sqlalchemy_db = SQLAlchemy(app)
        return sqlalchemy_db

    def get_mysql_db(self):
        """
        Configure and initialize MySQL connection using SQLDatabase.
        """
        db_user = "root"
        db_password = "ROOT1234"
        db_host = "localhost:3306"
        db_name = "training_management"

        # Create a MySQL database connection instance
        mysql_db = SQLDatabase.from_uri(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
        )
        # print(mysql_db.dialect)
        # print(mysql_db.get_usable_table_names())
        # print(mysql_db.table_info)
        return mysql_db
