from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from flask_login import LoginManager, login_user, logout_user, login_required



db = SQLAlchemy()

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # Create dummy secrey key so we can use sessions
    app.config['SECRET_KEY'] = '123456790'

    # Create in-memory database
    app.config['DATABASE_FILE'] = 'sample_db.sqlite'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
    app.config['SQLALCHEMY_ECHO'] = True
    
    # Initialize SQLAlchemy with this Flask app
    db.init_app(app)
    
    login_manager.init_app(app)
    
    return app


app = create_app()

from views import *


# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     first_name = request.form['first_name']  # pass the form field name as key
#     last_name = request.form['last_name']  # pass the form field name as key
#     return (f'User.first_name: {first_name} User.last_name: {last_name}')
    
def build_sample_db():
    pass
    # db.drop_all()
    # db.create_all()

    # # Create 2 roles
    # role1 = Role(name='Admin')
    # role2 = Role(name='User')
    # db.session.add(role1)
    # db.session.add(role2)
    
    # # Create 2 users
    # user1 = User(first_name='Phu', last_name='Nguyen', sex=Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' ,birthdate=datetime(2000, 3, 25), username='nqgp2k', password='123', role=role1)
    # user2 = User(first_name='Hazard', last_name='Eden', sex=Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' , birthdate=datetime(2000, 3, 25), username='eden', password='123', role=role2)
    # db.session.add(user1)
    # db.session.add(user2)

    # db.session.commit()


if __name__ == '__main__':
    # with app.app_context():
    #     build_sample_db()
    app.run(debug=True)