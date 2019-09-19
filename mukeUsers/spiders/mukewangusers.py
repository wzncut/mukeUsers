# -*- coding: utf-8 -*-
import scrapy
from mukeUsers.UserItems import UserItem
class MukewangusersSpider(scrapy.Spider):
    name = 'mukewangusers'
    allowed_domains = ['imooc.com/u']
    start_urls = ['https://imooc.com/u/3224566/courses?page=1']

    def parse(self, response):
        job = 0
        item = UserItem()
        for box in response.xpath('//div[@class="user-info clearfix"]/div[@class="user-info-right"]'):
            item['name'] = box.xpath('//span[1]/text()').extract()[0]

            if len(box.xpath('//span[1]/text()').extract()) != 0:
                item['sex'] = box.xpath('//span[1]/text()').extract()[1]
            else:
                item['sex'] = ''
            if (len(box.xpath('//span[2]/text()').extract()) != 0) and (len(box.xpath('//span[4]/text()').extract()) == 0):
                item['job'] = box.xpath('//span[2]/text()').extract()[1].strip()
                job = 1
                item['privince'] = ''
            elif len(box.xpath('//span[2]/text()').extract()) != 0 and (len(box.xpath('//span[4]/text()').extract()) != 0):
                item['privince'] = box.xpath('//span[2]/text()').extract()[1]
            else:
                item['privince'] = ''
            # if len(box.xpath('//span[3]/text()').extract()) != 0:
            #     item['city'] = box.xpath('//span[3]/text()').extract()[0]
            # else:
            #     item['city'] = ''
            if job == 0:
                if len(box.xpath('//span[4]/text()').extract()) != 0:
                # print (len(box.xpath('//span[4]/text()').extract()))
                    item['job'] = box.xpath('//span[4]/text()').extract()[0].strip()
                    job = 0
                else:
                    item['job'] = ''
                    job = 0
            else:
                job = 0
            item['time'] = response.xpath('//div[@class="study-info clearfix"]//div[@class="u-info-learn"]/em/text()').extract()[0]

            print (item['name'])
            print (item['sex'])
            print (item['privince'])
            print (item['job'])
            print (item['time'])
            # print(response.request.url)
        yield scrapy.Request(response.request.url,callback=self.Nextparse, meta=item, dont_filter=True)

        # numOfProject = len(response.xpath('//div[contains(@class,"clearfix tl-item")]//h3/a/text()').extract())
        # if item.get('projects', 0) != 0:
        # if item['projects']:
        #     project = ','.join(response.xpath('//div[contains(@class,"clearfix tl-item")]//h3/a/text()').extract())
        #     item['projects'] = item['projects'] + ',' + project
        #     print ("111111111111111111111111111")
        # else:
    def Nextparse(self, response):
        if response.meta.get('pro', 0) != 0:
            trans = ','.join(response.xpath('//div[contains(@class,"clearfix tl-item")]//h3/a/text()').extract())
            item = response.meta['pro']
            item['projects'] = item['projects']+trans
        else:
            item = response.meta
            item['projects'] = ','.join(response.xpath('//div[contains(@class,"clearfix tl-item")]//h3/a/text()').extract())
        next_page = response.xpath(u'//div[@class="page"]/a[contains(text(),"下一页")]/@href').get()

        if next_page:
            next_url = 'https://imooc.com' + next_page
            yield scrapy.Request(next_url, callback=self.Nextparse, meta={'pro': item}, dont_filter=True)
        yield item