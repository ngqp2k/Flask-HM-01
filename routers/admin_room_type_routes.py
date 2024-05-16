from app import app, db
from flask import render_template, request, redirect, url_for
from flask_login import login_required


import models as models


@app.route('/room-type')
@login_required
def room_type_page():
    room_types = models.RoomType.query.all()
    return render_template('mdRoomType.html', room_types=room_types)


@app.route('/add-room-type', methods=['GET', 'POST'])
@login_required
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
@login_required
def edit_room_type(room_type_id):
    room_type = models.RoomType.query.get(room_type_id)
    
    if request.method == 'POST':
        room_type.name = request.form['name']
        room_type.price_per_night = request.form['price_per_night']
        room_type.capacity = request.form['capacity']
        room_type.bed_quantity = request.form['bed_quantity']
        
        db.session.commit()
        
        return redirect(url_for('room_type_page'))
    
    return render_template('edit-room-type.html', room_type=room_type)


@app.route('/delete-room-type/<int:room_type_id>', methods=['GET', 'POST'])
@login_required
def delete_room_type(room_type_id):
    room_type = models.RoomType.query.get(room_type_id)
    db.session.delete(room_type)
    db.session.commit()
    
    return redirect(url_for('room_type_page'))