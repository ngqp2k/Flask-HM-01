from app import db
import models.myEnum as MyEnum

class BookingRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref='booking_room')
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref='booking_room')
    checkin_date = db.Column(db.Date)
    checkout_date = db.Column(db.Date)
    status = db.Column(db.Enum(MyEnum.BookingStatus))
