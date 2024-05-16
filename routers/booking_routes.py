from app import app, db
from flask import render_template, request, redirect, url_for, session, jsonify
from datetime import datetime, timedelta

import random
import models as models
import utils as utils

@app.route('/checkout/', methods=['GET', 'POST'])
def checkout_page():
    # r = Receipt(user=current_user)
    #     db.session.add(r)

    #     for c in cart.values():
    #         d = ReceiptDetails(quantity=c['quantity'], unit_price=c['price'],
    #                            receipt=r, product_id=c['id'])
    #         db.session.add(d)

    #     db.session.commit()

    cart = session.get('cart')

    room = models.Room.query.get(1)
    print(f'Room ID: {request.method}')

    # my_list = [elem[0] for elem in your_dict.values()]
    print()
        
    checkin_date = cart[next(iter(cart))]['check_in_date']
    checkout_date = cart[next(iter(cart))]['check_out_date']
    
    payment_methods = models.PaymentMethod.query.all()
    return render_template('checkout.html'
                            , room=room
                            , payment_methods=payment_methods
                            , checkin_date=checkin_date
                            , checkout_date=checkout_date
                            , num_of_nights=cart[next(iter(cart))]['num_of_nights'])
        
    return redirect(url_for('index'))


@app.route('/checkout-handler', methods=['POST'])
def checkout_handler():

    room_id = 0
    if request.method == 'POST':
        # create booking
        booking = models.Booking()
        booking.first_name = request.form['customer_first_name']
        booking.last_name = request.form['customer_last_name']
        booking.email = request.form['email']
        booking.phone = request.form['phone']
        booking.created_date = datetime.now()

        cart = session.get('cart')

        for c in cart.values():
            booking_room = models.BookingRoom()
            booking_room.booking = booking
            room = models.Room.query.get(c['id'])
            booking_room.room = room
            booking_room.check_in_date = datetime.strptime(c['check_in_date'], '%Y-%m-%d')
            booking_room.check_out_date = datetime.strptime(c['check_out_date'], '%Y-%m-%d')

            booking.check_in_date = datetime.strptime(c['check_in_date'], '%Y-%m-%d')
            booking.check_out_date = datetime.strptime(c['check_out_date'], '%Y-%m-%d')
            booking.number_of_guests = c['num_of_guests']

            booking_room.status = models.BookingStatus['CONFIRMED']

            db.session.add(booking_room)

            room.status = models.RoomStatus['BOOKED']

            db.session.add(room)

        booking.number_of_rooms = len(cart) if cart else 0


        # room = models.Room.query.get(room_id)
        # room.status = models.RoomStatus['BOOKED']
        # booking.room = room
        # booking.status = models.BookingStatus['CONFIRMED']
        
        # create payment
        payment = models.Payment()
        payment.booking = booking
        payment.created_date = datetime.now()
        payment.amount = utils.count_cart(cart)['total_amount']
        payment.transaction_id = random.randint(100000, 999999)
        payment.payment_method = models.PaymentMethod.query.get(request.form['payment_method'])

        db.session.add(booking)
        db.session.add(payment)
        
        db.session.commit()

        cart = session.get('cart')
        del session['cart']
        
    return redirect(url_for('index'))


@app.route('/cart')
def cart_page():
    return render_template('cart.html')


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():

    data = request.json

    id = data.get('id')
    name = str(data.get('name'))
    price = data.get('price')
    num_of_nights = int(data.get('num_of_nights'))
    num_of_guests = int(data.get('num_of_guests'))
    check_in_date = data.get('check_in_date')
    check_out_date = data.get('check_out_date')

    print(f'Check-in Date: {check_in_date} Check-out Date: {check_out_date}')

    cart = session.get('cart')

    if not cart:
        cart = {}

    id = str(request.json.get('id'))

    if id in cart:
        cart[id]['num_of_nights'] = num_of_nights
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1,
            'num_of_nights': num_of_nights,
            'num_of_guests': num_of_guests,
            'check_in_date': check_in_date,
            'check_out_date': check_out_date,
        }

    for c in cart.values():
        c['num_of_nights'] = num_of_nights
        c['check_in_date'] = check_in_date
        c['check_out_date'] = check_out_date
        c['num_of_guests'] = num_of_guests

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/api/pay", methods=['post'])
def pay():
    cart = session.get('cart')
    try:
        print(cart)
    except Exception as ex:
        print(ex)
        return jsonify({'status': 500})
    else:
        del session['cart']
        return jsonify({'status': 200})
    

@app.route('/api/cart/<room_id>', methods=['delete'])
def delete_cart(room_id):
    cart = session.get('cart')
    if cart and room_id in cart:
        del cart[room_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))