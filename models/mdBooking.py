from app import db
import models.myEnum as MyEnum


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_first_name = db.Column(db.String(50))
    customer_last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    sex = db.Column(db.Enum(MyEnum.Sex))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    is_regioner = db.Column(db.Boolean)
    created_date = db.Column(db.Date)
    checkin_date = db.Column(db.Date)
    checkout_date = db.Column(db.Date)
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('booking', lazy=True))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('booking', lazy=True))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    customer = db.relationship('Customer', backref=db.backref('booking', lazy=True))
    status = db.Column(db.Enum(MyEnum.BookingStatus))
    
    def __str__(self) -> str:
        return str(self.room)