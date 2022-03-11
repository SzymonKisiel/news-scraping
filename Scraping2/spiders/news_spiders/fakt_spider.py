import scrapy
from scrapy.spiders import SitemapSpider


# sitemap w scrapy shell:
# scrapy shell "https://www.fakt.pl/sitemap_article.xml"
# response.selector.register_namespace('d', 'http://www.sitemaps.org/schemas/sitemap/0.9')
# response.xpath('//d:loc/text()').getall()[


class FaktNewsSpider(SitemapSpider):
    name = "fakt_spider"
    allowed_domains = ["fakt.pl"]
    sitemap_urls = ["https://www.fakt.pl/sitemap_article.xml"]

    # parse article found in sitemap
    def parse(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_all_with_css(query):
            result = ''
            for block in response.css(query).getall():
                result += block.strip()
            return result

        yield {
            'url': response.url,
            'publishedAt': extract_with_css("div.article-date time ::attr(datetime)"),
            'title': extract_with_css("h1.article-title ::text"),
            'author': "",
            'subtitle': extract_all_with_css("div.article-lead ::text"),
            'text': extract_all_with_css(".article .article-p ::text")
        }
