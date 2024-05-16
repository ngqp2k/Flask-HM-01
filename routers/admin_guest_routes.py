from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required


import models as models


@app.route('/guest')
@login_required
def guest_page():
    guests = models.Guest.query.all()
    return render_template('mdGuest.html'
                           , guests=guests)


@app.route('/add-guest', methods=['GET', 'POST'])
@login_required
def add_guest():
    guest = models.Guest()
    
    if request.method == 'POST':
        guest.first_name = request.form['first_name']
        guest.last_name = request.form['last_name']
        guest.sex = models.Sex[request.form['sex']]
        guest.identification_number = request.form['identification_number']
        guest.guest_type = models.GuestType.query.get(request.form['guest_type'])
        guest.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        
        db.session.add(guest)
        db.session.commit()
        
        return redirect(url_for('guest_page'))
    
    guest_types = models.GuestType.query.all()
    booking_rooms = models.BookingRoom.query.all()
    sexs = [sex.name for sex in models.Sex]
    
    return render_template('add-guest.html'
                           , guest=guest
                           , guest_types=guest_types
                           , booking_rooms=booking_rooms
                           , sexs=sexs)
    
@app.route('/edit-guest/<int:guest_id>', methods=['GET', 'POST'])
@login_required
def edit_guest(guest_id):
    guest = models.Guest.query.get(guest_id)
    
    if request.method == 'POST':
        guest.first_name = request.form['first_name']
        guest.last_name = request.form['last_name']
        guest.sex = models.Sex[request.form['sex']]
        guest.identification_number = request.form['identification_number']
        guest.guest_type = models.GuestType.query.get(request.form['guest_type'])
        guest.booking_room = models.BookingRoom.query.get(request.form['booking_room'])
        
        db.session.commit()
        
        return redirect(url_for('guest_page'))
    
    guest_types = models.GuestType.query.all()
    booking_rooms = models.BookingRoom.query.all()
    sexs = [sex.name for sex in models.Sex]
    
    return render_template('edit-guest.html'
                           , guest=guest
                           , guest_types=guest_types
                           , booking_rooms=booking_rooms
                           , sexs=sexs)
    

@app.route('/delete-guest/<int:guest_id>', methods=['GET', 'POST'])
@login_required
def delete_guest(guest_id):
    guest = models.Guest.query.get(guest_id)
    db.session.delete(guest)
    db.session.commit()
    
    return redirect(url_for('guest_page'))