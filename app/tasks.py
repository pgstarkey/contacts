from celery import Celery
from flask import Flask
from time import sleep
import requests
import random
from .models import Contact
from .contacts import delete_contact


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
    while not stop_after or count <= stop_after:
        randval = str(random.randint(0, 1000))
        payload = {'firstname': 'first' + randval, 'surname': 'surname' + randval,
                   'emails': [randval + '@test.com', randval + '@test.co.uk']}
        r = requests.put('http://localhost:5000/contacts/' + randval, json=payload)
        count += 1
        sleep(15)

@celery.task()
def remove_old_contacts(stop_after=None):
    count = 0
    while not stop_after or count <= stop_after:
        all_contacts = Contact.query.all()
        sleep(60)
        for contact in all_contacts:
            delete_contact(contact.usewrname)
