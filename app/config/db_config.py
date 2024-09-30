# config/db_config.py
from langchain_community.utilities.sql_database import SQLDatabase


class DBConfig:
    def configure_sqlalchemy(self, app):
        """
        Configure SQLAlchemy for the Flask app.
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    def configure_mysql(self):
        """
        Configure MySQL connection using SQLDatabase.
        """
        db_user = "root"
        db_password = "ROOT1234"
        db_host = "localhost:3306"
        db_name = "training_management"

        # Create a MySQL database connection instance
        return SQLDatabase.from_uri(
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
        )
