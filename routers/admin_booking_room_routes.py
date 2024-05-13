from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


@app.route('/booking-room')
def booking_room_page():
    booking_rooms = models.BookingRoom.query.all()
    return render_template('mdBookingRoom.html', booking_rooms=booking_rooms)

@app.route('/add-booking-room', methods=['GET', 'POST'])
def add_booking_room():
    if request.method == 'POST':
        booking_service = models.BookingRoomService()
        booking_service.booking = models.Booking.query.get(request.form['booking'])
        booking_service.service = models.Service.query.get(request.form['service'])
        booking_service.qty = request.form['qty']
        
        db.session.add(booking_service)
        db.session.commit()
        
        return redirect(url_for('booking_service_page'))
    
    bookings = models.Booking.query.filter_by(status=models.BookingStatus.CHECKED_IN).all()
    services = models.Service.query.all()
    today = datetime.now().strftime('%d-%m-%Y')
    
    return render_template('add-booking-service.html', bookings=bookings, services=services, current_time=today)

@app.route('/edit-booking-room/<int:booking_room_id>', methods=['GET', 'POST'])
def edit_booking_room(booking_room_id):
    booking_service = models.BookingRoomService.query.get(booking_room_id)
    
    if request.method == 'POST':
        booking_service.booking = models.Booking.query.get(request.form['booking'])
        booking_service.service = models.Service.query.get(request.form['service'])
        booking_service.qty = request.form['qty']
        
        db.session.commit()
        
        return redirect(url_for('booking_service_page'))
    
    bookings = models.Booking.query.all()
    services = models.Service.query.all()
    
    return render_template('edit-booking-room.html'
                           , booking_service=booking_service
                           , bookings=bookings
                           , services=services)

@app.route('/delete-booking-room/<int:booking_room_id>', methods=['GET', 'POST'])
def delete_booking_room(booking_room_id):
    booking_room = models.BookingRoom.query.get(booking_room_id)
    db.session.delete(booking_room)
    db.session.commit()
    
    return redirect(url_for('booking_room_page'))