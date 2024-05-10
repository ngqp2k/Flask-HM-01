from app import db


class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price_per_night = db.Column(db.Float)
    capacity = db.Column(db.Integer)
    bed_quantity = db.Column(db.Integer)
    
    def __str__(self) -> str:
        return self.name