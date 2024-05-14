from app import db

class BookingRoomService(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_room_id = db.Column(db.Integer, db.ForeignKey('booking_room.id'))
    booking_room = db.relationship('BookingRoom', backref='booking_room_service')
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('Service', backref='booking_room_service')
    qty = db.Column(db.Integer)
    created_date = db.Column(db.Date)
