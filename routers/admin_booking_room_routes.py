from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required


import models as models


@app.route('/booking-room')
@login_required
def booking_room_page():
    booking_rooms = models.BookingRoom.query.all()
    return render_template('mdBookingRoom.html', booking_rooms=booking_rooms)

@app.route('/add-booking-room', methods=['GET', 'POST'])
@login_required
def add_booking_room():
    booking_room = models.BookingRoom()

    if request.method == 'POST':
        booking_room.booking = models.Booking.query.get(request.form['booking'])
        booking_room.room = models.Room.query.get(request.form['room'])
        booking_room.check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d')
        booking_room.check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d')
        booking_room.status = models.BookingStatus[request.form['status']]
        
        db.session.add(booking_room)
        db.session.commit()
        
        return redirect(url_for('booking_room_page'))
    
    bookings = models.Booking.query.all()
    rooms = models.Room.query.all()
    today = datetime.now().strftime('%Y-%m-%d')
    statuses = [status.name for status in models.BookingStatus]
    
    return render_template('add-booking-room.html'
                           , bookings=bookings
                           , rooms=rooms
                           , current_time=today
                           , booking_room=booking_room
                           , statuses=statuses)

@app.route('/edit-booking-room/<int:booking_room_id>', methods=['GET', 'POST'])
@login_required
def edit_booking_room(booking_room_id):
    booking_room = models.BookingRoom.query.get(booking_room_id)
    
    if request.method == 'POST':
        booking_room.booking = models.Booking.query.get(request.form['booking'])
        booking_room.room = models.Room.query.get(request.form['room'])
        booking_room.check_in_date = datetime.strptime(request.form['check_in_date'], '%Y-%m-%d')
        booking_room.check_out_date = datetime.strptime(request.form['check_out_date'], '%Y-%m-%d')
        booking_room.status = models.BookingStatus[request.form['status']]

        print(booking_room)
        
        db.session.commit()
        
        return redirect(url_for('booking_room_page'))
    
    bookings = models.Booking.query.all()
    rooms = models.Room.query.all()
    statuses = [status.name for status in models.BookingStatus]
    
    return render_template('edit-booking-room.html'
                           , booking_room=booking_room
                           , bookings=bookings
                           , rooms=rooms
                           , statuses=statuses)

@app.route('/delete-booking-room/<int:booking_room_id>', methods=['GET', 'POST'])
@login_required
def delete_booking_room(booking_room_id):
    booking_room = models.BookingRoom.query.get(booking_room_id)
    db.session.delete(booking_room)
    db.session.commit()
    
    return redirect(url_for('booking_room_page'))