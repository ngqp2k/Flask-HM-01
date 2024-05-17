from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Create dummy secrey key so we can use sessions
    app.config['SECRET_KEY'] = '123456790'

    # Create in-memory database
    app.config['DATABASE_FILE'] = 'hotel_management_db.sqlite'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/hotel_management_db'
    # app.config['SQLALCHEMY_ECHO'] = True
    
    # Initialize SQLAlchemy with this Flask app
    db.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.init_app(app)
    
    return app


app = create_app()

from routers import *


if __name__ == '__main__':
    # with app.app_context():
    #     import utils
    #     utils.build_sample_db()
    app.run(debug=True)