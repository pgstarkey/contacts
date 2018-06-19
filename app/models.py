from flask_sqlalchemy import SQLAlchemy

from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db = SQLAlchemy(app)


class Contact(db.Model):
    __tablename__ = 'contacts'
    username = db.Column(db.String, primary_key=True)
    firstname = db.Column(db.String, primary_key=True)
    surname = db.Column(db.String, primary_key=True)
    emails = db.relationship('Email', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Contact %r>' % self.username


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    username = db.Column(db.String, db.ForeignKey('contacts.username'))

    def __repr__(self):
        return self.email
