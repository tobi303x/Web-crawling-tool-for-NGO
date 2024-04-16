
import scrapy
from scrapy_redis.spiders import RedisSpider
import redis
from dotenv import load_dotenv
import os


load_dotenv()
redisClient = redis.from_url(os.getenv('REDIS_CLOUD_KEY'))

class QuotesSpider(RedisSpider):
    name = "ArticlesLinks"
    redis_key = 'pages_queue:start_urls'
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 1
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 1
            
    def parse(self, response):
        for quote in response.css('li.bb'):
            link = quote.css('.fw5 a.near-black::attr(href)').get()
            redisClient.lpush('ArticlesLinks:start_urls', link)
#