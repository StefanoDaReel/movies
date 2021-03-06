from flask_login import UserMixin

from movies import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
