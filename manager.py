import sqlite3, datetime, time, logging, math, markdown, os
import config, util, txtparser

util.setLoggingFromConfig()

class Item(object):
    pass

class Comment(object):
    pass

PAGE_LIMIT = config.page_post_limit


def createDatabase(conn):
    cursor = conn.cursor()

    sql = """
        SELECT count(*)
        FROM sqlite_master
        WHERE type='table'
        AND name='blog_items';
        """
    cursor.execute(sql)
    res = cursor.fetchone()[0]

    # If the table does not exist, create everything
    if res == 0:
        sql = """
            CREATE TABLE blog_items (
            id integer primary key AUTOINCREMENT,
            item_name text,
            item_title text,            
            item_text text,
            author text,
            creation_date integer,
            edit_date integer,
            static boolean
            )
            """
        cursor.execute(sql)

        sql = """
            CREATE TABLE blog_categories (
            id integer primary key AUTOINCREMENT,
            name text
            )
            """
        cursor.execute(sql)

        sql = """
            CREATE TABLE blog_item_categories (
            item_id integer,
            category_id integer
            )
            """
        cursor.execute(sql)

        sql = """
            CREATE TABLE blog_item_comments (
            comment_id integer primary key AUTOINCREMENT,
            item_name text,
            comment text,
            name text,
            website text,
            email text,
            ip text,
            date integer
            )
            """
        cursor.execute(sql)


def insertNewCategories(conn, categories):
    cursor = conn.cursor()

    exists = """
        select count(*)
        from blog_categories
        where name = ?
        """

    insert = """
        insert into blog_categories
        (name) values (?)
        """

    for c in categories:
        cursor.execute(exists, [c])
        res = cursor.fetchone()[0]

        if not res:
            logging.debug("Inserting new category '%s' " % c)
            cursor.execute(insert, [c])

    conn.commit()


def insertCategoriesForText(conn, categories, text_name):
    cursor = conn.cursor()

    insert = """
        insert into blog_item_categories
        (item_id, category_id)
        values (?,?)
        """
    getTextId = """
        select id from blog_items
        where item_name = ?
        """
    getCatId = """
        select id from blog_categories
        where name = ?
        """
    deleteAll = """
        delete from blog_item_categories
        """

    cursor.execute(deleteAll)
    cursor.execute(getTextId, [text_name])
    logging.debug([text_name])
    item_id = cursor.fetchone()[0]

    for c in categories:
        cursor.execute(getCatId, [c])
        cat_id = cursor.fetchone()[0]

        logging.debug('inserting item category pairs')
        cursor.execute(insert, [item_id, cat_id])

    conn.commit()


def insertAllTexts(conn, root):
    cursor = conn.cursor()
    texts = txtparser.getTextCollection(root)

    insert = """
        insert into blog_items
        (item_name, item_title, item_text, author, creation_date, edit_date, static)
        values (?,?,?,?,?,?,?)
        """
    update = """
        update blog_items
        set item_title = ?, item_text = ?, edit_date = ?, author = ?, static = ?
        where item_name = ?
        """
    exists = """
        select count(*)
        from blog_items
        where item_name = ?
        """

    for item in texts:
        cursor.execute(exists, [item.name])
        res = cursor.fetchone()[0]

        title = item.title
        if title != None:
            title = title.strip()
        dt = item.unixtime

        if res:
            logging.debug('Updating')
            cursor.execute(update, (title, item.html, dt, item.author, item.static, item.name))
        else:
            logging.debug('Inserting')
            cursor.execute(insert, (item.name, title, item.html,
                                    item.author, dt, dt, item.static))

        if item.categories:
            insertNewCategories(conn, item.categories)
            insertCategoriesForText(conn, item.categories, item.name)
            logging.debug('categories: '+','.join(item.categories))


    conn.commit()


def insertComment(conn, comment_data):
    author = comment_data['author']
    url = comment_data['url']
    comment = util.escape(comment_data['comment'])
    email = comment_data['email']
    ip = comment_data['ip']
    name= comment_data['name']
    dt = time.time()

    logging.info('Inserting comment by '+author)

    cursor = conn.cursor()

    insert = """
        insert into blog_item_comments
        (item_name, comment, name, website, email, ip, date)
        values (?,?,?,?,?,?,?)
        """

    getItemName = """
        select item_name
        from blog_items
        where item_title = ?
        """

    cursor.execute(getItemName, [name])
    data = cursor.fetchall()[0]
    item_name = data[0]
    logging.debug("item_name " + item_name)

    insert_data = [item_name, comment, author, url, email, ip, dt]
    cursor.execute(insert, insert_data)
    conn.commit()


def getComments(conn, item_name):
    logging.debug('Getting comments for ' + item_name)
    cursor = conn.cursor()

    result = []

    # Get item id
    getItemId = """
        select item_name
        from blog_items
        where item_title = ?
        """

    cursor.execute(getItemId, [item_name])
    data = cursor.fetchall()
    if len(data) < 1:
        return None

    item_name = data[0][0]
    logging.debug("item_name " + item_name)

    # Get comments
    getComments = """
        select comment, name, website, date
        from blog_item_comments
        where item_name = ?
        """

    cursor.execute(getComments, [item_name])
    data = cursor.fetchall()

    for d in data:
        comment = Comment()
        comment.html = markdown.markdown(d[0])
        comment.name = d[1]
        comment.website = d[2]
        dt = datetime.datetime.fromtimestamp(int(d[3])).strftime('%Y-%m-%d')
        comment.date = dt
        result.append(comment)

    return result


def clearBlogPosts(conn):
    cursor = conn.cursor()
    sql = 'delete from blog_items'
    cursor.execute(sql)
    conn.commit()


def cleanUp(conn, root):
    texts = txtparser.getTextCollection(root)

    cursor = conn.cursor()

    getItems = """
        select item_name from blog_items
        order by creation_date desc
        """
    delete = "delete from blog_items where item_name = ?"

    cursor.execute(getItems)
    data = cursor.fetchall()

    # get names into a list
    names = []
    for t in texts:
        names.append(t.name)
        logging.debug('getting name ' + t.name)

    for rec in data:
        name = rec[0]
        if any(name in s for s in names):
            logging.debug(name+' exists in list')
        else:
            logging.debug('deleting '+name)
            cursor.execute(delete, [name])

    conn.commit()


def getStaticItem(conn, item_title):
    logging.debug('Get static item '+ item_title)
    cursor = conn.cursor()

    getItem = """
        select id, item_title, item_text, author, creation_date
        from blog_items
        where item_title = ?
        and static = 1
        order by creation_date desc
        """

    cursor.execute(getItem, [item_title])
    results = cursor.fetchall()

    if len(results) < 1:
        return None

    data = results[0]

    item = Item()
    item.name = item_title
    item.title = data[1]
    item.html = data[2]
    item.author = data[3]

    return item


def getBlogPost(conn, item_title):
    logging.debug('Get blog post '+ item_title)
    cursor = conn.cursor()

    getItem = """
        select id, item_title, item_text, author, creation_date, item_name
        from blog_items
        where item_title = ?
        and static = 0
        order by creation_date desc
        """

    getCategories = """
        select c.name
        from blog_items b, blog_item_categories ic, blog_categories c
        where b.id = ?
        and ic.category_id = c.id
        and b.id = ic.item_id
        order by creation_date desc;
        """

    cursor.execute(getItem, [item_title])
    results = cursor.fetchall()

    if len(results) < 1:
        return None

    data = results[0]

    item = Item()
    item.categories = []
    item.title = data[1]
    item.html = data[2]
    item.author = data[3]
    item.name = data[5]

    dt = datetime.datetime.fromtimestamp(int(data[4])).strftime('%Y-%m-%d')
    item.date = dt

    return item


def getBlogPosts(conn, page):
    logging.debug('Get blog posts')
    cursor = conn.cursor()

    getItems = """
        select id, item_name, item_title, item_text, author, creation_date
        from blog_items
        where static = 0
        order by creation_date desc
        """

    getCategories = """
        select c.name
        from blog_items b, blog_item_categories ic, blog_categories c
        where b.id = ?
        and ic.category_id = c.id
        and b.id = ic.item_id
        order by creation_date desc;
        """

    getCommentCount = """
        select count(*)
        from blog_item_comments
        where item_name = ?
        """

    start_item = int((page-1) * PAGE_LIMIT)

    cursor.execute(getItems)
    data = cursor.fetchall()
    result = []

    num = 0

    for rec in data:
        id = rec[0]
        num = num + 1
        cursor.execute(getCategories, [id])
        cat = cursor.fetchall()
        categories = []

        # TODO: Why is this necesary? Look into API later.
        for c in cat:
            logging.debug("category: "+c[0])
            categories.append(c[0])

        item = Item()
        item.categories = categories
        item.name = rec[1]
        item.title = rec[2]
        item.html = rec[3]
        item.author = rec[4]
        # %Y-%m-%d %H:%M:%S
        date = datetime.datetime.fromtimestamp(int(rec[5])).strftime('%Y-%m-%d')
        item.date = date

        cursor.execute(getCommentCount, [item.name])
        count = cursor.fetchall()
        item.comment_count = count[0][0]

        result.append(item)

    result = result[start_item:start_item+PAGE_LIMIT]
    return result


def getPageCount(conn):
    logging.info('Get page count')
    cursor = conn.cursor()

    getPages = """
        select count(*)
        from blog_items
        where static = 0
    """

    cursor.execute(getPages)
    pages = cursor.fetchone()[0]

    return math.ceil(pages/PAGE_LIMIT)


if __name__ == "__main__":
    script_path = os.path.dirname(os.path.realpath(__file__)) + "/"
    print('Updating blog database.')
    print('Database:', script_path+"database/database.db")
    print('Text dir:', script_path+config.text_dir)

    conn = sqlite3.connect(script_path+"/database/database.db")

    # In case it doesn't already exist. Will not overwrite.
    createDatabase(conn)

    insertAllTexts(conn, script_path+config.text_dir)
    cleanUp(conn, script_path+config.text_dir)

    conn.close()


