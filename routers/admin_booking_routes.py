from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required


import models as models


@app.route('/booking')
@login_required
def booking_page():
    bookings = models.Booking.query.all()
    return render_template('mdBooking.html', bookings=bookings)


@app.route('/add-booking', methods=['GET', 'POST'])
@login_required
def add_booking():
    booking = models.Booking()

    if request.method == 'POST':
        booking.first_name = request.form['first_name']
        booking.last_name = request.form['last_name']
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        booking.check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d')
        booking.check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d')
        booking.user = models.User.query.get(request.form['user'])
        booking.number_of_guests = 0
        booking.number_of_rooms = 0
        
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
                           , booking=booking
                           , sexs=sexs
                           , users=users
                           , rooms=rooms
                           , customers=customers
                           , statuses=statuses)


@app.route('/edit-booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def edit_booking(booking_id):
    booking = models.Booking.query.get(booking_id)
    
    if request.method == 'POST':
        booking.first_name = request.form['first_name']
        booking.last_name = request.form['last_name']
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        booking.check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d')
        booking.check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d')
        booking.user = models.User.query.get(request.form['user'])
        
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
@login_required
def delete_booking(booking_id):
    booking = models.Booking.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    
    return redirect(url_for('booking_page'))