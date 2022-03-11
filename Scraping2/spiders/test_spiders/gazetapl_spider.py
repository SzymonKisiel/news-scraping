import scrapy


class NewsSpider(scrapy.Spider):
    name = "gazetapl"
    page = 1
    MAX_PAGE = 1
    start_urls = [
        'https://wiadomosci.gazeta.pl/wiadomosci/0,0.html#e=CapLinks',
        'https://wiadomosci.gazeta.pl/wiadomosci/0,114871.html?str=1',
    ]

    def parse(self, response):
        articles = response.css("li.entry a::attr('href')").getall()
        yield from response.follow_all(articles, self.parse_article)
        if self.page < self.MAX_PAGE:
            self.page += 1
            url = f"https://wiadomosci.gazeta.pl/wiadomosci/0,114871.html?str={self.page}"
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
            'title': response.css("h1.article_title ::text").get(),
            'subtitle': response.css("div#gazeta_article_lead ::text").get(),
            'publishedAt': response.css("span.article_date time ::attr('datetime')").get(),
            'author': response.css("span.article_author--author ::text").get(),
            'text': extract_all_with_css("p.art_paragraph, h2.art_sub_title ::text")
        }
