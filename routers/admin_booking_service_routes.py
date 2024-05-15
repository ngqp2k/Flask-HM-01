from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


@app.route('/booking-service')
def booking_service_page():
    booking_services = models.BookingRoomService.query.all()
    return render_template('mdBookingService.html', booking_services=booking_services)

@app.route('/add-booking-service', methods=['GET', 'POST'])
def add_booking_service():
    booking_service = models.BookingRoomService()
    
    if request.method == 'POST':
        booking_service.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        booking_service.service = models.Service.query.get(request.form['service'])
        booking_service.qty = request.form['qty']
        
        db.session.add(booking_service)
        db.session.commit()
        
        return redirect(url_for('booking_service_page'))
    
    booking_rooms = models.BookingRoom.query.all()
    services = models.Service.query.all()
    
    return render_template('edit-booking-service.html'
                           , booking_service=booking_service
                           , booking_rooms=booking_rooms
                           , services=services)

@app.route('/edit-booking-service/<int:booking_service_id>', methods=['GET', 'POST'])
def edit_booking_service(booking_service_id):
    booking_service = models.BookingRoomService.query.get(booking_service_id)
    
    if request.method == 'POST':
        booking_service.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        booking_service.service = models.Service.query.get(request.form['service'])
        booking_service.qty = request.form['qty']
        
        db.session.commit()
        
        return redirect(url_for('booking_service_page'))
    
    booking_rooms = models.BookingRoom.query.all()
    services = models.Service.query.all()
    
    return render_template('edit-booking-service.html'
                           , booking_service=booking_service
                           , booking_rooms=booking_rooms
                           , services=services)

@app.route('/delete-booking-service/<int:booking_service_id>', methods=['GET', 'POST'])
def delete_booking_service(booking_service_id):
    booking_service = models.BookingRoomService.query.get(booking_service_id)
    db.session.delete(booking_service)
    db.session.commit()
    
    return redirect(url_for('booking_service_page'))