# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MigrationNewsItem(scrapy.Item):
    # define the fields for your item here like:
    href = scrapy.Field()
    title = scrapy.Field()
    alt_title = scrapy.Field()
    date = scrapy.Field()
    text = scrapy.Field()
