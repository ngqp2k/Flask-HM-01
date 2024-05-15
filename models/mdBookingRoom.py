from app import db
import models.myEnum as MyEnum


class BookingRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref='booking_room')
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref='booking_room')
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    status = db.Column(db.Enum(MyEnum.BookingStatus))

    def __str__(self) -> str:
        return self.room.room_no