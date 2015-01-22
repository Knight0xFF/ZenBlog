__author__ = 'Zend'

from flask.ext.script import Server, Manager, prompt_bool
from run import app
from models import db

manager = Manager(app)
manager.add_command("runserver", Server('0.0.0.0', port=5000))

if __name__ == "__main__":
    manager.run()