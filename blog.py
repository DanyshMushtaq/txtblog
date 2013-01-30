import bottle, sqlite3, shutil
from beaker.middleware import SessionMiddleware
import manager, util

try:
    import config
except ImportError:
    shutil.copy('config.py.template', 'config.py')
    import config

# Keep the password hidden.
# Just in case the config leaks through a template.
admin_password = config.password
config.password = None

util.setLoggingFromConfig()

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 600,
    'session.data_dir': './tmp',
    'session.auto': True
}

database = "database/database.db"
app = SessionMiddleware(bottle.app(), session_opts)


###############################################################################
# The blog
###############################################################################

@bottle.route('/blog')
@bottle.route('/blog/page')
def root():
    return page(1)

@bottle.route('/blog/page/<page:int>')
def page(page):
    conn = sqlite3.connect(database)
    posts = manager.getBlogPosts(conn, page)
    pages = manager.getPageCount(conn)
    menu = manager.getStaticItem(conn, "Menu")
    sidebar = []
    for i in config.sidebar_statics:
        sitem = manager.getStaticItem(conn, i)
        sidebar.append(sitem)

    conn.close()
    return bottle.template('blog_frontpage', posts=posts, pages=pages,
        page=page, menu=menu, sidebar_items = sidebar, config = config)


@bottle.route('/blog/:name')
def item(name):
    conn = sqlite3.connect(database)
    item_title = name.replace('+', ' ')
    item = manager.getBlogPost(conn, item_title)

    if item == None:
        return bottle.HTTPError(404, "Page not found")
    posts = manager.getBlogPosts(conn, 1)
    comments = manager.getComments(conn, item_title)
    menu = manager.getStaticItem(conn, "Menu")

    sidebar = []
    for i in config.sidebar_statics:
        sitem = manager.getStaticItem(conn, i)
        sidebar.append(sitem)

    conn.close()

    return bottle.template('blog_item', item=item, comments=comments, 
        posts=posts, menu=menu, sidebar_items = sidebar, config = config)


@bottle.route('/blog/post-comment/:name', method='POST')
def post(name):
    conn = sqlite3.connect(database)
    author = bottle.request.forms.author
    email = bottle.request.forms.email
    url = bottle.request.forms.url
    comment = bottle.request.forms.comment
    ip = bottle.request.environ.get('REMOTE_ADDR')

    if author != None and email != None and comment != None:
        comment_data = {
            'author': author,
            'email': email,
            'url': url,
            'comment': comment,
            'ip': ip,
            'name': name}
        manager.insertComment(conn, comment_data)

    bottle.redirect("/blog/"+name)


###############################################################################
# The admin console
###############################################################################

@bottle.route('/console')
def console():
    s = bottle.request.environ.get('beaker.session')

    if s.get('user_login', False):
        return bottle.template('console_user', user_login=True, username=s['user'])
    else:
        return bottle.template('console_user', user_login=False)


@bottle.route('/console/logout', method='POST')
def console_logout():
    s = bottle.request.environ.get('beaker.session')
    s['user'] = None
    s['user_login'] = False
    s.save()
    bottle.redirect('/console')


@bottle.route('/console/login', method='POST')
def console_login():
    s = bottle.request.environ.get('beaker.session')
    u  = bottle.request.forms.username
    p =  bottle.request.forms.password

    if config.username == u and admin_password == p:
        s['user'] = u
        s['user_login'] = True
        bottle.redirect('/console')
    else:
        s['user_login'] = False
        return bottle.template('console_message', message='Login failed')


@bottle.route('/console/update', method='POST')
def console():
    conn = sqlite3.connect(database)
    s = bottle.request.environ.get('beaker.session')

    if s.get('user_login', False):
        manager.createDatabase(conn)
        manager.insertAllTexts(conn, config.text_dir)
        manager.cleanUp(conn, config.text_dir)
        conn.close()
        return bottle.template('console_message', message='Database reloaded')
    else:
        conn.close()
        return bottle.template('console_user', user_login=False)


@bottle.route('/console/my_ip')
def show_ip():
    ip = bottle.request.environ.get('REMOTE_ADDR')
    # or ip = request.get('REMOTE_ADDR')
    # or ip = request['REMOTE_ADDR']
    return "Your IP is: %s" % ip


@bottle.route('/not_implemented')
def not_implemented():
    return 'Not yet implemented...'



###############################################################################
# Serving static content
###############################################################################

@bottle.route('/static/:name')
def static_page(name):
    conn = sqlite3.connect(database)
    item_title = name.replace('+', ' ')
    item = manager.getStaticItem(conn, item_title)
    posts = manager.getBlogPosts(conn, 1)
    menu = manager.getStaticItem(conn, "Menu")

    sidebar = []
    for i in config.sidebar_statics:
        sitem = manager.getStaticItem(conn, i)
        sidebar.append(sitem)

    if item == None:
        return bottle.HTTPError(404, "Page not found")

    conn.close()

    return bottle.template('blog_static_item', item=item, comments=None, 
        posts=posts, menu = menu, config = config, sidebar_items = sidebar)


@bottle.route('/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='./web/')


@bottle.route('/')
def server_static_root():
    return static_page(config.frontpage_item)


