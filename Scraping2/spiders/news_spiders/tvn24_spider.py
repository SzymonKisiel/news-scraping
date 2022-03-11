# https://www.tvp.info/swiat
# class="main-mesh-box__text-container box__text-container"
# main-mesh-box__text-container box__text-container
# main-mesh-box__text-container box__text-container
import scrapy


class Tvn24NewsSpider(scrapy.Spider):
    name = "tvn24_spider"
    page = 1
    MAX_PAGE = 10
    start_urls = [
        'https://tvn24.pl/najnowsze',
    ]

    def parse(self, response):
        articles = response.css("article div div a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            url = f"https://tvn24.pl/najnowsze/{self.page}"
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
            'publishedAt': extract_with_css("time.article-top-bar__date ::attr('datetime')"),
            'title': extract_with_css("h1.heading ::text"),
            'author': extract_with_css("div.author-first-name ::text"),
            'subtitle': extract_with_css(".article-element--lead_text ::text"),
            'text': extract_all_with_css(".article-element--paragraph ::text, .article-element--subhead ::text")
        }
