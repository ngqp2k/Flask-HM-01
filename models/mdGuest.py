from app import db
import models.myEnum as MyEnum

class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(MyEnum.Sex))
    identification_number = db.Column(db.String(50))
    guest_type_id = db.Column(db.Integer, db.ForeignKey('guest_type.id'))
    guest_type = db.relationship('GuestType', backref='guest')
    booking_room_id = db.Column(db.Integer, db.ForeignKey('booking_room.id'))
    booking_room = db.relationship('BookingRoom', backref='guest')