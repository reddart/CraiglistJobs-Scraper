# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = []
    start_urls = ['http://bangalore.craigslist.org/search/jjj/']

    def parse(self, response):
        jobs=response.xpath('.//*[@class="result-row"]')
        for job in jobs:
            link=job.xpath('.//p/a/@href').extract_first()
            yield Request(link,callback=self.parse_job,meta={'URL':link})
            
        relative_next_url=response.xpath('.//*[@class="button next"]/@href').extract_first()
        absolute_next_url=response.urljoin(relative_next_url)
        
        yield Request(absolute_next_url,callback=self.parse)
        
    def parse_job(self,response):
        title=response.xpath('.//*[@id="titletextonly"]/text()').extract()
        address=response.xpath('.//*[@class="postingtitletext"]/small/text()').extract_first()
        lines=response.xpath('.//*[@id="postingbody"]/text()').extract()
        description="".join(lines)
        compensation=response.xpath('.//*[@class="attrgroup"]/span[1]/b/text()').extract()
        emptype=response.xpath('.//*[@class="attrgroup"]/span[2]/b/text()').extract()
        
        yield{
                'Title':title,
                'location':address,
                'Job Description':description,
                'Compensation':compensation,
                'Employment Type':emptype,
                'URL': response.meta.get('URL')
            }
