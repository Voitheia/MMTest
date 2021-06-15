from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

#secret key helps protect against XSRF attacks
app.config['SECRET_KEY'] = '135d1e15e1d736b415725bd01a0aafed'

#tell sqlalchemy where the database file is
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"

#--------------------info about database stuff with python--------------------#
#
#run python
#from <filename> import db (ex: from Flask_Test1 import db)
#from <filename> import User, Post (ex: from Flask_Test1 import User, Post)
#-these imports allow us to use the classes and db on the python command line
#db.create_all()
#-creates all the tables needed for the db
#user_1 = User(username='bob', email='bob@gmail.com', password='password')
#-this creates a user variable
#db.session.add(user_1)
#-this adds the user we created to the "stack" that is waiting to be committed to the db
#user_2 = User(username='joe', email='joe@gmail.com', password='password')
#db.session.add(user_2)
#db.session.commit()
#-commits the users we added to the "stack" to the db
#User.query.all()
#-querys the database for all users
#User.query.first()
#-gets the first user
#User.query.filter_by(username='bob').all()
#-querys the database for all users with username of 'bob'
#user = User.query.filter_by(username='bob').first()
#-puts the bob user into a variable of "user"
#user
#-will print out the information of the user in the user variable
#user.id
#-will print out the id of the user in the user variable
#user = User.query.get(2)
#-sets the user variable to the user of id 2
#post_1 = Post(title='thingy', content='this has stuff in it yeee', user_id=user.id)
#-makes a new post variable with information in it that has an author of the user variable
#db.drop_all()
#-drops all tables

#this posts variable is a list of dictionaries, used as dummy data for blog posts
#basically just a replacement for a database call
posts = [
    {
        'author': 'author1',
        'title': 'title1',
        'content': 'first lul',
        'date_posted': '5/10/21'
    },
    {
        'author': 'author2',
        'title': 'title2',
        'content': '2nd eeeeeeeee',
        'date_posted': '5/11/21'
    }
]

#root route, basically the homepage
#having two routes means that flask will put the same html on both of those pages
#by using the render_template, we are able to pass an html document to flask for it to put on the web server
#by passing posts=posts to render_template, we can give the template the data from the posts variable
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title='Home')

#about page route
@app.route('/about')
def about():
    return render_template('about.html', title='About')

#game page route, was going to have a simple javascript game, but i couldn't get it to work so it doesn't do anything rn
@app.route('/game')
def game():
    return render_template('game_test.html', title='Game Test')

#registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

#login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Logged in as {form.email.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

#allows us to run the web server with python so we don't have to type stuff in the terminal
#also turns on debug mode so that we can make changes while the web server is running
if __name__ == '__main__':
    app.run(debug=True)
#an alternative to doing this is in the terminal running the following commands:
# $env:FLASK_APP = "<.py name>" (in this case Flask_Test.py)
# $env:FLASK_DEBUG = 1 (turns debug mode on)