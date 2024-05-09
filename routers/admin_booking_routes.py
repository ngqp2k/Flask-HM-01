from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


@app.route('/booking')
def booking_page():
    bookings = models.Booking.query.all()
    return render_template('mdBooking.html', bookings=bookings)


@app.route('/add-booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        booking = models.Booking()
        booking.customer_first_name = request.form['customer_first_name']
        booking.customer_last_name = request.form['customer_last_name']
        booking.age = request.form['age']
        booking.sex = models.Sex[request.form['sex']]
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.is_regioner = request.form['is_regioner']
        booking.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        booking.checkin_date = datetime.strptime(request.form['checkin_date'], '%Y-%m-%d')
        booking.checkout_date = datetime.strptime(request.form['checkout_date'], '%Y-%m-%d')
        booking.user = models.User.query.get(request.form['user'])
        booking.room = models.Room.query.get(request.form['room'])
        booking.customer = models.Customer.query.get(request.form['customer'])
        booking.status = models.BookingStatus[request.form['status']]
        
        db.session.add(booking)
        db.session.commit()
        
        # Redirect to the booking page
        return redirect(url_for('booking_page'))
    
    sexs = [sex.name for sex in models.Sex]
    users = models.User.query.all()
    rooms = models.Room.query.all()
    customers = models.Customer.query.all()
    statuses = [status.name for status in models.BookingStatus]
    
    return render_template('add-booking.html'
                           , sexs=sexs
                           , users=users
                           , rooms=rooms
                           , customers=customers
                           , statuses=statuses)


@app.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
def edit_booking(booking_id):
    booking = models.Booking.query.get(booking_id)
    
    if request.method == 'POST':
        booking.customer_first_name = request.form['customer_first_name']
        booking.customer_last_name = request.form['customer_last_name']
        booking.age = request.form['age']
        booking.sex = models.Sex[request.form['sex']]
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.is_regioner = request.form.get('is_regioner', False)
        booking.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        booking.checkin_date = datetime.strptime(request.form['checkin_date'], '%Y-%m-%d')
        booking.checkout_date = datetime.strptime(request.form['checkout_date'], '%Y-%m-%d')
        booking.user = models.User.query.get(request.form['user'])
        booking.room = models.Room.query.get(request.form['room'])
        booking.customer = models.Customer.query.get(request.form['customer'])
        status = request.form['status']
        booking.status = models.BookingStatus[status]
        
        db.session.add(booking)
        db.session.commit()
        
        return redirect(url_for('booking_page'))
    
    rooms = models.Room.query.all()
    sexs = [sex.name for sex in models.Sex]
    users = models.User.query.all()
    customers = models.Customer.query.all()
    statuses = [status.name for status in models.BookingStatus]
    
    return render_template('edit-booking.html'
                           , booking=booking
                           , rooms=rooms
                           , sexs=sexs
                           , users=users
                           , customers=customers
                           , statuses=statuses)


@app.route('/delete-booking/<int:booking_id>', methods=['GET', 'POST'])
def delete_booking(booking_id):
    booking = models.Booking.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    
    return redirect(url_for('booking_page'))