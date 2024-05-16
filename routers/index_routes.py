from app import app
from flask import render_template, session, request
from flask_login import login_required
from datetime import datetime, timedelta


import models as models
import utils as utils


# Index Admin page
@app.route('/admin')
@login_required
def admin_page():
    return render_template('admin.html')


# Index page
@app.route('/', methods=['GET', 'POST'])
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    rooms = models.Room.query.all()

    print(f'request method: {request.method}')

    if request.method == 'POST':
        check_in_date = datetime.strptime(request.form['checkin_date'], '%Y-%m-%d').date()
        num_of_nights = request.form['num_of_nights']
        check_out_date = check_in_date + timedelta(days=float(num_of_nights))
        num_of_guests = request.form['num_of_guests']

        print(f'check_in_date: {check_in_date}')
        print(f'check_out_date: {check_out_date}')
        print(f'num_of_nights: {num_of_nights}')
        print(f'num_of_guests: {num_of_guests}')

        list_room_booked = []

        booking_rooms = models.BookingRoom.query.all()
        for booking_room in booking_rooms:
            if booking_room.check_in_date <= check_in_date and booking_room.check_out_date >= check_out_date:
                print(f'booking_room.room_id: {booking_room.room_id}')
                list_room_booked.append(booking_room.room_id)

    
        
        rooms = models.Room.query.filter(models.Room.id.notin_(list_room_booked)).all()


    return render_template('index.html'
                           , current_time=today
                           , tomorrow=tomorrow
                           , rooms=rooms)


@app.context_processor
def common_response():
    return {
        'cart_stats': utils.count_cart(session.get('cart')),
        'check_in_date': datetime.now().strftime('%Y-%m-%d'),
        'check_out_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
        'num_of_nights': 1,
        'num_of_guests': 1,
        'current_date': datetime.now().strftime('%Y-%m-%d'),
    }