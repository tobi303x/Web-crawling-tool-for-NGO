# import scrapy


# class NgoArrticlesSpider(scrapy.Spider):
#     name = 'ngo_arrticles'
#     start_urls = ['https://fundusze.ngo.pl/aktualne?page=1&terc=0407']

#     def parse(self, response):
#         yield {
#             "text": response.css(".pt3-ns div.mt2:nth-of-type(3)").get()
            
#         }
import scrapy


class NgoArrticlesSpider(scrapy.Spider):
    name = 'ngo_arrticles'
    start_urls = ['https://fundusze.ngo.pl/aktualne?page=1&terc=0205']

    def parse(self, response):
        curr_url = response.request.url
        Woj_i_Pow = curr_url[-4:]
        options = response.css('#select_156_gmi option:not([disabled])')
        for option in options:
            value = option.attrib['value']
            name = option.css('::text').get().strip()
            yield {
                'Województwo': Woj_i_Pow,
                # 'Powiat/Miasto': Pow,
                'name': name,
                'value': value
            }



# scrapy crawl ngo_arrticles -O data.csv