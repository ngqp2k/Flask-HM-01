from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models



@app.route('/payment')
def payment_page():
    payments = models.Payment.query.all()
    return render_template('mdPayment.html', payments=payments)


@app.route('/add-payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        payment = models.Payment()
        payment.booking = models.Booking.query.get(request.form['booking'])
        payment.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        payment.amount = request.form['amount']
        payment.payment_method = models.PaymentMethod.query.filter_by(name='Cash').first()
        
        db.session.add(payment)
        db.session.commit()
        
        return redirect(url_for('payment_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('add-payment.html', bookings=bookings)


@app.route('/edit-payment/<int:payment_id>', methods=['GET', 'POST'])
def edit_payment(payment_id):
    payment = models.Payment.query.get(payment_id)
    
    if request.method == 'POST':
        payment.booking = models.Booking.query.get(request.form['booking'])
        payment.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        payment.amount = request.form['amount']
        payment.transaction_id = request.form['transaction_id']
        payment.payment_method = models.PaymentMethod.query.get(request.form['payment_method'])
        
        db.session.add(payment)
        db.session.commit()
        
        db.session.commit()
        
        return redirect(url_for('payment_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('edit-payment.html', payment=payment, bookings=bookings)


@app.route('/delete-payment/<int:payment_id>', methods=['GET', 'POST'])
def delete_payment(payment_id):
    payment = models.Payment.query.get(payment_id)
    db.session.delete(payment)
    db.session.commit()
    
    return redirect(url_for('payment_page'))