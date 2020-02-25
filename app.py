import os
import json
from datetime import datetime
# from the flask module use Flask class and render template function
from flask import Flask, render_template, request, flash, session
# instantiate Flask class and ref with app 
app = Flask(__name__)
app.secret_key = "some_secret" 

date_time = datetime.now().strftime("%Y:%M:%D:%H:%M:%S")

# first template to index/home page
@app.route('/')
def index():
    return render_template("index.html", page_title="Home")

# template for signup page
@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        flash("Thanks {}, we have recieved your message".format(request.form["fname"]))
    return render_template("signup.html", page_title="Sign Up")

# template for login page 
@app.route('/login', methods=["GET", "POST"])
def login():
    
    if request.method == "POST":  
        flash("{}, you are logged into the system".format(request.form["user_name"]))
  
    return render_template("login.html", page_title="login" )


@app.route('/workspace')
def workspace():
    data = []
    with open("data/blogs.json", "r") as json_data:
        data = json.load(json_data)
    return render_template("workspace.html", page_title="Workspace", user="DAVE CAFFREY", 
                           list_of_numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], blogs=data)


@app.route('/workspace/<blog_title>', methods=["GET", "POST"])
def workspace_blog(blog_title):
    blog = {}

    with open("data/blogs.json", "r") as json_data:
        data = json.load(json_data)
        for obj in data:
            if obj["url"] == blog_title:
                blog = obj
    
    return render_template("blog.html", blog=blog)


# call to Flask Class run function passing in 
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            #remove debug = True from production code
            debug=True)




