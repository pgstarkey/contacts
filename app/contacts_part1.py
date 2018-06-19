from .models import Contact, db
from json import dumps, loads
from sqlalchemy import inspect


mapper = inspect(Contact)


def get_all_contacts():
    all_contacts = Contact.query.all()
    contact_list = []
    for contact in all_contacts:
        contact_list.append(dict([(c.key, getattr(contact, c.key)) for c in mapper.attrs]))
    return dumps(contact_list)


def get_contact(username):
    contact = Contact.query.filter_by(username=username).first()
    if contact:
        return dumps(dict([(c.key, getattr(contact, c.key)) for c in mapper.attrs]))
    else:
        return dumps({'error': 'username %s not found' % username}), 404


def create_contact(username, details):
    contact = Contact(username=username)
    detail_data = loads(details)
    for key in detail_data:
        setattr(contact, key, detail_data[key])
    db.session.add(contact)
    db.session.commit()
    return '', 201


def delete_contact(username):
    Contact.query.filter_by(username=username).delete()
    db.session.commit()
    return '', 204


def update_contact(username, details):
    contact = Contact.query.filter_by(username=username).first()
    detail_data = loads(details)
    for key in detail_data:
        setattr(contact, key, detail_data[key])
    db.session.commit()
    return '', 204
