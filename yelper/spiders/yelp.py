# -*- coding: utf-8 -*-
import re
import scrapy


class YelpSpider(scrapy.Spider):
    name = 'yelp'
    allowed_domains = ['yelp.com']
    start_urls = ['https://www.yelp.com/biz/pho-99-authentic-vietnamese-shoreline']

    def parse(self, response):
        for review in response.css('.review-wrapper'):
            stars = review.css('.review-content .biz-rating .i-stars::attr(class)').extract()

            for s in stars:
                match = re.search('(\d)', s)
                if match:
                    stars = int(match[0])

            yield {
                    'restaurant': response.css('.biz-page-title::text').extract_first().strip(),
                    'stars': stars,
                    'address': "\n".join([a.strip() for a in response.css('.street-address address ::text').extract()]),
                    'review': review.css('.review-content p::text').extract(),
                    'useful': review.css('a.useful span.count::text').extract_first(),
                    'funny': review.css('a.funny span.count::text').extract_first(),
                    'cool': review.css('a.cool span.count::text').extract_first()

            }

        for next_page in response.css('a.pagination-links_anchor::attr(href)'):
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
