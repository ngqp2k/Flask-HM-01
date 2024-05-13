from app import db

class AdditionalCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_room_id = db.Column(db.Integer, db.ForeignKey('booking_room.id'))
    booking_room = db.relationship('BookingRoom', backref='additional_charge')
    created_date = db.Column(db.Date)
    description = db.Column(db.Text)
    amount = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.booking_id