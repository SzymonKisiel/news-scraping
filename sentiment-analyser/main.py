import logging
from app import create_app

logging.basicConfig()
app = create_app()

if __name__ == '__main__':
    # development - local configuration
    app.run(host='0.0.0.0', port=5003, debug=True)
else:
    # production - gunicorn configuration
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
