import scrapy
import random

# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#instead of using start_requests we can simply use start_urls as a variable
    # start_urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
#    def start_requests(self):
#         urls = [
#             'http://quotes.toscrape.com/page/1/',
#             'http://quotes.toscrape.com/page/2/',
#         ]
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)
    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').get(),
    #             'author': quote.css('small.author::text').get(),
    #             'tags': quote.css('div.tags a.tag::text').getall(),
    #         }
#to save this file as json file we can run : scrapy crawl quotes -o quotes.json





#another method to give urls is shown below which will be dynamic instead of static.
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#             'http://quotes.toscrape.com/page/1/',
#     ]
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             yield {
#                 'text': quote.css('span.text::text').get(),
#                 'author': quote.css('small.author::text').get(),
#                 'tags': quote.css('div.tags a.tag::text').getall(),
#             }
#         next_page = response.css('li.next a::attr(href)').get()
#         if next_page is not None:
#             next_page = response.urljoin(next_page)
#             yield scrapy.Request(next_page, callback=self.parse) 






#shortening url with the help of follow:
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
            'http://quotes.toscrape.com/page/1/',
    ]
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

class AuthorSpider(scrapy.Spider):
    name = 'author'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        for link in response.css('.author + a::attr(href)'):
            yield response.follow(link, self.parse_author)
            
        for link in response.css('li.next a'):
            yield response.follow(link, self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }
        
         
#passing tags to hit only url with that tag
class Quoteswithtag(scrapy.Spider):
    name="usetag"

    def start_requests(self):
        url = "http://quotes.toscrape.com/"
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get()
            }

        for i in response.css('li.next a'):
            yield response.follow(i, self.parse)


class Authorss(scrapy.Spider):
    name = 'selfauthor'

    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tag': quote.css('div.tags a.tag::text').extract() 
            }

        if response.css('li.next a').extract_first() is not None:
            yield response.follow(response.css('li.next a').extract_first(), self.parse)