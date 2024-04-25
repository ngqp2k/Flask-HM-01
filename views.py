import enum
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
# from models import User, Role, Sex
from flask_wtf import FlaskForm
from wtforms import StringField
from datetime import datetime
from werkzeug.security import check_password_hash


import models as models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user = models.User.query.filter_by(username=request.form['username']).first()
        
        print(user is None)
        
        if not user is None:
            print(user.hash_password)
            print(request.form['password'])
            print(user is None)
            print(check_password_hash(user.hash_password, request.form['password']))
    
        if (user is None) or (not check_password_hash(user.hash_password, request.form['password'])):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('admin_page'))
        
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in_page():
    return render_template('signin.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('sign_in_page'))


@app.route('/')
def index():
    return render_template('index_home_page.html')


@app.route('/admin')
@login_required
def admin_page():
    return render_template('index.html')

@app.template_filter()
def to_string(obj):
    if isinstance(obj, enum.Enum):
        return obj.name

    return obj


@app.route('/user')
def user_page():
    users = models.User.query.all()
    return render_template('mdUser.html', users=users)


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    
    if request.method == 'POST':
        user = models.User()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        sex = request.form['sex']
        print(sex)
        user.sex = models.Sex[sex]
        user.birthdate = datetime(2012, 3, 3)
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.username = request.form['username']
        user.password = request.form['password']
        user.rold_id = request.form['role']
        
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        
        return redirect(url_for('user_page'))
    
    return render_template('add-user.html')
    
    
@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = models.User.query.get(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.sex = models.Sex[request.form['sex']]
        user.birthdate = datetime(2012, 3, 3)
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.username = request.form['username']
        user.password = request.form['password']
        
        role = models.Role.query.get(request.form['role'])
        user.role = role
        
        db.session.commit()
        
        return redirect(url_for('user_page'))
    
    sexs = [sex.name for sex in models.Sex]
    roles = models.Role.query.all()
    
    return render_template('edit-user.html'
                           , user=user, sexs=sexs
                           , roles=roles)


@app.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = models.User.query.get(user_id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('user_page'))


@app.route('/role')
def role_page():
    roles = models.Role.query.all()
    return render_template('mdRole.html', roles=roles)


@app.route('/add-role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        role = models.Role()
        role.name = request.form['name']
        
        with app.app_context():
            db.session.add(role)
            db.session.commit()
        
        return redirect(url_for('role_page'))
    
    return render_template('add-role.html')

@app.route('/edit-role/<int:role_id>', methods=['GET', 'POST'])
def edit_role(role_id):
    role = models.Role.query.get(role_id)
    
    if request.method == 'POST':
        role.name = request.form['name']
        
        db.session.commit()
        
        return redirect(url_for('role_page'))
    
    return render_template('edit-role.html', role=role)


@app.route('/delete-role/<int:role_id>', methods=['GET', 'POST'])
def delete_role(role_id):
    role = models.Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    
    return redirect(url_for('role_page'))