# CS235FlixSkeleton
The skeleton python project for the 2020 S2 CompSci 235 practical assignment CS235Flix.

**Getting Started**

1._Set up a virtual environment :_ 

First Way:

$ cd COMPSCI-235
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt

Second Way:

When you opened whole project in Pycharm
Left click on the right down corner 'Python3.7(FlixSkeletonWebApp)'(This is the name for my project)
Then choose 'Add Interpreter'
Then click 'OK'

2._Install all packages in 'requirements.txt':_

First Way:

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:COMPSCI-235' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment.

Second Way:

You can right click in 'requirements.txt' file then select 'install all packages'
Or Pycharm will remind you if you haven't installed all packages
Note: sometimes several packages need you to install manually after above steps.(The highlight ones)


**Basic Usage** 
1.Register/Login/Logout function
(Note:Login first before viewing movies)

2.Search Function
Can search by movie title, director name, actor name or genre.

3.Display Movie by Year.
2006-2016, 10 years, 1000 movies in total.

4.Display All Directors/Actors 
Pagination by 'flask_paginate'

5.Display movies by genre
click links below 'Genre'

6.View Review of users/Add your own review
By clicking the button below each movie

7.Add movie to your watchlist
Can add your favorite movie to your watchlist by clicking 'Like' button below each movie
If you do not refresh the page, the web app will remember each account's watchlist for each user, not messing up.

Warning:
Do not refresh the page before you logout.
