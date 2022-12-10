import mysql.connector
from settings.environment import is_docker
from model import article


def get_mysql_db_connection():
    basic_config = {
        'user': 'root',
        'password': 'p@ssw0rd1',
        'database': 'news_scraping_db',
    }

    if is_docker():
        host_config = {
            'host': 'scraper_db'
        }
    else:
        host_config = {
            'host': 'localhost',
            'port': 3306
        }

    config = basic_config | host_config
    db = mysql.connector.connect(**config)

    return db


# def insert_article(website: str, a: article):
#     cnx = get_mysql_db_connection()
#     cursor = cnx.cursor()
#     add_item = ("INSERT INTO articles"
#                 "(website, url, published_at, title, author, subtitle, text)"
#                 "VALUES (%(website)s, %(url)s, %(published_at)s, %(title)s, %(author)s, %(subtitle)s, %(text)s)")
#     data = {
#         'website': website,
#         'url': a.url,
#         'published_at': a.published_at,
#         'title': a.title,
#         'author': a.author,
#         'subtitle': a.subtitle,
#         'text': a.text,
#     }
#     cursor.execute(add_item, data)
#     print(cursor.lastrowid)
#
#     cnx.commit()
#     cursor.close()
#     cnx.close()


def insert_article(cnx, website: str, a: article):
    try:
        cursor = cnx.cursor()
        add_item = ("INSERT INTO articles"
                    "(website, url, published_at, title, author, subtitle, text)"
                    "VALUES (%(website)s, %(url)s, %(published_at)s, %(title)s, %(author)s, %(subtitle)s, %(text)s)")
        data = {
            'website': website,
            'url': a.url,
            'published_at': a.published_at,
            'title': a.title,
            'author': a.author,
            'subtitle': a.subtitle,
            'text': a.text,
        }
        cursor.execute(add_item, data)
        # print(f"Inserted article with id {cursor.lastrowid}")

        cnx.commit()
        cursor.close()

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
