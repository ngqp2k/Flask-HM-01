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
    user1 = models.User(first_name='Phu', last_name='Nguyen', sex=models.Sex.Men, email='ngqp2k@outlook.com', phone='+84857110010' ,birthdate=datetime(2000, 3, 25), username='admin', password='admin', role=role1)
    user2 = models.User(first_name='Hazard', last_name='Eden', sex=models.Sex.Women, email='eden99@example.com', phone='+841231234567' , birthdate=datetime(1997, 5, 9), username='user1', password='123', role=role2)
    db.session.add(user1)
    db.session.add(user2)
    
    # Create 2 room types
    room_type1 = models.RoomType(name='Tiêu chuẩn', price_per_night=1000000, capacity=3, bed_quantity=1)
    room_type2 = models.RoomType(name='Cao cấp', price_per_night=2000000, capacity=3, bed_quantity=2)
    room_type3 = models.RoomType(name='Đặc biệt', price_per_night=4000000, capacity=3, bed_quantity=2)
    db.session.add(room_type1)
    db.session.add(room_type2)
    db.session.add(room_type3)
    
    # Create 2 rooms
    room1 = models.Room(room_no='101', room_type=room_type1, status=models.RoomStatus.BOOKED, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893503/060912db19ae3c89079d6f2cd14aa054_ikj0vc.jpg')
    room2 = models.Room(room_no='102', room_type=room_type2, status=models.RoomStatus.BOOKED, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893540/19da767c8b8cd79a2ab68f9e2ece6b4a_dtutw8.jpg')
    room3 = models.Room(room_no='103', room_type=room_type3, status=models.RoomStatus.AVAILABLE, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893503/060912db19ae3c89079d6f2cd14aa054_ikj0vc.jpg')
    room4 = models.Room(room_no='201', room_type=room_type2, status=models.RoomStatus.AVAILABLE, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893540/19da767c8b8cd79a2ab68f9e2ece6b4a_dtutw8.jpg')
    room5 = models.Room(room_no='202', room_type=room_type1, status=models.RoomStatus.AVAILABLE, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893503/060912db19ae3c89079d6f2cd14aa054_ikj0vc.jpg')
    room6 = models.Room(room_no='203', room_type=room_type3, status=models.RoomStatus.AVAILABLE, image='https://res.cloudinary.com/dxll8tdwq/image/upload/v1714893540/19da767c8b8cd79a2ab68f9e2ece6b4a_dtutw8.jpg')
    db.session.add(room1)
    db.session.add(room2)
    db.session.add(room3)
    db.session.add(room4)
    db.session.add(room5)
    db.session.add(room6)
    
    # Create 2 customers
    # customer1 = models.Customer(first_name='A', last_name='Trần Văn', sex=models.Sex.Men, age=24, email='a@example.com', phone='0123')
    # customer2 = models.Customer(first_name='B', last_name='Lê Nguyễn', sex=models.Sex.Men, age=30, email='b@example.com', phone='0789')
    # db.session.add(customer1)
    # db.session.add(customer2)
    
    # Create 2 bookings
    booking1 = models.Booking(first_name='John', last_name='Conner', email='John@outlook.com', phone='095749574', created_date=datetime(2024, 5, 10), check_in_date=datetime(2024, 5, 10), check_out_date=datetime(2024, 5, 12), number_of_guests=2, number_of_rooms=1, user=user1)
    # booking2 = models.Booking(customer_first_name='Widow', customer_last_name='Black',age=22,sex=models.Sex.Women, email='Widow@example.com', phone='038471265',is_regioner=False,created_date=datetime(2024, 5, 10), checkin_date=datetime(2024, 5, 10), checkout_date=datetime(2024, 5, 12), total_price=0, user=user1, room=room4, status=models.BookingStatus.CONFIRMED)
    db.session.add(booking1)
    # db.session.add(booking2)

    booking_room_1 = models.BookingRoom(booking=booking1, room=room1, check_in_date=datetime(2024, 5, 10), check_out_date=datetime(2024, 5, 12), status=models.BookingStatus.CONFIRMED)
    booking_room_2 = models.BookingRoom(booking=booking1, room=room2, check_in_date=datetime(2024, 5, 10), check_out_date=datetime(2024, 5, 12), status=models.BookingStatus.CONFIRMED)
    db.session.add(booking_room_1)
    db.session.add(booking_room_2)
    
    # Create 2 invoice
    # invoice1 = models.Invoice(booking=booking1, created_date=datetime(2000, 3, 25), total_price=1000)
    # invoice2 = models.Invoice(booking=booking2, created_date=datetime(2000, 3, 25), total_price=2000)
    # db.session.add(invoice1)
    # db.session.add(invoice2)
    
    # Create 2 payment methods
    payment_method1 = models.PaymentMethod(name='Debit Card')
    payment_method2 = models.PaymentMethod(name='Credit Card')
    payment_method3 = models.PaymentMethod(name='Paypal')
    db.session.add(payment_method1)
    db.session.add(payment_method2)
    db.session.add(payment_method3)
    
    # Create 2 payments
    # payment1 = models.Payment(booking=booking1, created_date=datetime(2024, 5, 10), amount=booking1.room.room_type.price_per_night * 2, payment_method=payment_method1, transaction_id='12345')
    # payment2 = models.Payment(booking=booking2, created_date=datetime(2024, 5, 10), amount=booking2.room.room_type.price_per_night * 2, payment_method=payment_method2, transaction_id='54321')
    # db.session.add(payment1)
    # db.session.add(payment2)
    
    # Create 2 services
    service1 = models.Service(name='Bữa sáng 1', description='Bữa sáng 1', price=150000)
    service2 = models.Service(name='Bữa sáng 2', description='Bữa sáng 2', price=250000)
    service3 = models.Service(name='Bữa ăn tối 1', description='Bữa ăn tối 1', price=500000)
    service4 = models.Service(name='Bữa ăn tối 2', description='Bữa ăn tối 2', price=700000)
    service5 = models.Service(name='Bữa ăn tối 3', description='Bữa ăn tối 3', price=1000000)
    service6 = models.Service(name='Nước suối', description='Nước suối', price=15000)
    service7 = models.Service(name='Cocacola', description='Cocacola', price=22000)
    service8 = models.Service(name='Message', description='Message', price=1500000)
    
    db.session.add(service1)
    db.session.add(service2)
    db.session.add(service3)
    db.session.add(service4)
    db.session.add(service5)
    db.session.add(service6)
    db.session.add(service7)
    db.session.add(service8)

    booking_room_service_1 = models.BookingRoomService(booking_room=booking_room_1, service=service1, qty=2)
    booking_room_service_2 = models.BookingRoomService(booking_room=booking_room_1, service=service6, qty=3)
    booking_room_service_3 = models.BookingRoomService(booking_room=booking_room_1, service=service7, qty=7)
    db.session.add(booking_room_service_1)
    db.session.add(booking_room_service_2)
    db.session.add(booking_room_service_3)

    # Create 2 additional charges
    additional_charge1 = models.AdditionalCharge(booking_room=booking_room_1, created_date=datetime(2024, 5, 10), description='Phí làm hỏng bàn', amount=500000)
    # additional_charge2 = models.AdditionalCharge(booking=booking1, created_date=datetime(2024, 5, 10), description='Phí làm hỏng giường', amount=2000000)
    # additional_charge2 = models.AdditionalCharge(booking=booking2, created_date=datetime(2024, 5, 10), description='Dinner', amount=200)
    db.session.add(additional_charge1)
    # db.session.add(additional_charge2)
    

    db.session.commit()


def count_cart(cart):
    total_quantity, total_amount = 0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['num_of_nights']
            total_amount += c['num_of_nights'] * c['price']

    return {
        'total_quantity': cart.__len__() if cart else 0,
        'total_amount': total_amount
    }