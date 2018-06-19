from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app import routes
