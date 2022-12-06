import argparse
from utils.websites_util import websites


def get_parser():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    # crawl
    crawl_cmd = subparser.add_parser('crawl')
    crawl_group = crawl_cmd.add_mutually_exclusive_group(required=True)
    crawl_group.add_argument('--websites', type=str, nargs='+', choices=websites)
    crawl_group.add_argument('--all', action='store_true')
    crawl_cmd.add_argument('--due-time', dest='due_time', type=str, required=False,
                           help='datetime to which the crawler will be repeatedly run')
    crawl_cmd.add_argument('--run-time', dest='run_time', type=int, required=False,
                           help='amount of seconds for which the crawler will be repeatedly run')
    crawl_cmd.add_argument('--crawls-amount', dest='crawls_amount', type=int, required=False,
                           help='amount of times the crawler will be repeatedly run')

    # test3 = subparser.add_parser('test3')
    # test_group = test3.add_argument_group()
    # test_group.add_argument('-i', action='append', nargs='+')
    # test_group.add_argument('-count', type=int, action='append', nargs='+')
    # test_group.add_argument('-date', type=str, action='append', nargs='+')

    # test_cmd = subparser.add_parser('test')
    # websites = test_cmd.add_argument('--websites', type=str, required=True, nargs='+', choices=websites)

    # search
    search_cmd = subparser.add_parser('search')
    search_cmd.add_argument('--word', type=str, required=True)

    # set-scraping-start
    set_scraping_start_cmd = subparser.add_parser('set-scraping-start')
    set_scraping_start_group = set_scraping_start_cmd.add_mutually_exclusive_group(required=True)
    set_scraping_start_group.add_argument('--websites', type=str, nargs='+', choices=websites)
    set_scraping_start_group.add_argument('--all', action='store_true')
    set_scraping_start_cmd.add_argument('--date', type=str, required=True)

    # get-scraping-start
    get_scraping_start_cmd = subparser.add_parser('get-scraping-start')
    get_scraping_start_group = get_scraping_start_cmd.add_mutually_exclusive_group(required=True)
    get_scraping_start_group.add_argument('--websites', type=str, nargs='+', choices=websites)
    get_scraping_start_group.add_argument('--all', action='store_true')

    # set-delay
    set_delay_cmd = subparser.add_parser('set-delay')
    set_delay_group = set_delay_cmd.add_mutually_exclusive_group(required=True)
    set_delay_group.add_argument('--websites', type=str, nargs='+', choices=websites)
    set_delay_group.add_argument('--all', action='store_true')
    set_delay_cmd.add_argument('--delay', type=int, required=True)

    # get-delay
    get_delay_cmd = subparser.add_parser('get-delay')
    get_delay_group = get_delay_cmd.add_mutually_exclusive_group(required=True)
    get_delay_group.add_argument('--websites', type=str, nargs='+', choices=websites)
    get_delay_group.add_argument('--all', action='store_true')

    # test-cookies
    subparser.add_parser('update-cookies')

    # test-database
    subparser.add_parser('test-db1')
    insert_test = subparser.add_parser('test-db2')
    insert_test.add_argument('--url', type=str, required=True)

    return parser
