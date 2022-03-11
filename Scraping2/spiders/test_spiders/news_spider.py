import scrapy


class NewsSpider(scrapy.Spider):
    name = "news_test"
    page = 1
    MAX_PAGE = 2
    start_urls = [
        'https://www.rp.pl/ekonomia/biznes?page=1',
    ]

    def parse(self, response):
        #articles = response.css('div.row.content--block a.contentLink')
        articles = response.css("div.row.content--block a.contentLink::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            url = f"https://www.rp.pl/ekonomia/biznes?page={self.page}"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_article(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            result = ''
            for block in response.css(query).getall():
                result += block.strip()
            return result

        yield {
            'url': response.url,
            'title': extract_with_css('.blog--title ::text'),
            'subtitle': extract_with_css('.blog--subtitle ::text'),
            'publishedAt': extract_with_css('.blog--meta span#livePublishedAtContainer ::text'),
            'author': extract_with_css('.author a ::text'),
            'text': extract_all_with_css('.article--paragraph ::text')
        }

# response.css('div.row').get()
# response.css('a').get()
# response.css('div.row div.col--fill a.contentLink::attr(href)').get()
# response.css('div.row.content--block a.contentLink::attr(href)').get()