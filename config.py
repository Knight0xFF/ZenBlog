__author__ = 'zend'

DEBUG = True

# configuration mysql
SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s/%s" % ('root', 'xiaobai', '127.0.0.1', 'zen_blog')

SECRET_KEY = 'A0Zr98j/3yX R~XHHsdfdsfsdf'
USERNAME = 'admin'
PASSWORD = 'admin'


RECAPTCHA_PUBLIC_KEY = '6LeJTt8SAAAAACuSjRrt3a2jgGX-xQBREEAXw9Rs'
RECAPTCHA_PRIVATE_KEY = '6LeJTt8SAAAAACjz_N65vlf9yuscktZZjOIEISFA'