from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('invoice', lazy=True))
    created_date = db.Column(db.Date)
    total_price = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.booking.user.username