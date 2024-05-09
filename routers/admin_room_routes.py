from app import app, db
from flask import render_template, request, redirect, url_for


import models as models


@app.route('/room')
def room_page():
    rooms = models.Room.query.all()
    return render_template('mdRoom.html'
                           , rooms=rooms)


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
    statuses = [status.name for status in models.RoomStatus]
    
    return render_template('add-room.html'
                           , room_types=room_types
                           , statuses=statuses)
    
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
    statuses = [status.name for status in models.RoomStatus]
    print(f'ngqp2k: {statuses}')
    
    return render_template('edit-room.html'
                           , room=room
                           , room_types=room_types
                           , statuses=statuses)
    
@app.route('/delete-room/<int:room_id>', methods=['GET', 'POST'])
def delete_room(room_id):
    room = models.Room.query.get(room_id)
    db.session.delete(room)
    db.session.commit()
    
    return redirect(url_for('room_page'))