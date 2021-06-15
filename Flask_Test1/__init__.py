from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#secret key helps protect against XSRF attacks
app.config['SECRET_KEY'] = '135d1e15e1d736b415725bd01a0aafed'

#tell sqlalchemy where the database file is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#initialize the database
db = SQLAlchemy(app)

#password hashing lad
bcrypt = Bcrypt(app)

#login manager login manager manages login
login_manager = LoginManager(app)

#needed for redir on accessing page you need to login for
login_manager.login_view = 'login'

#make the "please login" message pretty
login_manager.login_message_category = 'info'

#this is done here to prevent circular imports
from Flask_Test1 import routes