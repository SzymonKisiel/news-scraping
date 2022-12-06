import logging
# from server.main import main
from console_app.program_parser import get_parser
from console_app.program import program
from flask_server.app import create_app


def main():
    parser = get_parser()
    args = parser.parse_args()
    program(args)


# def test():
#     parser = get_parser()
#     args = parser.parse_args(['crawl', '--websites', 'fakt', '--crawls-amount', '1'])
#     program(args)

logging.basicConfig()
app = create_app()

if __name__ == '__main__':
    # development - local configuration
    app.run(host='0.0.0.0', port=5002, debug=True)
else:
    # production - gunicorn configuration
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
