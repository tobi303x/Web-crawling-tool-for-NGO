
import scrapy
from scrapy_redis.spiders import RedisSpider

class QuotesSpider(RedisSpider):
    name = "scrape_quotes_worker"
    redis_key = 'filters_queue:start_urls'
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 2
            
    def parse(self, response):
        curr_url = response.request.url
        Woj_i_Pow = curr_url[-4:]
        options = response.css('#select_156_gmi option:not([disabled])')
        for option in options:
            value = option.attrib['value']
            name = option.css('::text').get().strip()
            yield {
                'Województwo': Woj_i_Pow,
                'name': name,
                'value': value
            }
# scrapy crawl scrape_quotes_worker