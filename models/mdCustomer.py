from app import db
import models.myEnum as MyEnum


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(MyEnum.Sex))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    
    def __str__(self) -> str:
        return self.first_name