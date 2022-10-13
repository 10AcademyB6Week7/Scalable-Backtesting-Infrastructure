from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class User(db.Model):
    __tablename__ = "user_acc"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    first_name = db.Column(db.String(20), unique=False)
    last_name = db.Column(db.String(20), unique=False)
    password = db.Column(db.Text, nullable=False)
    user_role=db.Column(db.String(10),nullable=False)
