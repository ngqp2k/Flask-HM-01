import decimal
from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime


import models as models


class InvoiceDetail():
    def __init__(self, no, description, unit_price, qty, amount):
        self.no = no
        self.description = description
        self.unit_price = unit_price
        self.qty = qty
        self.amount = amount

@app.route('/create-invoice/<int:booking_id>', methods=['GET', 'POST'])
def invoice_detail_page(booking_id):
    booking = models.Booking.query.get(booking_id)
    
    print(f'ngqp2k-debug: {request.method} {booking_id}')
        
    # get all payment of booking
    payment = models.Payment.query.filter_by(booking_id=booking_id).first()
    # get all additional charges of booking
    additional_charges = models.AdditionalCharge.query.filter_by(booking_id=booking_id).all()
    # get all services of booking
    booking_services = models.BookingServices.query.filter_by(booking_id=booking_id).all()
    
    # create invoice details
    row_count = 1
    total_amount = 0
    
    invoice_details = []
    
    cnt_date = (booking.checkout_date - booking.checkin_date).days
    invoice_detail = InvoiceDetail(row_count, 'Tiền phòng', booking.room.room_type.price_per_night, cnt_date, booking.room.room_type.price_per_night * cnt_date)
    total_amount += decimal.Decimal(invoice_detail.amount)
    invoice_details.append(invoice_detail)
        
    for additional_charge in additional_charges:
        row_count += 1
        invoice_detail = InvoiceDetail(row_count, additional_charge.description, additional_charge.amount, 1, additional_charge.amount)
        total_amount += invoice_detail.amount
        invoice_details.append(invoice_detail)
        
    for booking_service in booking_services:
        row_count += 1
        invoice_detail = InvoiceDetail(row_count, booking_service.service.name, booking_service.service.price, booking_service.qty, booking_service.service.price * booking_service.qty)
        total_amount += decimal.Decimal(invoice_detail.amount)
        invoice_details.append(invoice_detail)
        
    if payment is None:
        reminder = total_amount
    else:
        reminder = total_amount - payment.amount
        
    is_read_only = booking.status == models.BookingStatus.CHECKED_OUT
        
    if request.method == 'POST':
        invoice = models.Invoice()
        invoice.booking = booking
        invoice.created_date = datetime.now()
        invoice.total_price = total_amount
        
        db.session.add(invoice)
        
        booking.status = models.BookingStatus.CHECKED_OUT
        db.session.add(booking)
        
        room = booking.room
        room.status = models.RoomStatus.AVAILABLE
        db.session.add(room)
        
        db.session.commit()
        
        return redirect(url_for('invoice_page'))
        
    return render_template('create-invoice.html'
                           , booking=booking
                           , invoice_details=invoice_details
                           , total_amount=total_amount
                           , payment=payment
                           , reminder=reminder
                           , is_read_only=is_read_only
                           , current_time=datetime.now().strftime('%d-%m-%Y'))


@app.route('/invoice')
def invoice_page():
    invoices = models.Invoice.query.all()
    return render_template('mdInvoice.html', invoices=invoices)

@app.route('/add-invoice', methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'POST':
        invoice = models.Invoice()
        invoice.booking = models.Booking.query.get(request.form['booking'])
        invoice.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        invoice.total_price = request.form['total_price']
        
        db.session.add(invoice)
        db.session.commit()
        
        return redirect(url_for('invoice_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('add-invoice.html', bookings=bookings)


@app.route('/edit-invoice/<int:invoice_id>', methods=['GET', 'POST'])
def edit_invoice(invoice_id):
    invoice = models.Invoice.query.get(invoice_id)
    
    if request.method == 'POST':
        invoice.booking = models.Booking.query.get(request.form['booking'])
        invoice.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        invoice.total_price = request.form['total_price']
        
        db.session.commit()
        
        return redirect(url_for('invoice_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('edit-invoice.html', invoice=invoice, bookings=bookings)


@app.route('/delete-invoice/<int:invoice_id>', methods=['GET', 'POST'])
def delete_invoice(invoice_id):
    invoice = models.Invoice.query.get(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    
    return redirect(url_for('invoice_page'))