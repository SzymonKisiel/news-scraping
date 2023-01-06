import datetime

from utils.database_util import get_mysql_db_connection


def database_query_test():
    cnx = get_mysql_db_connection()
    cursor = cnx.cursor()
    query = ("SELECT id, url "
             "FROM articles")
    cursor.execute(query)
    for (id, url) in cursor:
        print(f"{id}: {url}")

    cursor.close()
    cnx.close()


def database_insert_test(url):
    cnx = get_mysql_db_connection()
    cursor = cnx.cursor()
    add_item = ("INSERT INTO articles"
                "(website, url, published_at, title, author, subtitle, text)"
                "VALUES (%(website)s, %(url)s, %(published_at)s, %(title)s, %(author)s, %(subtitle)s, %(text)s)")
    data = {
        'website': 'test_website',
        'url': url,
        'published_at': datetime.datetime.now(),
        'title': 'title',
        'author': 'author',
        'subtitle': 'subtitle',
        'text': 'text',
    }
    cursor.execute(add_item, data)
    print(cursor.lastrowid)

    cnx.commit()
    cursor.close()
    cnx.close()
