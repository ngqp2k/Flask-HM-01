from app import db


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    price = db.Column(db.DECIMAL)
    
    def __str__(self) -> str:
        return self.name
