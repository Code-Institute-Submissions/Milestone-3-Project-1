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























