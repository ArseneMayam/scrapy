# -*- coding: utf-8 -*-
import scrapy
from ..items import QuotetutorialItem


class QuotesSpiderSpider(scrapy.Spider):
    name = 'quotes'
    page_number = 2
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/page/1/']

    def parse(self, response):
        items = QuotetutorialItem()

        all_div_quotes = response.css('div.quote')

        for quote in all_div_quotes:
            title = quote.css('span.text::text').extract()
            author = quote.css('.author::text').extract()
            tag = quote.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items

        # next_page = response.css('li.next a::attr(href)').get()
        next_page = 'http://quotes.toscrape.com/page/' + str(QuotesSpiderSpider.page_number) + '/'

        # if next_page is not None:
        if QuotesSpiderSpider.page_number <= 11:
            QuotesSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
