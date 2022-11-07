import argparse
from modules.crawl import crawl_websites
from modules.set_scraping_start import set_scraping_start
from modules.get_scraping_start import get_scraping_start
from modules.set_delay import set_delay
from modules.get_delay import get_delay
from modules.search import search_websites
from modules.test import test
from modules.update_cookies import update_cookies
from utils.websites_util import websites


def main():
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

    # parse
    args = parser.parse_args()
    if args.command == 'crawl':
        input_websites = []
        if args.websites:
            input_websites = args.websites
        elif args.all:
            input_websites = websites
        print(f"Crawling websites: {input_websites}")
        if args.due_time:
            print(f"due-time: {args.due_time}")
        if args.run_time:
            print(f"run-time: {args.run_time}")
        if args.crawls_amount:
            print(f"crawls-count: {args.crawls_amount}")
        print()
        crawl_websites(input_websites, due_time=args.due_time, run_time=args.run_time, crawls_amount=args.crawls_amount)
    elif args.command == 'search':
        print(f"Searching for {args.word}\n")
        search_websites(args.word)
    elif args.command == 'set-scraping-start':
        input_websites = []
        if args.websites:
            input_websites = args.websites
        elif args.all:
            input_websites = websites
        print(f"Setting scraping start date ({args.date}) for websites: {input_websites}\n")
        for website in input_websites:
            set_scraping_start(args.date, website)
    elif args.command == 'get-scraping-start':
        input_websites = []
        if args.websites:
            input_websites = args.websites
        elif args.all:
            input_websites = websites
        print(f"Scraping start date for websites: {input_websites}")
        for website in input_websites:
            print(f"{website}: {get_scraping_start(website)}")
    elif args.command == 'set-delay':
        input_websites = []
        if args.websites:
            input_websites = args.websites
        elif args.all:
            input_websites = websites
        print(f"Setting delay ({args.delay}) for websites: {input_websites}\n")
        for website in input_websites:
            set_delay(website, args.delay)
    elif args.command == 'get-delay':
        input_websites = []
        if args.websites:
            input_websites = args.websites
        elif args.all:
            input_websites = websites
        print(f"Delay for websites: {input_websites}")
        for website in input_websites:
            print(f"{website}: {get_delay(website)}")
    elif args.command == 'test':
        test()
    elif args.command == 'update-cookies':
        update_cookies()


if __name__ == '__main__':
    main()
