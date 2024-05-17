import decimal
from app import app, db
from flask import render_template, request, redirect, url_for
from datetime import datetime
from flask_login import login_required
from decimal import Decimal


import models as models


class InvoiceDetail():
    def __init__(self, description, unit_price, qty, amount):
        self.description = description
        self.unit_price = unit_price
        self.qty = qty
        self.amount = amount

@app.route('/create-invoice/<int:booking_room_id>', methods=['GET', 'POST'])
@login_required
def invoice_detail_page(booking_room_id):

    booking_room = models.BookingRoom.query.get(booking_room_id)

    booking = booking_room.booking

    room = booking_room.room
    
        
    # get all payment of booking
    payment = models.Payment.query.filter_by(booking_id=booking.id).first()
    # get all additional charges of booking
    additional_charges = models.AdditionalCharge.query.filter_by(booking_room_id=booking_room_id).all()
    # get all services of booking
    booking_services = models.BookingRoomService.query.filter_by(booking_room_id=booking_room_id).all()
    
    
    # create invoice details
    total_amount = 0
    
    invoice_details = []
    
    cnt_date = (booking_room.check_out_date - booking_room.check_in_date).days
    invoice_detail = InvoiceDetail('Tiền phòng', booking_room.room.room_type.price_per_night, cnt_date, booking_room.room.room_type.price_per_night * cnt_date)
    total_amount += decimal.Decimal(invoice_detail.amount)
    invoice_details.append(invoice_detail)
        
    for additional_charge in additional_charges:
        invoice_detail = InvoiceDetail(additional_charge.description, additional_charge.amount, 1, additional_charge.amount)
        total_amount += invoice_detail.amount
        invoice_details.append(invoice_detail)
        
    for booking_service in booking_services:
        invoice_detail = InvoiceDetail(booking_service.service.name, booking_service.service.price, booking_service.qty, booking_service.service.price * booking_service.qty)
        total_amount += decimal.Decimal(invoice_detail.amount)
        invoice_details.append(invoice_detail)

    num_of_guests = models.Guest.query.filter_by(booking_room_id=booking_room_id).count()

    if num_of_guests >= 3:
        policy = models.Policy.query.get(1)
        amount = booking_room.room.room_type.price_per_night * cnt_date * Decimal(policy.value) / 100
        invoice_detail = InvoiceDetail(f'Phí có thêm người thứ 3 (x  {policy.value}%)'
                                       , booking_room.room.room_type.price_per_night * cnt_date, 1
                                       , amount) 
        total_amount += decimal.Decimal(invoice_detail.amount)
        invoice_details.append(invoice_detail)

    guests = models.Guest.query.filter_by(booking_room_id=booking_room_id).all()
    is_regioners = False
    for guest in guests:
        if guest.guest_type.name == models.GuestType.query.get(2).name:
            is_regioners = True
            break

    if is_regioners:
        policy = models.Policy.query.get(2)
        amount = booking_room.room.room_type.price_per_night * cnt_date * Decimal(policy.value - 1.0)
        invoice_detail = InvoiceDetail(f'Phí người nước ngoài (x  {policy.value})'
                                       , booking_room.room.room_type.price_per_night * cnt_date, 1
                                       , amount) 
        total_amount += decimal.Decimal(invoice_detail.amount)
        invoice_details.append(invoice_detail)

        
    if payment is None:
        reminder = total_amount
    else:

        reminder = total_amount - booking_room.room.room_type.price_per_night * cnt_date
        
    is_read_only = booking_room.status == models.BookingStatus.CHECKED_OUT
        
    if request.method == 'POST':
        invoice = models.Invoice()
        invoice.first_name = booking.first_name
        invoice.last_name = booking.last_name
        invoice.booking_room = booking_room
        invoice.created_date = booking.check_out_date
        invoice.total_price = total_amount
        
        db.session.add(invoice)
        
        booking_room.status = models.BookingStatus.CHECKED_OUT
        db.session.add(booking_room)
        
        room = booking_room.room
        room.status = models.RoomStatus.AVAILABLE
        db.session.add(room)



        for invoice_detail in invoice_details:
            invoiceDetail = models.InvoiceDetail()
            invoiceDetail.invoice = invoice
            invoiceDetail.description = invoice_detail.description
            invoiceDetail.unit_price = invoice_detail.unit_price
            invoiceDetail.qty = invoice_detail.qty
            invoiceDetail.amount = invoice_detail.amount
            invoiceDetail.created_date = datetime.now()
            db.session.add(invoiceDetail)


        

        
        db.session.commit()
        
        return redirect(url_for('booking_room_page'))
        
    return render_template('create-invoice.html'
                           , booking_room=booking_room
                           , invoice_details=invoice_details
                           , total_amount=total_amount
                           , payment=payment
                           , payment_amout=booking_room.room.room_type.price_per_night * cnt_date
                           , reminder=reminder
                           , is_read_only=is_read_only
                           , current_time=datetime.now().strftime('%d-%m-%Y'))


@app.route('/invoice')
@login_required
def invoice_page():
    invoices = models.Invoice.query.all()
    return render_template('mdInvoice.html', invoices=invoices)

@app.route('/add-invoice', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_invoice(invoice_id):
    invoice = models.Invoice.query.get(invoice_id)
    db.session.delete(invoice)
    db.session.commit()
    
    return redirect(url_for('invoice_page'))


@app.route('/view-invoice-1/<int:invoice_id>')
@login_required
def view_invoice(invoice_id):
    invoice = models.Invoice.query.get(invoice_id)
    
    payment = models.Payment.query.filter_by(booking_id=invoice.booking_room.booking.id).first()

    reminder = invoice.total_price - payment.amount if payment is not None else invoice.total_price

    invoice_details = models.InvoiceDetail.query.filter_by(invoice_id=invoice_id).all()

    return render_template('view-invoice.html'
                           , invoice=invoice
                           , payment=payment
                           , reminder=reminder
                           , invoice_details=invoice_details)


@app.route('/view-invoice-2/<int:booking_room_id>')
@login_required
def view_invoice_2(booking_room_id):
    invoice = models.Invoice.query.filter_by(booking_room_id=booking_room_id).first()
    
    payment = models.Payment.query.filter_by(booking_id=invoice.booking_room.booking.id).first()

    reminder = invoice.total_price - payment.amount if payment is not None else invoice.total_price

    invoice_details = models.InvoiceDetail.query.filter_by(invoice_id=invoice.id).all()

    return render_template('view-invoice.html'
                           , invoice=invoice
                           , payment=payment
                           , reminder=reminder
                           , invoice_details=invoice_details)
