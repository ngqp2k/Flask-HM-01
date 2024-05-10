from app import db


class RefundRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('refund_request', lazy=True))
    created_date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL)
    reason = db.Column(db.Text)
    
    def __str__(self) -> str:
        return self.booking_id