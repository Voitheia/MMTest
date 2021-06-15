from flask import render_template, url_for, flash, redirect
from Flask_Test1 import app
from Flask_Test1.forms import RegistrationForm, LoginForm
from Flask_Test1.models import User, Post

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