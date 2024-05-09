from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


@app.route('/additional-charge')
def additional_charge_page():
    additional_charges = models.AdditionalCharge.query.all()
    return render_template('mdAdditionalCharge.html', additional_charges=additional_charges)

@app.route('/add-additional-charge', methods=['GET', 'POST'])
def add_additional_charge():
    if request.method == 'POST':
        additional_charge = models.AdditionalCharge()
        additional_charge.booking = models.Booking.query.get(request.form['booking'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.add(additional_charge)
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    bookings = models.Booking.query.filter_by(status=models.BookingStatus.CHECKED_IN).all()
    today = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add-additional-charge.html', bookings=bookings, current_time=today)

@app.route('/edit-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
def edit_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    
    if request.method == 'POST':
        additional_charge.booking = models.Booking.query.get(request.form['booking'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('edit-additional-charge.html', additional_charge=additional_charge, bookings=bookings)

@app.route('/delete-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
def delete_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    db.session.delete(additional_charge)
    db.session.commit()
    
    return redirect(url_for('additional_charge_page'))