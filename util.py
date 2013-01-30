import logging
import config

def escape(htmlstring):
    escapes = {'\"': '&quot;',
               '\'': '&#39;',
               '<': '&lt;',
               '>': '&gt;'}
    # This is done first to prevent escaping other escapes.
    htmlstring = htmlstring.replace('&', '&amp;')
    for seq, esc in escapes.items():
        htmlstring = htmlstring.replace(seq, esc)
    return htmlstring


def setLoggingFromConfig():
    format= '%(asctime)s - %(name)s:%(lineno)s - %(levelname)s - %(message)s'

    if config.log_level == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG, format=format)
    elif config.log_level == 'CRITICAL':
        logging.basicConfig(level=logging.CRITICAL, format=format)
    elif config.log_level == 'WARN':
        logging.basicConfig(level=logging.WARN, format=format)
    elif config.log_level == 'ERROR':
        logging.basicConfig(level=logging.ERROR, format=format)
    elif config.log_level == 'INFO':
        logging.basicConfig(level=logging.INFO, format=format)