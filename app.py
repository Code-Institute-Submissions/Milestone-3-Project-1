import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# from the flask module use Flask class and render template function
from flask import Flask, render_template, request, flash, session, redirect, url_for
from functools import wraps

from wtforms import Form, BooleanField, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import InputRequired
from passlib.hash import pbkdf2_sha256
# instantiate Flask class and ref with ap
from os import path
if path.exists("env.py"):
    import env
# Configure Flask App
app = Flask(__name__)
app.secret_key = "some_secret"
app.config["MONGO_DBNAME"] = 'milestone'
MONGO_URI = os.environ.get("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)

# Set up of  Custom Signupform Class inheriting from Form


class SignUpForm(Form):
    name = StringField('Name', [validators.Length(
        min=5, max=50), validators.InputRequired()])
    username = StringField('Username', [validators.Length(
        min=4, max=25), validators.InputRequired()])
    email = StringField('Email Address', [validators.Length(
        min=6, max=35), validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo(
            'confirm', message='The Passwords must match to proceed')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.InputRequired()])


# Set up for Custom Login form


class LoginForm(Form):

    username = StringField('Username', [validators.Length(
        min=4, max=25), validators.InputRequired()])

    password = PasswordField('Password', [validators.InputRequired()])

# Set up for Custom Add Blog Form


class AddBlogForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=300)])
    body = TextAreaField('Body', [validators.Length(min=5, max=2000)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    date = StringField('Date: dd/mm/yyyy format')
    img_src = StringField('Image URL', [validators.Length(min=5, max=500)])

# Set up for Custom form to edit blogs


class EditBlogForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=300)])
    body = TextAreaField('Body', [validators.Length(min=5, max=2000)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    date = StringField('Date: dd/mm/yyyy format')
    img_src = StringField('Image URL', [validators.Length(min=5, max=300)])


# first template to index/home page


@app.route('/')
def index():
    return render_template("index.html", page_title="Home")


# template for signup page


@app.route('/signup', methods=["GET", "POST"])
def signup():
    users = mongo.db.users
    form = SignUpForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = pbkdf2_sha256.hash(str(form.password.data))
        user_signup_form = {
            'name': name,
            'email': email,
            'user_name': username,
            'password': password
        }
        users.insert_one(user_signup_form)
        
        return redirect(url_for('login'))
   
    return render_template("signup.html", page_title="Sign Up", form=form)


# template for login page


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    username = form.username.data
    password_input = form.password.data
    result = {}
    if request.method == "POST" and form.validate():
        result = mongo.db.users.find_one({"user_name": username})
        f_pass = result["password"]
        if pbkdf2_sha256.verify(password_input, f_pass):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('blogs'))
        else:
            flash("FAILED TO LOG YOU IN TRY AGAIN", 'success')

    return render_template("login.html", page_title="login", form=form)


# route to all blogs


@app.route('/blogs')
def blogs():
    return render_template("blogs.html", blogs=mongo.db.blog.find())


# route to the individual blogs by their ID


@app.route('/blog/<blog_id>')
def workspace_blog(blog_id):
    return render_template("blog.html", 
                           blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


# function to insure that only registered/logged in users can edit/delete blogs


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_function


# Route to log users out


@app.route('/logout')
@login_required
def logout():
    session.clear()

    return redirect(url_for('login'))


# route to edit page where users can add a blog/click into a blog for editing


@app.route('/edit')
@login_required
def edit():
    return render_template("edit.html", blogs=mongo.db.blog.find())


# The route to edit/delete an individual blog from the site


@app.route('/edit_blog/<blog_id>', methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    blogs = mongo.db.blog.find_one({'_id': ObjectId(blog_id)})
    form = EditBlogForm(request.form)
    form.title.data = blogs["title"]
    form.body.data = blogs["body"]
    form.username.data = blogs["user_name"]
    form.date.data = blogs["date"]
    form.img_src.data = blogs["img_src"]
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']
        username = request.form['username']
        date = request.form['date']
        img_src = request.form['img_src']
        mongo.db.blog.update({'_id': ObjectId(blog_id)},
        {
            'title': title,
            'body': body,
            'user_name': username,
            'date': date,
            'img_src': img_src
        })

        flash('Blog Updated', 'sucess')
        return redirect(url_for('blogs'))

    return render_template("edit_blog.html",
                           form=form, blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


# Route to delete blog by its ID


@app.route('/delete_blog/<blog_id>', methods=["GET", "POST"])
@login_required
def delete_blog(blog_id):
    mongo.db.blog.remove({'_id': ObjectId(blog_id)})
    return redirect(url_for('blogs'))


# Route to add a blog


@app.route('/add_blog', methods=["GET", "POST"])
@login_required
def add_blog():
    blogs = mongo.db.blog
    form = AddBlogForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data
        username = form.username.data
        date = form.date.data
        img_src = form.img_src.data
        add_blog = {'title': title, 'body': body,
                    'user_name': username, 'date': date, 'img_src': img_src}
        blogs.insert_one(add_blog)
        flash('Blog Added', 'sucess')
        return redirect(url_for('edit'))

    return render_template('add_blog.html', form=form)


# call to Flask Class run function passing in
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")))
