import scrapy
import pandas as pd

def get_migrations_url(query: str, date_from: str, date_to: str)->list:
    results = []
    bins = pd.date_range(start = date_from, end = date_to, freq = '2D').astype(str)
    bins_size = len(bins)-1
    for i in range(bins_size):
        results.append(f'https://ria.ru/services/search/getmore/?query={query}&tags_limit=20&date_from={bins[i]}&date_to={bins[i+1]}&sort%5B%5D=date')
    return results


class RiaSpider(scrapy.Spider):
    name = 'ria'
    allowed_domains = ['ria.ru']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 3,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 1
    }

    start_urls = get_migrations_url('Миграция в России', date_from = '2019-11-14', date_to = '2020-11-13')

    def parse(self, response):
        print('print:', response.url)
        for article in response.css('div.list-item a::attr(href)'):
            yield response.follow(article, callback=self.parse_news)

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

class GarantSpider(scrapy.Spider):
    name = 'garant'
    allowed_domains = ['garant.ru']
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOAD_DELAY': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 0.5,
        'AUTOTHROTTLE_DEBUG': True,
        'CONCURRENT_REQUESTS': 1
    }

    start_urls = ['https://www.garant.ru/news/tag/334/?ysclid=m3ee842w7g49890035']

    def parse(self, response):
        hrefs = response.css('div.descr>a::attr(href)').extract()
        for href in hrefs:
            yield response.follow(href, callback = self.parse_news)

    def parse_news(self, response):
        href = response.url
        title = response.css('h1::text').get()
        text = response.css('div>p::text').extract()
        date = response.css('div.actions-info>time::text').get()
        alt_tilte = title
        yield {
                'href': href,
                'title': title,
                'alt_title': alt_tilte,
                'date': date,
                'text': text
            }