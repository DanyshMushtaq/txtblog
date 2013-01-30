import os, codecs, datetime, markdown, logging, util

logger = logging.getLogger(__name__)

class Item(object):
    pass

def stripMeta(text):
    result = ""

    for t in text.split('\n'):
        if not t.startswith('...'):
            result = result + t + '\n'

    return result

def getTextMeta(text_lines):
    meta = {'categories': None, 'author': None, 'title': None, 'static': False}

    for text in text_lines:
        if text.startswith('...'):
            t = text[3:].split('=')

            if t[0] == 'categories':
                meta['categories'] = t[1].split(',')

            if t[0] == 'author':
                meta['author'] = t[1]

            if t[0] == 'title':
                meta['title'] = t[1]

            if t[0] == 'static':
                if t[1].strip() == 'true':
                    meta['static'] = True

        else:
            return meta

    return meta

def getTexts(path):
    save_for_later = []
    items = []
    for root, dirs, files in os.walk(path):
        while len(dirs) > 0:
            save_for_later.append(dirs.pop(0))

        for f in files:
            input_file = codecs.open(root + '/' + f, mode="r", encoding="utf8")
            text = input_file.read()

            meta = getTextMeta(text.split('\n'))
            logger.debug(meta)

            text = stripMeta(text)
            html = markdown.markdown(text)

            time = os.path.getmtime(root + '/' + f)
            dt = datetime.datetime.fromtimestamp(time)

            item = Item()
            item.name = f
            item.html = html
            item.datetime = dt
            item.unixtime = time
            item.author = meta['author']
            item.categories = meta['categories']
            item.title = meta['title']
            item.static = meta['static']
            items.append(item)

    return (save_for_later, items)


def getTextCollection(root):
    dirs, texts = getTexts(root)
    return texts


