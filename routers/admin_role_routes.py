from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required


import models as models


@app.route('/role')
@login_required
def role_page():
    roles = models.Role.query.all()
    return render_template('mdRole.html', roles=roles)


@app.route('/add-role', methods=['GET', 'POST'])
@login_required
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
@login_required
def edit_role(role_id):
    role = models.Role.query.get(role_id)
    
    if request.method == 'POST':
        role.name = request.form['name']
        
        db.session.commit()
        
        return redirect(url_for('role_page'))
    
    return render_template('edit-role.html', role=role)


@app.route('/delete-role/<int:role_id>', methods=['GET', 'POST'])
@login_required
def delete_role(role_id):
    role = models.Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    
    return redirect(url_for('role_page'))