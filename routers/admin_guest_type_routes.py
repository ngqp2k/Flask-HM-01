from app import app, db
from flask import render_template, request, redirect, url_for


import models as models


@app.route('/guest-type')
def guest_type_page():
    guest_types = models.GuestType.query.all()
    return render_template('mdGuestType.html'
                           , guest_types=guest_types)


@app.route('/add-guest-type', methods=['GET', 'POST'])
def add_guest_type():
    guest_type = models.GuestType()
    
    if request.method == 'POST':
        guest_type.name = request.form['name']
        guest_type.description = request.form['description']
        
        db.session.add(guest_type)
        db.session.commit()
        
        return redirect(url_for('guest_type_page'))
    
    return render_template('edit-guest-type.html'
                           , guest_type=guest_type)
    
@app.route('/edit-guest-type/<int:guest_type_id>', methods=['GET', 'POST'])
def edit_guest_type(guest_type_id):
    guest_type = models.GuestType.query.get(guest_type_id)
    
    if request.method == 'POST':
        guest_type.name = request.form['name']
        guest_type.description = request.form['description']
        
        db.session.commit()
        
        return redirect(url_for('guest_type_page'))
    
    return render_template('edit-guest-type.html'
                           , guest_type=guest_type)
    
@app.route('/delete-guest-type/<int:guest_type_id>', methods=['GET', 'POST'])
def delete_guest_type(guest_type_id):
    guest_type = models.GuestType.query.get(guest_type_id)
    db.session.delete(guest_type)
    db.session.commit()
    
    return redirect(url_for('guest_type_page'))