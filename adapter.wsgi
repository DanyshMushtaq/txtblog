import sys, os

script_path = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path = [script_path] + sys.path
os.chdir(os.path.dirname(__file__))

import bottle, blog

bottle.debug = False
application = blog.app

