from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets 
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    recs = db.relationship('Recs', backref = 'owner', lazy = True)

    def __init__(self, name, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.name = name
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)




class Recs(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150), unique = True)
    category = db.Column(db.String(150))
    location = db.Column(db.String(300))
    url = db.Column(db.String(200))
    phone = db.Column(db.String(150))
    image_url = db.Column(db.String(500))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, category, location, url, phone, image_url, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.category = category
        self.location = location
        self.url = url
        self.phone = phone
        self.image_url = image_url
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())

# detailing which fields to pull out recs and send to API call
class RecsSchema(ma.Schema):
    class Meta:  
        fields = ['id','name','category','location','url','phone', 'image_url', 'user_token']

# take a python class iterates through fields and adds to a dictionary

rec_schema = RecsSchema()
recs_schema = RecsSchema(many=True)



