from app import db

class BookingServices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    qty = db.Column(db.Integer)

    booking = db.relationship('Booking', backref='bookings')
    service = db.relationship('Service', backref='services')