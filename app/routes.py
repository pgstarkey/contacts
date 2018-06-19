from flask import request
from json import loads
from app import app
from .contacts import get_all_contacts, get_contact, delete_contact, create_contact, update_contact, get_all_emails

@app.route('/contacts', methods=['GET'])
def contacts():
    return get_all_contacts()

@app.route('/contacts/<username>', methods=['GET', 'DELETE', 'PUT', 'POST'])
def contact_by_name(username):
    if request.method == 'GET':
        return get_contact(username)
    elif request.method == 'DELETE':
        return delete_contact(username)
    elif request.method == 'PUT':
        return create_contact(username, request)
    else:
        return update_contact(username, request)

@app.route('/emails', methods=['GET'])
def emails():
    return get_all_emails()
