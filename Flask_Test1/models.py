from datetime import datetime
from Flask_Test1 import db, login_manager
from flask_login import UserMixin

#login management

@login_manager.user_loader #tells login manager that this is the user loader function
def load_user(user_id):
    return User.query.get(int(user_id))


#this is basically creating the tables for the database

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) # the backref allows the posts to reference the users without needing a column in the posts table

    def __repr__(self): #this is what gets printed out for the User
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self): #this is what gets printed out for the Post
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