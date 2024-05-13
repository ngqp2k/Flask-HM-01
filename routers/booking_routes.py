from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime, timedelta

import random
import models as models


@app.route('/checkout/<int:room_id>', methods=['GET', 'POST'])
def checkout_page(room_id):
    room = models.Room.query.get(room_id)
    print(f'Room ID: {room_id} {room} {request.method}')
    if request.method == 'GET':
        
        checkin_date = datetime.now().strftime('%d/%m/%Y')
        checkout_date = (datetime.now() + timedelta(days=2)).strftime('%d/%m/%Y')
        
        payment_methods = models.PaymentMethod.query.all()
        return render_template('checkout.html'
                               , room=room
                               , payment_methods=payment_methods
                               , checkin_date=checkin_date
                               , checkout_date=checkout_date)
        
    return redirect(url_for('index'))


@app.route('/checkout-handler/<int:room_id>', methods=['GET', 'POST'])
def checkout_handler(room_id):
    if request.method == 'POST':
        # create booking
        booking = models.Booking()
        booking.customer_first_name = request.form['customer_first_name']
        booking.customer_last_name = request.form['customer_last_name']
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.created_date = datetime.now()
        booking.checkin_date = datetime.now()
        booking.checkout_date = datetime.now() + timedelta(days=2)
        room = models.Room.query.get(room_id)
        room.status = models.RoomStatus['BOOKED']
        booking.room = room
        booking.status = models.BookingStatus['CONFIRMED']
        
        # create payment
        payment = models.Payment()
        payment.booking = booking
        payment.created_date = datetime.now()
        payment.amount = room.room_type.price_per_night * 2
        payment.transaction_id = random.randint(100000, 999999)
        
        db.session.add(booking)
        db.session.add(payment)
        
        db.session.commit()
        
    return redirect(url_for('index'))


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    

    return redirect(url_for('admin_page'))


@app.route('/api/test', methods=['POST'])
def testtest():
    print('testtest')


    return redirect(url_for('index'))
