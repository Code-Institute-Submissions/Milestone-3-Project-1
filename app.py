import pprint
import pymongo
import os
import json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
# from the flask module use Flask class and render template function
from flask import Flask, render_template, request, flash, session, redirect, url_for, logging,request
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, TextAreaField, PasswordField, validators
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
    name = StringField('Name', [validators.Length(min=5, max=50), validators.InputRequired()])
    username = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.InputRequired(), validators.Email()])
    password = PasswordField('Password', [
        validators.InputRequired(),
        validators.EqualTo('confirm', message='The Passwords must match to proceed')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.InputRequired()])


class LoginForm(Form):
   
    username = StringField('Username', [validators.Length(min=4, max=25), validators.InputRequired()])
   
    password = PasswordField('Password', [validators.InputRequired()])
   

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
        pprint.pprint(list(mongo.db.users.find_one({"user_name":username})))
        result = mongo.db.users.find_one({"user_name":username})
        app.logger.info(result)

    if pbkdf2_sha256.verify(password_input, result["password"]):
        """password = user["password"]
        app.logger.info("App gets this far")
        
        if pbkdf2_sha256.verify(password_input, password):
            app.logger.info("Pass word match")
            flash("Thanks {}, You have logged in", 'success')
        else:
            app.logger.info("PASS WORD DO NOT MATCH") 
    else:
        app.logger.info("PASSWORD WRONG")
        flash("ERRRORRR{}, we have recieved your message", 'success')"""
    return render_template("login.html", page_title="login", form=form)


@app.route('/blogs')
def blogs():
    return render_template("blogs.html", blogs=mongo.db.blog.find())


@app.route('/blog/<blog_id>')
def workspace_blog(blog_id):
    return render_template("blog.html", blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


@app.route('/edit')
def edit():
    return render_template("edit.html", blogs=mongo.db.blog.find())


# call to Flask Class run function passing in
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # remove debug = True from production code
            debug=True)


