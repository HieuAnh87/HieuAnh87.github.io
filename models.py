from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random
import string
from app import db

class Urls(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(500))
    short = db.Column(db.String(10), unique=True)
    def __init__(self, long, short):
        self.long = long
        self.short = short


# class Users(db.Model):
#     id_ = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password


def shorten_url():
    letters = string.ascii_lowercase + string.ascii_uppercase
    while True:
        rand_letters = random.choices(letters, k=5)
        rand_letters = "".join(rand_letters)
        short_url = Urls.query.filter_by(short=rand_letters).first()
        if not short_url:
            return rand_letters
