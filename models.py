import enum
from app import db
from werkzeug.security import generate_password_hash

class Sex(enum.Enum):
    Men = 1,
    Women = 2,
    Other = 3
    

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __str__(self) -> str:
        return self.name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(Sex))
    birthdate = db.Column(db.Date)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    username = db.Column(db.String(255), unique=True)
    hash_password = db.Column(db.String(255))
    rold_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('user', lazy=True))

    def __str__(self) -> str:
        return self.username
    
    @property
    def password(self):
        raise AttributeError('password: write-only field')
        
    @password.setter
    def password(self, password: str):
            self.hash_password = generate_password_hash(password)
            
    # Flask-Login integration
    # NOTE: is_authenticated, is_active, and is_anonymous
    # are methods in Flask-Login < 0.3.0
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    # Required for administrative interface
    def __unicode__(self):
        return self.username
        
   
class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price_per_night = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    bed_quantity = db.Column(db.Integer)
    
    def __str__(self) -> str:
        return self.name


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(50))  
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'))
    room_type = db.relationship('RoomType', backref=db.backref('room', lazy=True))
    
    def __str__(self) -> str:
        return self.room_no
    
    
class BookingStatus(enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    CHECKED_IN = "Checked-in"
    CHECKED_OUT = "Checked-out"
    NO_SHOW = "No-show"
    OVERDUE = "Overdue"
    ON_HOLD = "On-hold"
    ERROR = "Error"


# booking_services = db.Table('booking_services',
#     db.Column('booking_id', db.Integer(), db.ForeignKey('booking.id')),
#     db.Column('service_id', db.Integer(), db.ForeignKey('service.id')))

class BookingServices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    qty = db.Column(db.Integer)

    booking = db.relationship('Booking', backref='bookings')
    service = db.relationship('Service', backref='services')


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_first_name = db.Column(db.String(50))
    customer_last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    sex = db.Column(db.Enum(Sex))
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
    status = db.Column(db.Enum(BookingStatus))
    
    def __str__(self) -> str:
        return str(self.id)


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.name


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('invoice', lazy=True))
    created_date = db.Column(db.Date)
    total_price = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.booking.user.username
    

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    def __str__(self) -> str:
        return self.name


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
    
class RefundRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('refund_request', lazy=True))
    created_date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL)
    reason = db.Column(db.Text)
    
    def __str__(self) -> str:
        return self.booking_id


class AdditionalCharge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('additional_charge', lazy=True))
    created_date = db.Column(db.Date)
    description = db.Column(db.Text)
    amount = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.booking_id
    
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(Sex))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))