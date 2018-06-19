from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Contact(db.Model):
    username = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, primary_key=True)
    firstname = db.Column(db.String, primary_key=True)
    surname = db.Column(db.String, primary_key=True)

    def __repr__(self):
        return '<Contact %r>' % self.username
