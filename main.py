# from server.main import main
from console_app.program_parser import get_parser
from console_app.program import program


def main():
    parser = get_parser()
    args = parser.parse_args()
    program(args)

# def test():
#     parser = get_parser()
#     args = parser.parse_args(['crawl', '--websites', 'fakt', '--crawls-amount', '1'])
#     program(args)


if __name__ == '__main__':
    main()
    # test()
