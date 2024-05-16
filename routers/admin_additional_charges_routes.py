from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required


import models as models


@app.route('/additional-charge')
@login_required
def additional_charge_page():
    additional_charges = models.AdditionalCharge.query.all()
    return render_template('mdAdditionalCharge.html', additional_charges=additional_charges)

@app.route('/add-additional-charge', methods=['GET', 'POST'])
@login_required
def add_additional_charge():
    additional_charge = models.AdditionalCharge()
    
    if request.method == 'POST':
        additional_charge.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.add(additional_charge)
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    booking_rooms = models.BookingRoom.query.all()
    
    return render_template('add-additional-charge.html'
                           , additional_charge=additional_charge
                           , booking_rooms=booking_rooms)

@app.route('/edit-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
@login_required
def edit_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    
    if request.method == 'POST':
        additional_charge.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    booking_rooms = models.BookingRoom.query.all()
    
    return render_template('edit-additional-charge.html'
                           , additional_charge=additional_charge
                           , booking_rooms=booking_rooms)

@app.route('/delete-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
@login_required
def delete_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    db.session.delete(additional_charge)
    db.session.commit()
    
    return redirect(url_for('additional_charge_page'))