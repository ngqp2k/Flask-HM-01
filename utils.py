from datetime import datetime
from app import db
import models

def build_sample_db():
    pass
    db.drop_all()
    db.create_all()

    # Create 2 roles
    role1 = models.Role(name='Admin')
    role2 = models.Role(name='User')
    db.session.add(role1)
    db.session.add(role2)
    
    # Create 2 users
    user1 = models.User(first_name='Phu', last_name='Nguyen', sex=models.Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' ,birthdate=datetime(2000, 3, 25), username='nqgp2k', password='123', role=role1)
    user2 = models.User(first_name='Hazard', last_name='Eden', sex=models.Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' , birthdate=datetime(2000, 3, 25), username='eden', password='123', role=role2)
    db.session.add(user1)
    db.session.add(user2)
    
    # Create 2 room types
    room_type1 = models.RoomType(name='Standard', price_per_night=100, capacity=3, bed_quantity=1)
    room_type2 = models.RoomType(name='Deluxe', price_per_night=200, capacity=3, bed_quantity=2)
    db.session.add(room_type1)
    db.session.add(room_type2)
    
    # Create 2 rooms
    room1 = models.Room(room_no='101', room_type=room_type1)
    room2 = models.Room(room_no='102', room_type=room_type2)
    db.session.add(room1)
    db.session.add(room2)
    
    # Create 2 customers
    customer1 = models.Customer(first_name='f1', last_name='l1', sex=models.Sex.Men, age=24, email='f1@example.com', phone='0123')
    
    # Create 2 bookings
    booking1 = models.Booking(customer_first_name='Phu', customer_last_name='Nguyen',age=20,sex=models.Sex.Men, email='ngqp2k@outlook.com', phone='0123',is_regioner=False,created_date=datetime(2000, 3, 25), checkin_date=datetime(2000, 3, 25), checkout_date=datetime(2000, 3, 25), total_price=1000, user=user1, room=room1, status=models.BookingStatus.PENDING, customer=customer1)
    booking2 = models.Booking(customer_first_name='Eden', customer_last_name='Nguyen',age=22,sex=models.Sex.Men, email='ngqp2k@example.com', phone='0948',is_regioner=False,created_date=datetime(2000, 3, 25), checkin_date=datetime(2000, 3, 25), checkout_date=datetime(2000, 3, 25), total_price=1000, user=user1, room=room2, status=models.BookingStatus.PENDING)
    db.session.add(booking1)
    db.session.add(booking2)
    
    # Create 2 invoice
    invoice1 = models.Invoice(booking=booking1, created_date=datetime(2000, 3, 25), total_price=1000)
    invoice2 = models.Invoice(booking=booking2, created_date=datetime(2000, 3, 25), total_price=2000)
    db.session.add(invoice1)
    db.session.add(invoice2)
    
    # Create 2 payment methods
    payment_method1 = models.PaymentMethod(name='Cash')
    payment_method2 = models.PaymentMethod(name='Credit Card')
    db.session.add(payment_method1)
    db.session.add(payment_method2)
    
    # Create 2 payments
    payment1 = models.Payment(booking=booking1, created_date=datetime(2000, 3, 25), amount=1000, payment_method=payment_method1, transaction_id='12345')
    payment2 = models.Payment(booking=booking2, created_date=datetime(2000, 3, 25), amount=2000, payment_method=payment_method2, transaction_id='54321')
    db.session.add(payment1)
    db.session.add(payment2)
    
    # Create 2 services
    service1 = models.Service(name='Breakfast', description='Breakfast', price=100)
    service2 = models.Service(name='Dinner', description='Dinner', price=200)
    db.session.add(service1)
    db.session.add(service2)
    
    # Create 2 additional charges
    additional_charge1 = models.AdditionalCharge(booking=booking1, created_date=datetime(2000, 3, 25), description='Breakfast', amount=100)
    additional_charge2 = models.AdditionalCharge(booking=booking2, created_date=datetime(2000, 3, 25), description='Dinner', amount=200)
    db.session.add(additional_charge1)
    db.session.add(additional_charge2)
    

    db.session.commit()