from .models import Contact, db, Email
from json import dumps, loads
from sqlalchemy import inspect
from celery import Celery
from flask import Flask
from time import sleep
import requests
import random


contact_mapper = inspect(Contact)
email_mapper = inspect(Email)


def get_all_contacts():
    all_contacts = Contact.query.all()
    contact_list = []
    for contact in all_contacts:
        attributes = []
        for c in contact_mapper.attrs:
            attribute = getattr(contact, c.key)
            attributes.append(
                [c.key, [str(entry) for entry in attribute] if isinstance(attribute, list) else attribute])
        contact_list.append(dict(attributes))
    return dumps(contact_list)


def get_all_emails():
    all_emails = Email.query.all()
    email_list = []
    for email in all_emails:
        email_list.append(dict([(e.key, str(getattr(email, e.key))) for e in email_mapper.attrs]))
    return dumps(email_list)


def get_contact(user_ref):
    contact = Contact.query.filter_by(username=user_ref).first()
    if not contact:
        user_email = Email.query.filter_by(email=user_ref).first()
        contact = Contact.query.filter_by(username=user_email.username).first()
        if not contact:
            return dumps({'error': 'username %s not found' % user_ref}), 404
    attributes = []
    for c in contact_mapper.attrs:
        attribute = getattr(contact, c.key)
        attributes.append(
            [c.key, [str(entry) for entry in attribute] if isinstance(attribute, list) else attribute])
    return dumps(dict(attributes))


def create_contact(username, request):
    contact = Contact(username=username)
    request_body = request.form if request.form else loads(request.data)
    for key in request_body:
        try:
            setattr(contact, key, request_body[key])
        except AttributeError:
            contact.emails = [Email(email=e, username=username) for e in request_body[key]]
    db.session.add(contact)
    db.session.commit()
    return '', 201


def delete_contact(username):
    Contact.query.filter_by(username=username).delete()
    Email.query.filter_by(username=username).delete()
    db.session.commit()
    return '', 204


def update_contact(username, request):
    contact = Contact.query.filter_by(username=username).first()
    request_body = request.form if request.form else loads(request.data)
    for key in request_body:
        try:
            setattr(contact, key, request_body[key])
        except AttributeError:
            new_emails = set(e for e in request_body[key])
            current_emails = set(str(e) for e in Email.query.filter_by(username=username))
            for email in [e for e in new_emails if e not in current_emails]:
                contact.emails.append(Email(email=email, username=username))
            for email in [e for e in current_emails if e not in new_emails]:
                contact.emails.remove(email)
    db.session.commit()
    return '', 204


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['CELERY_broker_url']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = Flask(__name__)
flask_app.config.update(
    CELERY_broker_url='redis://localhost:6379',
    result_backend='redis://localhost:6379'
)
celery = make_celery(flask_app)


@celery.task()
def create_random_contact(stop_after=None):
    count = 0
    while not stop_after or count < stop_after:
        randval = str(random.randint(0, 1000))
        payload = {'firstname': 'first' + randval, 'surname': 'surname' + randval,
                   'emails': [randval + '@test.com', randval + '@test.co.uk']}
        r = requests.put('http://localhost:5000/contacts/' + randval, json=payload)
        count += 1
        sleep(15)


#@celery.task()
def remove_old_contacts(stop_after=None):
    count = 0
    while not stop_after or count < stop_after:
        all_contacts = Contact.query.all()
        sleep(60)
        for contact in all_contacts:
            delete_contact(contact.username)
        count += 1
