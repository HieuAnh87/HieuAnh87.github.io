# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import random
# import string
# from app import db
# #
# #
# class Urls(db.Model):
#     __tablename__ = 'urls'
#     id_ = db.Column(db.Integer, primary_key=True)
#     long = db.Column(db.String(500))
#     short = db.Column(db.String(10), unique=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id_user'), nullable=False)
#     user = db.relationship("Users", backref=db.backref("Urls", lazy=True))
#
#     def __init__(self, long, short):
#         self.long = long
#         self.short = short
#
# class Users(db.Model):
#     __tablename__ = 'users'
#     id_user = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100))
#     url = db.relationship("Urls", backref="Users")
#
#     def __init__(self, name, email, password):
#         self.name = name
#         self.email = email
#         self.password = password
# #
# def shorten_url():
#     letters = string.ascii_lowercase + string.ascii_uppercase
#     while True:
#         rand_letters = random.choices(letters, k=5)
#         rand_letters = "".join(rand_letters)
#         short_url = Urls.query.filter_by(short=rand_letters).first()
#         if not short_url:
#             return rand_letters
