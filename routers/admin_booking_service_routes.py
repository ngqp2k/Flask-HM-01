from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


@app.route('/booking-service')
def booking_service_page():
    booking_services = models.BookingServices.query.all()
    return render_template('mdBookingService.html', booking_services=booking_services)

@app.route('/add-booking-service', methods=['GET', 'POST'])
def add_booking_service():
    if request.method == 'POST':
        booking_service = models.BookingServices()
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

@app.route('/edit-booking-service/<int:booking_service_id>', methods=['GET', 'POST'])
def edit_booking_service(booking_service_id):
    booking_service = models.BookingServices.query.get(booking_service_id)
    
    if request.method == 'POST':
        booking_service.booking = models.Booking.query.get(request.form['booking'])
        booking_service.service = models.Service.query.get(request.form['service'])
        booking_service.qty = request.form['qty']
        
        db.session.commit()
        
        return redirect(url_for('booking_service_page'))
    
    bookings = models.Booking.query.all()
    services = models.Service.query.all()
    
    return render_template('edit-booking-service.html', booking_service=booking_service, bookings=bookings, services=services)

@app.route('/delete-booking-service/<int:booking_service_id>', methods=['GET', 'POST'])
def delete_booking_service(booking_service_id):
    booking_service = models.BookingServices.query.get(booking_service_id)
    db.session.delete(booking_service)
    db.session.commit()
    
    return redirect(url_for('booking_service_page'))