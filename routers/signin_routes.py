from flask_login import login_user, logout_user
from app import app, login_manager
from werkzeug.security import check_password_hash
from flask import render_template, request, redirect, url_for, flash


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
            return redirect(url_for('index'))
        
    return render_template('signin.html')


@app.route('/signin', methods=['GET', 'POST'])
def sign_in_page():
    return render_template('signin.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))