import argparse
from utils.time_util import *
from datetime import *
import pytz
from crawl import crawl_websites
from utils.websites_util import websites
from set_scraping_start import set_scraping_start


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    crawl_cmd = subparser.add_parser('crawl')
    crawl_cmd.add_argument('--websites', type=str, required=True, nargs='+', choices=websites)

    crawl_all_cmd = subparser.add_parser('crawl_all')

    search_cmd = subparser.add_parser('search')
    search_cmd.add_argument('--word', type=str, required=True)

    set_scraping_start_cmd = subparser.add_parser('set_scraping_start')
    set_scraping_start_cmd.add_argument('--websites', type=str, required=True, nargs='+', choices=websites)
    set_scraping_start_cmd.add_argument('--date', type=str, required=True)

    set_scraping_start_all_cmd = subparser.add_parser('set_scraping_start_all')
    set_scraping_start_all_cmd.add_argument('--date', type=str, required=True)

    args = parser.parse_args()
    if args.command == 'crawl':
        print(f"Crawling {args.websites}\n")
        crawl_websites(args.websites)
    elif args.command == 'crawl_all':
        print(f"Crawling all websites\n")
        crawl_websites(websites)
    elif args.command == 'search':
        print(f"Searching for {args.word}\n")
    elif args.command == 'set_scraping_start':
        print(f"Setting scraping start date ({args.date}) for {args.websites}\n")
        for website in args.websites:
            set_scraping_start(args.date, website)
    elif args.command == 'set_scraping_start_all':
        print(f"Setting scraping start date ({args.date}) for all websites\n")
        for website in websites:
            set_scraping_start(args.date, website)


if __name__ == '__main__':
    main()
