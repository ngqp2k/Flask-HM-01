from app import db

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('payment', lazy=True))
    created_date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    payment_method = db.relationship('PaymentMethod', backref=db.backref('payment', lazy=True))
    transaction_id = db.Column(db.String(50))
    
    def __str__(self) -> str:
        return self.booking_id