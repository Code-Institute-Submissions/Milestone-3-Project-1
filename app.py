import pprint
import pymongo
import os
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
from datetime import datetime
# from the flask module use Flask class and render template function
from flask import Flask, render_template, request, flash, session, redirect, url_for, logging, request, g
from functools import wraps
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, TextAreaField, PasswordField, DateField, validators
from wtforms.validators import DataRequired
from passlib.hash import pbkdf2_sha256
# instantiate Flask class and ref with ap
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = "some_secret"
app.config["MONGO_DBNAME"] = 'milestone'
MONGO_URI = os.environ.get("MONGO_URI")
app.config["MONGO_URI"] = MONGO_URI

mongo = PyMongo(app)


class RegistrationForm(Form):
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


class LoginForm(Form):

    username = StringField('Username', [validators.Length(
        min=4, max=25), validators.InputRequired()])

    password = PasswordField('Password', [validators.InputRequired()])


class AddBlogForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=300)])
    body = TextAreaField('Body', [validators.Length(min=40)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    date = StringField('Date: dd/mm/yyyy format')
    img_src = StringField('Image URL', [validators.Length(min=5, max=500)])


class EditBlogForm(Form):
    title = StringField('Title', [validators.Length(min=5, max=300)])
    body = TextAreaField('Body', [validators.Length(min=40)])
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
    form = RegistrationForm(request.form)
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
        flash("Thanks {}, we have recieved your message", 'success')
        return redirect(url_for('login'))
    else:
        flash("Error")
    return render_template("signup.html", page_title="Sign Up", form=form)

# template for login page
@app.route('/login', methods=["GET", "POST"])
def login():
    users = mongo.db.users
    user = {}
    form = LoginForm(request.form)
    username = form.username.data
    password_input = form.password.data
    result = {}
    if request.method == "POST" and form.validate():
        app.logger.info("App gets this far")
        pprint.pprint(list(mongo.db.users.find_one({"user_name": username})))
        result = mongo.db.users.find_one({"user_name": username})
        f_pass = result["password"]
        app.logger.info(result)
        app.logger.info(f_pass)
        if pbkdf2_sha256.verify(password_input, f_pass):
            app.logger.info(True)
            session['logged_in'] = True
            session['username'] = username
            flash("Thanks {}, You have logged in", 'success')
            return redirect(url_for('blogs'))
        else:
            flash("FAILED TO LOG YOU IN TRY AGAIN", 'success')
    return render_template("login.html", page_title="login", form=form)


@app.route('/blogs')
def blogs():
    return render_template("blogs.html", blogs=mongo.db.blog.find())


@app.route('/blog/<blog_id>')
def workspace_blog(blog_id):
    return render_template("blog.html", blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login', next=request.url))
    return decorated_function


@app.route('/logout')
@login_required
def logout():
    session.clear()

    return redirect(url_for('login'))


@app.route('/edit')
@login_required
def edit():
    return render_template("edit.html", blogs=mongo.db.blog.find())


@app.route('/edit_blog/<blog_id>', methods=["GET", "POST"])
@login_required
def edit_blog(blog_id):
    blogs = mongo.db.blog.find_one({'_id': ObjectId(blog_id)})
    app.logger.info(blogs)
    form = EditBlogForm(request.form)
    form.title.data = blogs["title"]
    form.body.data = blogs["body"]
    form.username.data = blogs["user_name"]
    form.date.data = blogs["date"]
    form.img_src.data = blogs["img_src"]
    if request.method == 'POST' and form.validate():
        flash('Posted', 'success')
        title = request.form['title']
        body = request.form['body']
        username = request.form['username']
        date = request.form['date']
        img_src = request.form['img_src']
        app.logger.info(title)
        mongo.db.blog.update({'_id': ObjectId(blog_id)},
                     {
            'title': title,
            'body': body,
            'user_name': username,
            'date': date,
            'img_src': img_src
        })

        app.logger.info(blogs)
        flash('Blog Updated', 'sucess')
        return redirect(url_for('blogs'))

    return render_template("edit_blog.html", form=form, blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


@app.route('/add_blog', methods=["GET", "POST"])
@login_required
def add_blog():
    blogs = mongo.db.blog
    app.logger.info(blogs)
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
        app.logger.info(blogs)
        flash('Blog Added', 'sucess')
        return redirect(url_for('edit'))

    return render_template('add_blog.html', form=form)


# call to Flask Class run function passing in
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # remove debug = True from production code
            debug=True)
