from app import db
from werkzeug.security import generate_password_hash
import models.myEnum as MyEnum



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.Enum(MyEnum.Sex))
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