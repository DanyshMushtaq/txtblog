txtblog
=======

txtblog is a very simple blog engine written in Python3 using Bottle: Python Web Framework.

Features
--------
* Sqlite database for storing comments, blog posts, and static page contents.
* Simple admin console for making changes go live on the blog when needed.
* Only depends on python3, beaker, and markdown modules. Bottle is included.

Installation
------------

txtblog only works with python3. On Ubuntu/Debian, get it as follows.

    sudo apt-get install python3

You also need pip, virtualenv, and python setuptools

    sudo apt-get install python-setuptools pip

I don’t think the virtualenv in the debian repositories is up to date. It didn’t work for me with python3.
Use easy_install instead.

    sudo easy_install virtualenv

Initiate virtualenv for runing txtblog

    mkdir .virtualenvs
    cd .virtualenvs
    virtualenv --python=/usr/bin/python3 --no-site-packages txtblog
	
Activate the environment (deactivate again with ‘deactivate’ if needed).

    source txtblog/bin/activate

Now install needed packages into environment

    pip install markdown
    pip install beaker

Now you need to clone txtblog from Github. Place it where ever you think it’s appropiate.
    
    git clone https://github.com/kdorland/txtblog.git
	
Initialize the database and start it up

    python txtblog/manager.py
    python txtblog/blog_run.py

Now visit localhost:8080 and see if it works :)

You can access the admin console on http://localhost:8080/console. Look through the config.py file in the txtblog 
directory and change the settings to your liking. Please pick a new password for the admin console. Also, the 
adapter.wsgi file should be useful for running txtblog on mod_wsgi.
