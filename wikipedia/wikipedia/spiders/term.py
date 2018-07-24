# -*- coding: utf-8 -*-
import scrapy
import spacy

class TermSpider(scrapy.Spider):
    name = 'term'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Heteroscedasticity']

    def parse(self, response):
        yield {
                'title': response.css('title::text').extract_first(), 
                'document': ' '.join(response.css('.mw-parser-output ::text').extract())
        }
        
        for link in response.css('.mw-parser-output a'):
            href = link.css('::attr(href)').extract_first()
            yield response.follow(href, callback=self.parse)
