import blog, logging, bottle, util

util.setLoggingFromConfig()

logging.info('Started')
bottle.run(host='localhost', port=8080, debug=True, app=blog.app)