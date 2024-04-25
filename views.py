import enum
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
# from models import User, Role, Sex
from flask_wtf import FlaskForm
from wtforms import StringField
from datetime import datetime
from werkzeug.security import check_password_hash


import models as models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        user = models.User.query.filter_by(username=request.form['username']).first()
        
        print(user is None)
        
        if not user is None:
            print(user.hash_password)
            print(request.form['password'])
            print(user is None)
            print(check_password_hash(user.hash_password, request.form['password']))
    
        if (user is None) or (not check_password_hash(user.hash_password, request.form['password'])):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('admin_page'))
        
    return render_template('signin.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in_page():
    return render_template('signin.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('sign_in_page'))


@app.route('/')
def index():
    return render_template('index_home_page.html')


@app.route('/admin')
@login_required
def admin_page():
    return render_template('index.html')

@app.template_filter()
def to_string(obj):
    if isinstance(obj, enum.Enum):
        return obj.name

    return obj


@app.route('/user')
def user_page():
    users = models.User.query.all()
    return render_template('mdUser.html', users=users)


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    
    if request.method == 'POST':
        user = models.User()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        sex = request.form['sex']
        print(sex)
        user.sex = models.Sex[sex]
        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.username = request.form['username']
        user.password = request.form['password']
        user.rold_id = request.form['role']
        
        with app.app_context():
            db.session.add(user)
            db.session.commit()
        
        return redirect(url_for('user_page'))
    
    return render_template('add-user.html')
    
    
@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = models.User.query.get(user_id)
    
    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.sex = models.Sex[request.form['sex']]
        user.birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.username = request.form['username']
        user.password = request.form['password']
        
        role = models.Role.query.get(request.form['role'])
        user.role = role
        
        db.session.commit()
        
        return redirect(url_for('user_page'))
    
    sexs = [sex.name for sex in models.Sex]
    roles = models.Role.query.all()
    
    return render_template('edit-user.html'
                           , user=user, sexs=sexs
                           , roles=roles)


@app.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
def delete_user(user_id):
    user = models.User.query.get(user_id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    
    return redirect(url_for('user_page'))


@app.route('/role')
def role_page():
    roles = models.Role.query.all()
    return render_template('mdRole.html', roles=roles)


@app.route('/add-role', methods=['GET', 'POST'])
def add_role():
    if request.method == 'POST':
        role = models.Role()
        role.name = request.form['name']
        
        with app.app_context():
            db.session.add(role)
            db.session.commit()
        
        return redirect(url_for('role_page'))
    
    return render_template('add-role.html')

@app.route('/edit-role/<int:role_id>', methods=['GET', 'POST'])
def edit_role(role_id):
    role = models.Role.query.get(role_id)
    
    if request.method == 'POST':
        role.name = request.form['name']
        
        db.session.commit()
        
        return redirect(url_for('role_page'))
    
    return render_template('edit-role.html', role=role)


@app.route('/delete-role/<int:role_id>', methods=['GET', 'POST'])
def delete_role(role_id):
    role = models.Role.query.get(role_id)
    db.session.delete(role)
    db.session.commit()
    
    return redirect(url_for('role_page'))

@app.route('/room-type')
def room_type_page():
    room_types = models.RoomType.query.all()
    return render_template('mdRoomType.html', room_types=room_types)


@app.route('/add-room-type', methods=['GET', 'POST'])
def add_room_type():
    if request.method == 'POST':
        room_type = models.RoomType()
        room_type.name = request.form['name']
        room_type.price_per_night = request.form['price_per_night']
        room_type.capacity = request.form['capacity']
        room_type.bed_quantity = request.form['bed_quantity']
        
        with app.app_context():
            db.session.add(room_type)
            db.session.commit()
        
        return redirect(url_for('room_type_page'))
    
    return render_template('add-room-type.html')

@app.route('/edit-room-type/<int:room_type_id>', methods=['GET', 'POST'])
def edit_room_type(room_type_id):
    room_type = models.RoomType.query.get(room_type_id)
    
    if request.method == 'POST':
        room_type.name = request.form['name']
        
        db.session.commit()
        
        return redirect(url_for('room_type_page'))
    
    return render_template('edit-room-type.html', room_type=room_type)


@app.route('/delete-room-type/<int:room_type_id>', methods=['GET', 'POST'])
def delete_room_type(room_type_id):
    room_type = models.RoomType.query.get(room_type_id)
    db.session.delete(room_type)
    db.session.commit()
    
    return redirect(url_for('room_type_page'))


@app.route('/room')
def room_page():
    rooms = models.Room.query.all()
    return render_template('mdRoom.html', rooms=rooms)


@app.route('/add-room', methods=['GET', 'POST'])
def add_room():
    
    if request.method == 'POST':
        room = models.Room()
        room.room_no = request.form['room_no']
        room.image = request.form['image']
        room.description = request.form['description']
        room.room_type = models.RoomType.query.get(request.form['room_type'])
        
        db.session.add(room)
        db.session.commit()
        
        return redirect(url_for('room_page'))
    
    room_types = models.RoomType.query.all()
    
    return render_template('add-room.html'
                           , room_types=room_types)
    
@app.route('/edit-room/<int:room_id>', methods=['GET', 'POST'])
def edit_room(room_id):
    room = models.Room.query.get(room_id)
    
    if request.method == 'POST':
        room.room_no = request.form['room_no']
        room.image = request.form['image']
        room.description = request.form['description']
        
        room_type = models.RoomType.query.get(request.form['room_type'])
        room.room_type = room_type
        
        db.session.commit()
        
        return redirect(url_for('room_page'))
    
    room_types = models.RoomType.query.all()
    
    return render_template('edit-room.html'
                           , room=room, room_types=room_types)
    
@app.route('/delete-room/<int:room_id>', methods=['GET', 'POST'])
def delete_room(room_id):
    room = models.Room.query.get(room_id)
    db.session.delete(room)
    db.session.commit()
    
    return redirect(url_for('room_page'))


@app.route('/service')
def service_page():
    services = models.Service.query.all()
    return render_template('mdService.html', services=services)


@app.route('/add-service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        service = models.Service()
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        
        db.session.add(service)
        db.session.commit()
        
        return redirect(url_for('service_page'))
    
    return render_template('add-service.html')


@app.route('/edit-service/<int:service_id>', methods=['GET', 'POST'])
def edit_service(service_id):
    service = models.Service.query.get(service_id)
    
    if request.method == 'POST':
        service.name = request.form['name']
        service.description = request.form['description']
        service.price = request.form['price']
        
        db.session.commit()
        
        return redirect(url_for('service_page'))
    
    return render_template('edit-service.html', service=service)


@app.route('/delete-service/<int:service_id>', methods=['GET', 'POST'])
def delete_service(service_id):
    service = models.Service.query.get(service_id)
    db.session.delete(service)
    db.session.commit()
    
    return redirect(url_for('service_page'))

# invoice
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
        payment.transaction_id = request.form['transaction_id']
        payment.payment_method = models.PaymentMethod.query.get(request.form['payment_method'])
        
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
    
    invoices = models.Invoice.query.all()
    
    return render_template('edit-payment.html', payment=payment, invoices=invoices)


@app.route('/delete-payment/<int:payment_id>', methods=['GET', 'POST'])
def delete_payment(payment_id):
    payment = models.Payment.query.get(payment_id)
    db.session.delete(payment)
    db.session.commit()
    
    return redirect(url_for('payment_page'))

#additional charges
@app.route('/additional-charge')
def additional_charge_page():
    additional_charges = models.AdditionalCharge.query.all()
    return render_template('mdAdditionalCharge.html', additional_charges=additional_charges)

@app.route('/add-additional-charge', methods=['GET', 'POST'])
def add_additional_charge():
    if request.method == 'POST':
        additional_charge = models.AdditionalCharge()
        additional_charge.booking = models.Booking.query.get(request.form['booking'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.add(additional_charge)
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('add-additional-charge.html', bookings=bookings)

@app.route('/edit-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
def edit_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    
    if request.method == 'POST':
        additional_charge.booking = models.Booking.query.get(request.form['booking'])
        additional_charge.created_date = datetime.strptime(request.form['created_date'], '%Y-%m-%d')
        additional_charge.description = request.form['description']
        additional_charge.amount = request.form['amount']
        
        db.session.commit()
        
        return redirect(url_for('additional_charge_page'))
    
    bookings = models.Booking.query.all()
    
    return render_template('edit-additional-charge.html', additional_charge=additional_charge, bookings=bookings)

@app.route('/delete-additional-charge/<int:additional_charge_id>', methods=['GET', 'POST'])
def delete_additional_charge(additional_charge_id):
    additional_charge = models.AdditionalCharge.query.get(additional_charge_id)
    db.session.delete(additional_charge)
    db.session.commit()
    
    return redirect(url_for('additional_charge_page'))

@app.route('/booking')
def booking_page():
    bookings = models.Booking.query.all()
    return render_template('mdBooking.html', bookings=bookings)


@app.route('/add-booking', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        # Retrieve form data
        # Example: 
        # room_id = request.form['room_id']
        # start_date = request.form['start_date']
        # end_date = request.form['end_date']
        
        # Create a new booking object
        # Example:
        # booking = models.Booking(room_id=room_id, start_date=start_date, end_date=end_date)
        
        # Add the booking to the database
        # Example:
        # db.session.add(booking)
        # db.session.commit()
        
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
        # Retrieve form data and update the booking object
        # Example:
        # booking.room_id = request.form['room_id']
        # booking.start_date = request.form['start_date']
        # booking.end_date = request.form['end_date']
        
        # Commit the changes to the database
        # Example:
        # db.session.commit()
        
        # Redirect to the booking page
        return redirect(url_for('booking_page'))
    
    rooms = models.Room.query.all()
    
    return render_template('edit-booking.html', booking=booking, rooms=rooms)


@app.route('/delete-booking/<int:booking_id>', methods=['GET', 'POST'])
def delete_booking(booking_id):
    booking = models.Booking.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    
    return redirect(url_for('booking_page'))