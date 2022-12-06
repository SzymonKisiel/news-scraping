import logging
from flask_server.app import create_app


def start_flask():
    app = create_app()
    app.run(host='0.0.0.0', port=5002, debug=True)


if __name__ == '__main__':
    logging.basicConfig()
    start_flask()
