__author__ = 'zend'

from flask import Flask, render_template


app = Flask(__name__)
app.config.from_object('config')

from views import *

if __name__ == '__main__':
    app.run()
