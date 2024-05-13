from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    booking_room_id = db.Column(db.Integer, db.ForeignKey('booking_room.id'))
    booking_room = db.relationship('BookingRoom', backref='invoice')
    created_date = db.Column(db.Date)
    total_price = db.Column(db.DECIMAL)

    def __str__(self) -> str:
        return self.booking.user.username