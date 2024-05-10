from app import db
import models.myEnum as MyEnum


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_no = db.Column(db.String(50))  
    image = db.Column(db.String(255))
    description = db.Column(db.Text)
    room_type_id = db.Column(db.Integer, db.ForeignKey('room_type.id'))
    room_type = db.relationship('RoomType', backref=db.backref('room', lazy=True))
    status = db.Column(db.Enum(MyEnum.RoomStatus))
    
    def __str__(self) -> str:
        return self.room_no