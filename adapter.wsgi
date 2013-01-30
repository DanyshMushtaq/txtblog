import sys, os, bottle

script_path = os.path.dirname(os.path.realpath(__file__)) + "/"
sys.path = [script_path] + sys.path
os.chdir(os.path.dirname(__file__))

import blog

bottle.debug = False
application = blog.app

