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

    url_rooms = [
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790428/point3d-commercial-imaging-ltd-oxeCZrodz78-unsplash_zchecn.jpg',
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790426/vojtech-bruzek-Yrxr3bsPdS0-unsplash_negjhq.jpg',
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790417/point3d-commercial-imaging-ltd-5BV56SdvLmo-unsplash_atjs7s.jpg',
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790413/roberto-nickson-emqnSQwQQDo-unsplash_c3ahu9.jpg',
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790411/iwood-R5v8Xtc0ecg-unsplash_pyt7mu.jpg',
        'https://res.cloudinary.com/dxll8tdwq/image/upload/v1715790289/visualsofdana-T5pL6ciEn-I-unsplash_hurwud.jpg'
    ]
    
    # Create 2 rooms
    room1 = models.Room(room_no='101', room_type=room_type1, status=models.RoomStatus.AVAILABLE, image=url_rooms[0])
    room2 = models.Room(room_no='102', room_type=room_type2, status=models.RoomStatus.AVAILABLE, image=url_rooms[1])
    room3 = models.Room(room_no='103', room_type=room_type3, status=models.RoomStatus.AVAILABLE, image=url_rooms[2])
    room4 = models.Room(room_no='201', room_type=room_type2, status=models.RoomStatus.AVAILABLE, image=url_rooms[3])
    room5 = models.Room(room_no='202', room_type=room_type1, status=models.RoomStatus.AVAILABLE, image=url_rooms[4])
    room6 = models.Room(room_no='203', room_type=room_type3, status=models.RoomStatus.AVAILABLE, image=url_rooms[5])
    db.session.add(room1)
    db.session.add(room2)
    db.session.add(room3)
    db.session.add(room4)
    db.session.add(room5)
    db.session.add(room6)
    
    
    # Create 3 bookings in April 2024
    booking1 = models.Booking(
        first_name='John', last_name='Conner', email='John@outlook.com', phone='095749574'
        , created_date=datetime(2024, 4, 10), check_in_date=datetime(2024, 4, 10), check_out_date=datetime(2024, 4, 12)
        , number_of_guests=2, number_of_rooms=1, user=user1
    )
    booking2 = models.Booking(
        first_name='Shaw', last_name='Luk', email='Luk@outlook.com', phone='0123214'
        , created_date=datetime(2024, 4, 13), check_in_date=datetime(2024, 4, 13), check_out_date=datetime(2024, 4, 14)
        , number_of_guests=2, number_of_rooms=2, user=user1
    )
    booking3 = models.Booking(
        first_name='Hazard', last_name='Eden', email='Hazard@outlook.com', phone='0764382'
        , created_date=datetime(2024, 4, 23), check_in_date=datetime(2024, 4, 23), check_out_date=datetime(2024, 4, 26)
        , number_of_guests=2, number_of_rooms=2, user=user1
    )

     # Create 3 bookings in May 2024
    booking4 = models.Booking(
        first_name='Widow', last_name='Black', email='Widow@outlook.com', phone='038471265'
        , created_date=datetime(2024, 5, 10), check_in_date=datetime(2024, 5, 10), check_out_date=datetime(2024, 5, 12)
        , number_of_guests=2, number_of_rooms=1, user=user1
    )
    booking5 = models.Booking(
        first_name='Thor', last_name='Odinson', email='Thor@outlook.com', phone='0987654321'
        , created_date=datetime(2024, 5, 15), check_in_date=datetime(2024, 5, 15), check_out_date=datetime(2024, 5, 17)
        , number_of_guests=1, number_of_rooms=1, user=user1
    )
    booking6 = models.Booking(
        first_name='Natasha', last_name='Romanoff', email='Natasha@outlook.com', phone='0123456789'
        , created_date=datetime(2024, 5, 20), check_in_date=datetime(2024, 5, 20), check_out_date=datetime(2024, 5, 22)
        , number_of_guests=2, number_of_rooms=2, user=user1
    )

    
    db.session.add(booking1)
    db.session.add(booking2)
    db.session.add(booking3)
    db.session.add(booking4)
    db.session.add(booking5)
    db.session.add(booking6)

    booking_room_1 = models.BookingRoom(booking=booking1, room=room1
                                        , check_in_date=booking1.check_in_date, check_out_date=booking1.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)
    
    booking_room_2 = models.BookingRoom(booking=booking2, room=room1
                                        , check_in_date=booking2.check_in_date, check_out_date=booking2.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)
    
    booking_room_3 = models.BookingRoom(booking=booking2, room=room2
                                        , check_in_date=booking2.check_in_date, check_out_date=booking2.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)
    
    booking_room_4 = models.BookingRoom(booking=booking3, room=room3
                                        , check_in_date=booking3.check_in_date, check_out_date=booking3.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)
    
    booking_room_5 = models.BookingRoom(booking=booking3, room=room4
                                        , check_in_date=booking3.check_in_date, check_out_date=booking3.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)
    
    booking_room_7 = models.BookingRoom(booking=booking4, room=room1
                                        , check_in_date=booking4.check_in_date, check_out_date=booking4.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)

    booking_room_8 = models.BookingRoom(booking=booking5, room=room2
                                        , check_in_date=booking5.check_in_date, check_out_date=booking5.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)

    booking_room_9 = models.BookingRoom(booking=booking5, room=room3
                                        , check_in_date=booking5.check_in_date, check_out_date=booking5.check_out_date
                                        , status=models.BookingStatus.CONFIRMED)

    booking_room_10 = models.BookingRoom(booking=booking6, room=room4
                                         , check_in_date=booking6.check_in_date, check_out_date=booking6.check_out_date
                                         , status=models.BookingStatus.CONFIRMED)

    booking_room_11 = models.BookingRoom(booking=booking6, room=room5
                                         , check_in_date=booking6.check_in_date, check_out_date=booking6.check_out_date
                                         , status=models.BookingStatus.CONFIRMED)
    
    db.session.add(booking_room_1)
    db.session.add(booking_room_2)
    db.session.add(booking_room_3)
    db.session.add(booking_room_4)
    db.session.add(booking_room_5)
    db.session.add(booking_room_7)
    db.session.add(booking_room_8)
    db.session.add(booking_room_9)
    db.session.add(booking_room_10)
    db.session.add(booking_room_11)
    
    
    
    # Create 2 invoice
    # invoice1 = models.Invoice(booking=booking1, created_date=datetime(2000, 3, 25), total_price=1000)
    # invoice2 = models.Invoice(booking=booking2, created_date=datetime(2000, 3, 25), total_price=2000)
    # db.session.add(invoice1)
    # db.session.add(invoice2)
    
    # Create 2 payment methods
    payment_method1 = models.PaymentMethod(name='Debit Card')
    payment_method2 = models.PaymentMethod(name='Credit Card')
    payment_method3 = models.PaymentMethod(name='Paypal')
    payment_method4 = models.PaymentMethod(name='Cash')
    db.session.add(payment_method1)
    db.session.add(payment_method2)
    db.session.add(payment_method3)
    db.session.add(payment_method4)
    
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

    booking_room_service_4 = models.BookingRoomService(booking_room=booking_room_2, service=service2, qty=1)
    booking_room_service_5 = models.BookingRoomService(booking_room=booking_room_2, service=service1, qty=2)

    booking_room_service_6 = models.BookingRoomService(booking_room=booking_room_3, service=service2, qty=3)
    booking_room_service_7 = models.BookingRoomService(booking_room=booking_room_3, service=service3, qty=2)

    booking_room_service_8 = models.BookingRoomService(booking_room=booking_room_4, service=service3, qty=2)
    booking_room_service_9 = models.BookingRoomService(booking_room=booking_room_4, service=service1, qty=4)
    booking_room_service_10 = models.BookingRoomService(booking_room=booking_room_4, service=service2, qty=1)

    booking_room_service_11 = models.BookingRoomService(booking_room=booking_room_5, service=service5, qty=5)
    booking_room_service_12 = models.BookingRoomService(booking_room=booking_room_5, service=service2, qty=2)
    booking_room_service_13 = models.BookingRoomService(booking_room=booking_room_5, service=service3, qty=1)

    booking_room_service_14 = models.BookingRoomService(booking_room=booking_room_10, service=service4, qty=3)
    booking_room_service_15 = models.BookingRoomService(booking_room=booking_room_10, service=service5, qty=2)
    booking_room_service_16 = models.BookingRoomService(booking_room=booking_room_10, service=service6, qty=1)

    booking_room_service_17 = models.BookingRoomService(booking_room=booking_room_7, service=service1, qty=2)
    booking_room_service_18 = models.BookingRoomService(booking_room=booking_room_7, service=service2, qty=1)
    booking_room_service_19 = models.BookingRoomService(booking_room=booking_room_7, service=service3, qty=3)

    booking_room_service_20 = models.BookingRoomService(booking_room=booking_room_8, service=service4, qty=2)
    booking_room_service_21 = models.BookingRoomService(booking_room=booking_room_8, service=service5, qty=1)
    booking_room_service_22 = models.BookingRoomService(booking_room=booking_room_8, service=service6, qty=3)

    booking_room_service_23 = models.BookingRoomService(booking_room=booking_room_9, service=service1, qty=1)
    booking_room_service_24 = models.BookingRoomService(booking_room=booking_room_9, service=service2, qty=2)
    booking_room_service_25 = models.BookingRoomService(booking_room=booking_room_9, service=service3, qty=2)

    db.session.add(booking_room_service_14)
    db.session.add(booking_room_service_15)
    db.session.add(booking_room_service_16)
    db.session.add(booking_room_service_17)
    db.session.add(booking_room_service_18)
    db.session.add(booking_room_service_19)
    db.session.add(booking_room_service_20)
    db.session.add(booking_room_service_21)
    db.session.add(booking_room_service_22)
    db.session.add(booking_room_service_23)
    db.session.add(booking_room_service_24)
    db.session.add(booking_room_service_25)

    db.session.add(booking_room_service_1)
    db.session.add(booking_room_service_2)
    db.session.add(booking_room_service_3)
    db.session.add(booking_room_service_4)
    db.session.add(booking_room_service_5)
    db.session.add(booking_room_service_6)
    db.session.add(booking_room_service_7)
    db.session.add(booking_room_service_8)
    db.session.add(booking_room_service_9)
    db.session.add(booking_room_service_10)
    db.session.add(booking_room_service_11)
    db.session.add(booking_room_service_12)
    db.session.add(booking_room_service_13)

    # Create 2 additional charges
    # additional_charge1 = models.AdditionalCharge(booking_room=booking_room_1, created_date=datetime(2024, 5, 10), description='Phí làm hỏng bàn', amount=500000)
    # additional_charge2 = models.AdditionalCharge(booking=booking1, created_date=datetime(2024, 5, 10), description='Phí làm hỏng giường', amount=2000000)
    # additional_charge2 = models.AdditionalCharge(booking=booking2, created_date=datetime(2024, 5, 10), description='Dinner', amount=200)
    # db.session.add(additional_charge1)
    # db.session.add(additional_charge2)

    guest_type1 = models.GuestType(name='Khách nội địa', description='Khách nội địa')
    guest_type2 = models.GuestType(name='Khách nước ngoài', description='Khách nước ngoài')
    db.session.add(guest_type1)
    db.session.add(guest_type2)

     
    guest1 = models.Guest(first_name='John', last_name='Conner', sex=models.Sex.Men, identification_number='123456789', guest_type=guest_type1, booking_room=booking_room_1)
    guest2 = models.Guest(first_name='Craig', last_name='Haley', sex=models.Sex.Men, identification_number='123456789', guest_type=guest_type1, booking_room=booking_room_1)
    guest3 = models.Guest(first_name='Simone', last_name='Wolf', sex=models.Sex.Women, identification_number='987654321', guest_type=guest_type1, booking_room=booking_room_1)
    guest4 = models.Guest(first_name='Christina', last_name='Shea', sex=models.Sex.Women, identification_number='456789123', guest_type=guest_type1, booking_room=booking_room_2)
    guest5 = models.Guest(first_name='Aileen', last_name='Gomez', sex=models.Sex.Women, identification_number='321654987', guest_type=guest_type1, booking_room=booking_room_2)

    db.session.add(guest1)
    db.session.add(guest2)
    db.session.add(guest3)
    db.session.add(guest4)
    db.session.add(guest5)

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