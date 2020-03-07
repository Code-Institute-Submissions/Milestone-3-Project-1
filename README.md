# David Caffrey Milestone 3 Project The Daily Commute Blog Website
------------------------------------------------------------------------------------------------------------------------------------------
[The live site running on Heroku is here](https://milestone-3-project-dc.herokuapp.com/)

This is the project for the Data-Centric module of the Code Institute Full Stack Software Developer Course. It is a blog site that visitors can come to and see the blogs that have been posted. The emphasis of the site is on the Database operations that can be performed by visitors.

## The Daily Commute Blog
### User Stories
------------------------------------------------------------------------------------------------------------------------------------------

* As a new user I should be able
  * View all the blogs that have been posted
  * Unable to edit or delete blogs 
  * Sign-up/Register on the site 
  
* As an existing/registered user I should be able
  * Login to the site
  * View the blogs
  * Add a new blog
  * Edit an existing blog
  * Delete a blog
  * Logout from the site
  
## Technologies 
----------------------------------------------------------------------------------------------------------------------------------------
* HTML
* CSS
* Python
* Flask(web framework)
* MongoDB

## Database Schema
--------------------------------------------------------------------------------------------------------------------------------------
The noSql database MongoDB was used and from the inception of the project I wanted to have registered users who would be able to Create, Read, Update and Delete blogs from the DB so it was clear that two DB collections would be required. The first collection would be for users that would store: Name, Email Address, UserName, Password. The second collection would be for the blogs and would store: UserName, Title, Body(the body of text that is the blog), Date and the ImageURL associated with the blog. Both of these collections would also store the unique ID for Users and Blogs.



id|ObjectID
--|--------
name| Dave Caffrey
email| dave.caffrey@gmail.com
user_name| dcaffer
password | sdlfsdfhdslhdg


id| ObjectID
--| --------
title| The end of the world as we know it?
body| Some random info goes here
user_name| dcaffer
date| 02/03/2020
img_src| www.google.com



## Features
### Existing Features
--------------------------------------------------------------------------------------------------------------------------------------

* new users are able to views the blogs but are unable to add, edit or delete blogs
* new users can register/signup via signup form
 * the signup form provides validation by using wtform validators 
 * the signup form encrypts the password of the user by using the passlib modul
 
* registered users can login
 * the login is validated by wtforms validators
 * once logged in the link to logout becomes available
 * when logged in the link to edit blogs becomes available

* when a registered user navigates to the edit blogs page
 * the user can add a new blog using wtform and CKEditor
 * can click on a blog link to view that blog
  * here they can edit the blog via the wtfform incorporating the CKEditor
  * they can delete that blog
  
  
* animated social media links in aside credit to Sky Blue Youtube Tutorial 
 * these links currently open up to their home pages not my social media accounts
 
## Future Features 
---------------------------------------------------------------------------------------------------------------------------------------
* the RHS aside holds two profiles, it would good if these where dynamically generated to represent those who have blogged the most.
* this RHS space could be used for adverts
* a two step email validation of new signups to further verify the users of the site.
* allow users to change their login details 

## Testing
---------------------------------------------------------------------------------------------------------------------------------------
### Validation
* HTML was passed through a validator
* CSS was passed through a validator
* Python was validated through PEP8
### Manual Testing
* Responsive - The site was tested on multiple devices and browsers without any flaws.
* Links - All the links take the user to a valid end point on the site
* Forms - The Signup and Login perform the correct validation provided by wtforms
* Database Operations - The users can Create new users by signing up, Read blogs from the DB, Update a particular blog, Delete a blog     all with success.


## Deployment
---------------------------------------------------------------------------------------------------------------------------------------
The site was deployed to heroku and uses MongoDB as its datastore. The process involved created a remote repo on GitHub, opening up that repo with GitPod thereby creating a local repo that was directly pushed to the remote. The creation of the monoDB and its collections hosted in the cloud. The creation of a new app on heroku and connect to it through the CLI by creating the requirements.txt and Procfile whilst also setting the PORT,IP and MONGOURL so that the app can run on the server. Configure Heroku to get the app from GitHub and then test the app in heroku.

The Project remote repo is[here](https://github.com/DavidCaffrey/Milestone-3-Project) and can be cloned to the desktop and run locally
by typing git clone https://github.com/DavidCaffrey/Milestone-3-Project.git into the terminal and once completed type git remote rm origin to break the connection to the remote
## Credits
----------------------------------------------------------------------------------------------------------------------------------------

I would like to acknowledge Brad Travesy and his flask tutorials, which although a few years old and used a different DB they where helpful in pointing me in the right direction. Sky Blue for the tutorial on the sticky social media links.


























