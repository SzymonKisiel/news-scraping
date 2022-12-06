from modules.crawl import crawl_websites, async_crawl_websites
from modules.set_scraping_start import set_scraping_start
from modules.get_scraping_start import get_scraping_start
from modules.set_delay import set_delay
from modules.get_delay import get_delay
from modules.search import search_websites
from modules.test import test
from modules.update_cookies import update_cookies
from modules.test_database import database_query_test, database_insert_test
from utils.websites_util import websites


def program(args):
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
        # crawl_websites(
        #     input_websites,
        #     due_time=args.due_time,
        #     run_time=args.run_time,
        #     crawls_amount=args.crawls_amount)
        async_crawl_websites(
            input_websites,
            due_time=args.due_time,
            run_time=args.run_time,
            crawls_amount=args.crawls_amount)
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
    elif args.command == 'test-db1':
        database_query_test()
    elif args.command == 'test-db2':
        database_insert_test(args.url)
