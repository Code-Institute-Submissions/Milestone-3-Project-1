import os
import json
# from the flask module use Flask class and render template function
from flask import Flask, render_template
#instantiate Flask class and ref with app 
app = Flask(__name__)

# first template to index/home page
@app.route('/')
def index():
    return render_template("index.html", page_title="Home")

# template for signup page
@app.route('/signup')
def signup():
    return render_template("signup.html", page_title="Sign Up")

# template for login page 
@app.route('/login')
def login():
    return render_template("login.html", page_title="Login")


@app.route('/workspace')
def workspace():
    return render_template("workspace.html", page_title="Workspace", user="DAVE CAFFREY")

# call to Flask Class run function passing in 
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            #remove debug = True from production code
            debug=True)
