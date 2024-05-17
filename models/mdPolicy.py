from app import db
import models.myEnum as MyEnum


class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text)
    value = db.Column(db.Float)
    value_type = db.Column(db.Enum(MyEnum.PolicyValueType))

    
    def __str__(self) -> str:
        return self.name
