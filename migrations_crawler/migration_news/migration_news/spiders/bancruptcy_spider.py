import scrapy
import pandas as pd

#def get_migrations_url(query: str, date_from: str, date_to: str)->list:
#    results = []
#    bins = pd.date_range(start = date_from, end = date_to, freq = '2D').astype(str)
#    bins_size = len(bins)-1
#    for i in range(bins_size):
#       results.append(f'https://ria.ru/services/search/getmore/?query={query}&tags_limit=20&date_from={bins[i]}&date_to={bins[i+1]}&sort%5B%5D=date')
#    return results


class BankrotSpider(scrapy.Spider):
    name = 'bankrot'
    allowed_domains = ['bankrot.fedresurs.ru']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 1
    }

    start_urls = ['https://bankrot.fedresurs.ru/bankrupts?regionId=all&isActiveLegalCase=null&offset=0&limit=15']

    def parse(self, response):
        print('print:', response.url)
        company_name = response.xpath('//app-bankrupt-result-card-company').extract()
        
        #css('div.u-card-result__name.u-card-result__name_mb.u-card-result__name_width')
        print(company_name)
        url = response.css('.info_position')    
        print(url)                  
        #yield response.follow(article, callback=self.parse_news)

    def parse_news(self, response):
        href = response.url
        title = response.css('div.article__title ::text').get()
        alt_tilte = response.css('h1.article__title::text').get()
        date = response.css('div.article__info-date a::text').get()
        text = ' '.join(response.css('div.article__text ::text').getall())
        if 'мигра' in text:
            yield {
                'href': href,
                'title': title,
                'alt_title': alt_tilte,
                'date': date,
                'text': text
            }