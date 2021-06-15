from flask import render_template, url_for, flash, redirect, request
from Flask_Test1 import app, db, bcrypt
from Flask_Test1.forms import RegistrationForm, LoginForm
from Flask_Test1.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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

#registration page route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home')) #if the user is logged in, redir to home
    form = RegistrationForm() #specify which form to user
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #this hashes the user's password and converts it to utf-8
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #create the user for the db
        db.session.add(user) #stage the user for the db
        db.session.commit() #commit new user to db
        flash(f'Your account has been created! Please login', 'success')
        return redirect(url_for('login')) #redir the user to the login page
    return render_template('register.html', title='Register', form=form)

#login page route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home')) #if the user is logged in, redir to home
    form = LoginForm() #specify which form to user
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #check that the user exists, using email because that's what the user uses to log in
        if user and bcrypt.check_password_hash(user.password, form.password.data): #if the user exists and the password is correct
            login_user(user, remember=form.remember.data) #log the user in, and if the user checked the remeber box, remember the user
            next_page = request.args.get('next') #check if the next argument exists (i.e. user tried to go somewhere they needed to login to see)
            return redirect(next_page) if next_page else redirect(url_for('home')) #redir the user to the next_page arg if it exists, if not send them to home page
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger') #display error message
    return render_template('login.html', title='Login', form=form)

#logout route
@app.route('/logout')
def logout():
    logout_user() #logout user
    return redirect(url_for('home')) #redir the user to the home page

#account page route
@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')