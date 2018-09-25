from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# inorder to connect with mysql db
import mysql.connector as mysqlconnector
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)


# random key for security purpose
app.config['SECRET_KEY'] = '1e9f1b48c53261cf4563d4ea5670657b'

# mysqlconnector is necessary it provides a medium of communication between sqlalchemy and mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://dbuser:password@localhost/flask_blog_db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# inorder to redirect to login page if the page to access requres user tobe logged in
login_manager.login_view = 'login'

from flask_blog import routes