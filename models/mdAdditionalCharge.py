from app import db

class AdditionalCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('additional_charge', lazy=True))
    created_date = db.Column(db.Date)
    description = db.Column(db.Text)
    amount = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.booking_id