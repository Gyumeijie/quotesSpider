import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('small.author + a::attr(href)').getall():
            yield response.follow(href, self.parse_author)

        # follow pagination links
        for href in response.css('li.next a::attr(href)').get():
            yield response.follow(href, self.parse)

    @staticmethod
    def parse_author(response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthday': extract_with_css('span.author-born-date::text'),
            'bio': extract_with_css('div.author-description::text'),
        }
