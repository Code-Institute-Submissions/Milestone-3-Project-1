import os
import json
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", page_title="About")


@app.route('/signup')
def signup():
    return render_template("signup.html", page_title="Sign Up")


@app.route('/login')
def login():
    return render_template("login.html", page_title="Login")


@app.route('/workspace')
def workspace():
    return render_template("workspace.html", page_title="Workspace", user= "DAVE CAFFREY")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
