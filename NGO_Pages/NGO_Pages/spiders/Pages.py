import scrapy
import re

with open('../../Users_current_link.txt', 'r') as input_file:
    file_contents = input_file.read()
    url = file_contents
print(url)
class PagesSpider(scrapy.Spider):
    name = 'Pages'
    start_urls = [url]

    def parse(self, response):

        ilość_stron = response.css('span.f6-xl::text').getall()
        ilość_wyników = response.css('.pt3 .cms p::text').get()
        link = response.url

        yield {
        'ilość_stron': ilość_stron,
        'ilość_wyników': ilość_wyników, 
        'link': link
        }


# scrapy crawl Pages