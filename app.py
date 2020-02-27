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
from passlib.hash import sha256_crypt
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

#DBS_NAME = "milestone"
#COLLECTION_NAME_BLOG = "blog"
#COLLECTION_NAME_USERS = "user"
"""
def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("CONNECTED TO MONGO DATABASE" + str(conn))
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("WARNING NOT CONNECTED TO DATABASE")


date_time = datetime.now().strftime("%Y:%M:%D:%H:%M:%S")


conn_blog = mongo_connect(MONGODB_URI)
conn_users = mongo_connect(MONGODB_URI)
coll_blog = conn_blog[DBS_NAME][COLLECTION_NAME_BLOG]
coll_users = conn_users[DBS_NAME][COLLECTION_NAME_USERS]
"""

class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Length(min=5, max=50), validators.DataRequired()])
    username = StringField('Username', [validators.Length(min=4, max=25), validators.DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=35), validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='The Passwords must match to proceed')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])


# first template to index/home page
@app.route('/')
def index():
    return render_template("index.html", page_title="Home")

# template for signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        user = {}
        name = form.name.data 
        username = form.username.data 
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        user = {"Name": name,"Username": username,"email": email,
        "password": password}
        mongo.db.blog.insert_one(user)
        flash("Thanks {}, we have recieved your message", 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", page_title="Sign Up", form=form)

# template for login page
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        flash("{}, you are logged into the system".format(
            request.form["user_name"]))

    return render_template("login.html", page_title="login")


@app.route('/workspace')
def workspace():
    """
    data = []
    try:
        data = coll_blog.find()
        print(data)
    except:
        print("Errrorrrrrr")

    if not data:
        print("")
        print("NO RESULTS FOUND")

    """

    return render_template("workspace.html", blogs=mongo.db.blog.find())


@app.route('/blog/<blog_id>')
def workspace_blog(blog_id):
    return render_template("blog.html", blogs=mongo.db.blog.find({'_id': ObjectId(blog_id)}))


# call to Flask Class run function passing in
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # remove debug = True from production code
            debug=True)


