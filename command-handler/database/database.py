import mysql.connector
from database.env import is_docker


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
