
import scrapy
from scrapy_redis.spiders import RedisSpider
import redis
import re
from dotenv import load_dotenv
import os


load_dotenv()

redisClient = redis.from_url(os.getenv('REDIS_CLOUD_KEY'))

class QuotesSpider(RedisSpider):
    name = "ArticlesData"
    redis_key = 'ArticlesLinks:start_urls'
    # Number of url to fetch from redis on each attempt
    redis_batch_size = 5
    # Max idle time(in seconds) before the spider stops checking redis and shuts down
    max_idle_time = 3
    
    def parse(self, response):
        # nabór = response.css('div.f7:nth-of-type(3) div.lh-title::text').get().split()
        # nabór = ''.join(nabór)
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});') 

        def cleanhtml(raw_html):
            text = re.sub(CLEANR, '', raw_html).strip()
            semitext = text.replace("\t", "")
            cleantext = semitext.replace("  ", "")
            return cleantext.replace("\n", "")
        yield {
            "Link": response.url,
            "Nagłówek": response.css('h2.f2-m::text').get().strip(),
            "Opis": response.css('.cms-red-orange strong::text').get(),
            "Lokalizacja": cleanhtml(response.css('div.f7:nth-of-type(2)').get()),
            "Nabór": cleanhtml(response.css('div.f7:nth-of-type(3)').get()),
            "Fundacja": cleanhtml(response.css('div.f7:nth-of-type(4)').get()),
            "Założyciel": cleanhtml(response.css('div.f7:nth-of-type(5)').get()),
            "Budżet": cleanhtml(response.css('div.f7:nth-of-type(6)').get()),
            "Procent": cleanhtml(response.css('div.f7:nth-of-type(7)').get()),
            "Dotacje": cleanhtml(response.css('div.f7:nth-of-type(8)').get()),
            "Aktywność": cleanhtml(response.css('div.f7:nth-of-type(9)').get()),
            "Organizacje": cleanhtml(response.css('div.f7:nth-of-type(10)').get()),
            "LinkDoStronyOrganizatora": response.css('a.f5::attr(href)').get()
        }
#scrapy crawl ArticlesData
        #NGO_Final/NGO_ArticlesLinks/RedisDB_Filters/scaling-python-scrapy-redis/redis-python-scrapy-examples