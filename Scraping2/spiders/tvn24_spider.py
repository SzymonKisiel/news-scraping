# https://www.tvp.info/swiat
# class="main-mesh-box__text-container box__text-container"
# main-mesh-box__text-container box__text-container
# main-mesh-box__text-container box__text-container
import scrapy


class Tvn24NewsSpider(scrapy.Spider):
    name = "tvn24_spider"
    page = 1
    start_urls = [
        f"https://tvn24.pl/najnowsze/{page}"
        # 'https://tvn24.pl/najnowsze'
        # 'https://tvn24.pl/najnowsze/320'
        # 'https://tvn24.pl/najnowsze/50000'
    ]
    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [500]
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.skipped_pages = []
        self.skipped_articles = []

    def parse(self, response):
        # debug
        # if self.page > 200:
        #     return
        if response.status == 500:
            self.crawler.stats.inc_value('skipped_page_count')
            self.skipped_pages.append(response.url)
            self.page += 1
            yield scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}", callback=self.parse)
        else:
            articles = response.css("article div div a::attr('href')").getall()
            if articles:
                yield from response.follow_all(articles, self.parse_article)
                self.page += 1
                yield scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}", callback=self.parse)

        # if self.page < self.MAX_PAGE:
        #     self.page += 1
        #     url = f"https://tvn24.pl/najnowsze/{self.page}"
        #     yield scrapy.Request(url=url, callback=self.parse)

        # self.page += 1
        # next_page = scrapy.Request(f"https://tvn24.pl/najnowsze/{self.page}")
        # if next_page is not None:
        #     yield from response.follow(next_page, self.parse)

    def parse_article(self, response):
        if response.status == 500:
            self.crawler.stats.inc_value('skipped_article_count')
            self.skipped_articles.append(response.url)

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            result = ''
            for block in response.css(query).getall():
                result += block.strip() + " "
            return result

        yield {
            'url': response.url,
            'publishedAt': extract_with_css("time.article-top-bar__date ::attr('datetime')"),
            'title': extract_with_css("h1.heading ::text"),
            'author': extract_with_css("div.author-first-name ::text"),
            'subtitle': extract_with_css(".article-element--lead_text ::text"),
            'text': extract_all_with_css(".article-element--paragraph ::text, .article-element--subhead ::text")
        }

    def closed(self, reason):
        self.crawler.stats.set_value('skipped_pages', ', '.join(self.skipped_pages))
        self.crawler.stats.set_value('skipped_articles', ', '.join(self.skipped_articles))
