from app import db
import models.myEnum as MyEnum

class GuestType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))

    def __str__(self) -> str:
        return self.name