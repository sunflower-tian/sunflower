# -*- coding: utf-8 -*-
import scrapy
from travel.items import TravelItem


class TravelTalkSpider(scrapy.Spider):
    name = 'travel_talk'
    allowed_domains = ['you.ctrip.com']
    start_urls = ['https://you.ctrip.com/travels/guangzhou152/t3.html']
    page = 1
    id = 0

    def parse(self, response):
        for i in range(10):
            item = TravelItem()
            self.id = self.id+1
            item['id'] = self.id
            # print(type(item['id']))
            item['title'] = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/dl/dt/text()").extract_first()
            # item['preview'] = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/span/img/@src").extract_first()
            #  链接不见了
            item['introduction'] = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/dl/dd[2]/text()").extract_first()
            # item['comment_num'] = \
            #     int(response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/ul/li[3]/i/text()").extract_first())
            # item['star_num'] = \
            #     int(response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/ul/li[2]/i/text()").extract_first())
            # re = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/ul/li[1]/i/text()").extract_first()
            # item['collection_num'] = int(float(re[:-1])*10**4)
            url = "https://you.ctrip.com" + str(response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/@href").extract_first())
            genres = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/a["+str(i+1)+"]/div/span/span[1]/@class").extract()
            if genres == []:
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.new_parse1)
                # item['type1'] = '0'
            elif genres[0][-1:] == '4':  # 典藏版
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.new_parse4)
                # item['type1'] = genres[0]
            elif genres[0][-1:] == '1':    # 精华版
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.new_parse1)
                # item['type1'] = genres[0]
            elif genres[0][-1:] == '3':    # 实用版
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.new_parse1)
                # item['type1'] = genres[0]
            elif genres[0][-1:] == '2':    # 美图版
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.new_parse1)
                # item['type1'] = genres[0]
        if self.page <= 6:
            next = response.xpath("/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div/a[7]/@href").extract_first()
            next_url = response.urljoin(next)
            self.page += 1
            yield scrapy.Request(url=next_url, callback=self.parse)
    # def new_parse(self, response):
    #     item = response.meta['item']
    #     re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/dl").extract_first()
    #     re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/dl/dt").extract_first()
    #     content = re[:10]# .replace(re0, "")
    #     # for i in range(10):
    #     #     content += \
    #     #         response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div["+str(i+3)+"]").extract_first()[:4]#+'\r\n'
    #     item['content'] = content
    #     yield item
    #     # yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def new_parse4(self, response):
        item = response.meta['item']
        item['preview'] = response.xpath('//*[@id="ctd_cover"]/@data-imagedisplayurl').extract()[0]
        re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]").extract_first()
        re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[1]").extract_first()
        content = re.replace(re0, "")
        recommend = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[3]").extract()
        if recommend != []:
            content = content.replace(recommend[0], "")
        urls_remove = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]//*[@data-classtype="1"and '
                                    '@href!="javascript:;"]/@href').extract()
        for url_remove in urls_remove:
            content = content.replace(url_remove, "")
        item['content'] = content
        yield item

    def new_parse1(self, response):
        item = response.meta['item']
        item['preview'] = response.xpath('//*[@id="ctd_cover"]/@data-imagedisplayurl').extract()[0]
        if response.xpath('//*[@id="ctd_cover"]/@data-imagedisplayurl').extract() == ['']:
            item['preview'] = response.xpath('//*[@id="ctd_cover"]/@src').extract()[0]
        re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]").extract_first()
        re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[1]").extract_first()
        content = re.replace(re0, "")
        recommend = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[2]/div[2]").extract()
        if recommend != []:
            content = content.replace(recommend[0], "")
        urls_remove = response.xpath('/html/body/div[2]/div[4]/div[1]/div[1]//*[@data-classtype="1"and '
                                     '@href!="javascript:;"]/@href').extract()
        for url_remove in urls_remove:
            content = content.replace(url_remove, "")
        item['content'] = content
        yield item


    def new_parse3(self, response):
        item = response.meta['item']
        re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]").extract_first()
        re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[1]").extract_first()
        content = re.replace(re0, "")
        item['content'] = content
        yield item

    def new_parse2(self, response):
        item = response.meta['item']
        re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]").extract_first()
        re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[1]").extract_first()
        content = re.replace(re0, "")
        item['content'] = content
        yield item

    def new_parse0(self, response):
        item = response.meta['item']
        re = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[2]").extract_first()[:4]
        # re0 = response.xpath("/html/body/div[2]/div[4]/div[1]/div[1]/div[1]").extract_first()
        content = re    # .replace(re0, "")
        item['content'] = content
        yield item





