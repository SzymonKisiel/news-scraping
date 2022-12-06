from server.scraping_server import ScrapingServer
from server.settings import SERVER_HOST, SERVER_PORT


def main():
    print('test')

    server = ScrapingServer(SERVER_HOST, SERVER_PORT)
    server.run()


if __name__ == '__main__':
    main()
