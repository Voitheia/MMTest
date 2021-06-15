from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#secret key helps protect against XSRF attacks
app.config['SECRET_KEY'] = '135d1e15e1d736b415725bd01a0aafed'

#tell sqlalchemy where the database file is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#this is done here to prevent circular imports
from Flask_Test1 import routes