import shutil, os, sys 

script_path = os.path.dirname(os.path.realpath(__file__)) + "/"
os.chdir(os.path.dirname(script_path))

try:
    import config
except ImportError:
    shutil.copy('config.py.template', 'config.py')
    import config

import blog
import logging, bottle, util

util.setLoggingFromConfig()

logging.info('Started')
bottle.run(host='lucca.codeheim.com', port=8080, debug=True, app=blog.app)
