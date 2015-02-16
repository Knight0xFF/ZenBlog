__author__ = 'Zend'

from flask import Flask

app = Flask(__name__, static_folder=None)
app.config.from_object('config')

from app.index.views import index
app.register_blueprint(index, url_prefix="/")
from app.admin.views import admin
app.register_blueprint(admin, url_prefix="/admin")