import scrapy
import logging


class AuthorSpider(scrapy.Spider):
    name = 'author'
    delay_setting_name = "DELAY_TEST1"
    start_urls = ['https://quotes.toscrape.com/']

    def __init__(self):
        super()
        logging.getLogger('scrapy').setLevel(logging.CRITICAL)

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }