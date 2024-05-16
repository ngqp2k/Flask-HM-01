from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required


import models as models


@app.route('/user')
@login_required
def user_page():
    users = models.User.query.all()
    return render_template('mdUser.html', users=users)


@app.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    
    if request.method == 'POST':
        user = models.User()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        sex = request.form['sex']
        print(sex)
        user.sex = models.Sex[sex]
        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
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
@login_required
def edit_user(user_id):
    user = models.User.query.get(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.sex = models.Sex[request.form['sex']]
        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
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
@login_required
def delete_user(user_id):
    user = models.User.query.get(user_id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('user_page'))