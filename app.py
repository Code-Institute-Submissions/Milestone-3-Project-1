import pymongo
import os
import json
from datetime import datetime
# from the flask module use Flask class and render template function
from flask import Flask, render_template, request, flash, session
# instantiate Flask class and ref with ap
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.secret_key = "some_secret"


MONGODB_URI = os.environ.get("MONGO_URI")
DBS_NAME = "milestone"
COLLECTION_NAME = "blog"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("CONNECTED TO MONGO DATABASE")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("WARNING NOT CONNECTED TO DATABASE")


date_time = datetime.now().strftime("%Y:%M:%D:%H:%M:%S")


conn = mongo_connect(MONGODB_URI)
coll = conn[DBS_NAME][COLLECTION_NAME]


# first template to index/home page
@app.route('/')
def index():
    return render_template("index.html", page_title="Home")

# template for signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        flash("Thanks {}, we have recieved your message".format(
            request.form["fname"]))
    return render_template("signup.html", page_title="Sign Up")

# template for login page
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        flash("{}, you are logged into the system".format(
            request.form["user_name"]))

    return render_template("login.html", page_title="login")


@app.route('/workspace')
def workspace():
    data = []
    try:
        data = coll.find()
        print(data)
    except:
        print("Errrorrrrrr")

    if not data:
        print("")
        print("NO RESULTS FOUND")

    return render_template("workspace.html", page_title="Workspace", user="DAVE CAFFREY",
                           list_of_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], blogs=data)


@app.route('/workspace/<blog_title>/', methods=["GET", "POST"])
def workspace_blog(blog_title):
    blog = {}
    blog = coll.find_one({'title': blog_title})
     
    return render_template("blog.html", blog=blog)


# call to Flask Class run function passing in
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # remove debug = True from production code
            debug=True)
