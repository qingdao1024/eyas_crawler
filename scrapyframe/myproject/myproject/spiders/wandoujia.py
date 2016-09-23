# -*- coding: utf-8 -*-
import scrapy


class WandoujiaSpider(scrapy.Spider):
    name = "wandoujia"
    allowed_domains = ["http://www.wandoujia.com/apps"]
    start_urls = (
        'http://www.http://www.wandoujia.com/apps/',
    )

    def parse(self, response):
        pass
