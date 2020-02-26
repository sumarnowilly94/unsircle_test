from datetime import datetime
from flask_restful import fields
from blueprints import db

### USERS ###
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    response_fields = {
        "id": fields.Integer,
        "email": fields.String,
        "password": fields.String,
        "created_at": fields.DateTime
    }

    ### JWT PAYLOAD ###
    jwt_claim_fields = {
        "id": fields.Integer,
        "email": fields.String
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return "<Users %r>" % self.id
