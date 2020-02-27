import pymongo
import os
from os import path
if path.exists("env.py"):
    import env

MONGODB_URI = os.environ.get("MONGO_URI")
DBS_NAME = "milestone"
COLLECTION_NAME_BLOG = "blog"
COLLECTION_NAME_USERS = "users"


def mongo_connect(url):
    try:
        conn = pymongo.MongoClient(url)
        print("mongo is connected")
        return conn
    except pymongo.errors.ConnectionFailure as e:
        print("could not connect" + e)

def show_menu():
    print("")
    print("1. Add a record")
    print("2. Find a record by name")
    print("3. Edit a record")
    print("4. Delete a record")
    print("5. Exit")

    option = input("Enter option: ")
    return option


def get_record():
    print("")
    user_name = input("Enter the User name")
    try:
        doc = coll.find_one({'user_name': user_name})
        print(doc)
    except:
        print("Errrorrrrrr")

    if not doc:
        print("")
        print("NO RESULTS FOUND")

def add_record():
    print("")
    title = input("Enter title of Blog > ")
    body = input("Enter the main body of the blog > ")
    user_name = input("Enter the Username for the Blog > ")
    date = input("Enter the Date in dd/mm/yyyy + timzone ie GMT > ")
    image_src = input("Enter the URL for your image > ")

    new_record = {'title': title,'body': body,'user_name': user_name,'date': date, 'image_src': image_src}

    try:
        coll_blog.insert(new_record)
        print("")
        print("Record Inserted")
    except:
        print("Error inserting record")


def find_record():
    doc = get_record()
    if doc:
        print("")
        for k, v in doc.items:
            if k != "_id":
                print(k + ":" + v)

def main_loop():
    while True:
        option = show_menu()
        if option == "1":
            add_record()
        elif option == "2":
            find_record()
        elif option == "3":
            print("You have selected option 3")
        elif option == "4":
            print("You have selected option 4")
        elif option == "5":
            conn.close()
            break
        else:
            print("Invalid option")
        print("")


conn = mongo_connect(MONGODB_URI)
coll_blog = conn[DBS_NAME][COLLECTION_NAME_BLOG]

main_loop()







#conn = mongo_connect(MONGODB_URI)

#coll = conn[DBS_NAME][COLLECTION_NAME]

#new_doc = {'title':'Tesla crashes again','body':'Share price plummets','user_name':'DuneMan','date':'Tue Feb 25 2020 17:00:00 GMT','img_src':'www.facebook.com'}
#coll.insert(new_doc)
#coll.update_one({'user_name':'DuneMan'},{'$set':{'date':'Tue Feb 26 2020 13:00:00 GMT'}})
#documents = coll.find()

#for doc in documents:
    #print(doc)


