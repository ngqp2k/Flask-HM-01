from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
import enum


app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['DATABASE_FILE'] = 'sample_db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.config['DATABASE_FILE']
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


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
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    total_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('booking', lazy=True))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', backref=db.backref('booking', lazy=True))
    status = db.Column(db.Enum(BookingStatus))
    
    def __str__(self) -> str:
        return self.id


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
    
class RefundRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'))
    booking = db.relationship('Booking', backref=db.backref('refund_request', lazy=True))
    created_date = db.Column(db.Date)
    amount = db.Column(db.DECIMAL)
    reason = db.Column(db.Text)
    
    def __str__(self) -> str:
        return self.booking.user.username
    

@app.route('/')
def index():
    return render_template('index.html')

@app.template_filter()
def to_string(obj):
    if isinstance(obj, enum.Enum):
        return obj.name

    return obj


@app.route('/user')
def user_page():
    users = User.query.all()
    return render_template('mdUser.html', users=users)


@app.route('/role')
def role_page():
    roles = Role.query.all()
    return render_template('mdRole.html', roles=roles)

def build_sample_db():
    
    db.drop_all()
    db.create_all()

    # Create 2 roles
    role1 = Role(name='Admin')
    role2 = Role(name='User')
    db.session.add(role1)
    db.session.add(role2)
    
    # Create 2 users
    user1 = User(first_name='Phu', last_name='Nguyen', sex=Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' ,birthdate=datetime(2000, 3, 25), username='nqgp2k', password='123', role=role1)
    user2 = User(first_name='Hazard', last_name='Eden', sex=Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' , birthdate=datetime(2000, 3, 25), username='eden', password='123', role=role2)
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()


if __name__ == '__main__':
    # with app.app_context():
    #     build_sample_db()
    app.run(debug=True)