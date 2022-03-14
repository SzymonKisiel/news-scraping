import argparse
from crawl import crawl
from search import search


websites = ['fakt', 'onet', 'radiozet', 'rmf24', 'tvn24']


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command', required=True)

    crawl_cmd = subparser.add_parser('crawl')
    crawl_cmd.add_argument('--website', type=str, required=True, choices=websites)

    search_cmd = subparser.add_parser('search')
    search_cmd.add_argument('--word', type=str, required=True)

    args = parser.parse_args()
    if args.command == 'crawl':
        # print(f"Crawling {args.website}\n")
        crawl(args.website)
    elif args.command == 'search':
        # print(f"Searching for {args.word}\n")
        search(args.word)


if __name__ == '__main__':
    main()
