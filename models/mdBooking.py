from app import db
import models.myEnum as MyEnum


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    created_date = db.Column(db.Date)
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    number_of_guests = db.Column(db.Integer)
    number_of_rooms = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('booking', lazy=True))
    
    def __str__(self) -> str:
        return str(self.room)