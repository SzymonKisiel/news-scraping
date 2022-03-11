import scrapy


class NewsSpider(scrapy.Spider):
    name = "news_test2"
    page = 1
    MAX_PAGE = 2
    start_urls = [
        'https://www.polityka.pl/tematy/technologie',
    ]

    def parse(self, response):
        articles = response.css("li.cg_tag_index_item a ::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)

        next_page = response.css(".cg_pager_nextpage_link ::attr('href')").get()
        if next_page and self.page < self.MAX_PAGE:
            self.page += 1
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            result = ''
            for block in response.css(query).getall():
                result += block
            return result

        yield {
            'url': response.url,
            'title': extract_with_css('.cg_article_internet_title ::text'),
            'subtitle': '',
            'publishedAt': extract_with_css('.cg_article_date ::text'),
            'author': extract_with_css('.cg_article_author_name ::text'),
            'text': extract_all_with_css('.cg_article_content ::text')
        }
