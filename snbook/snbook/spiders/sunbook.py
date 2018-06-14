# -*- coding: utf-8 -*-
import scrapy
import re
from snbook.items import SnbookItem


class SunbookSpider(scrapy.Spider):
    name = 'sunbook'
    allowed_domains = ['suning.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        # 分组 获取图书分类的所有url
        a_list = response.xpath('//div[@class="three-sort"]/a/@href').extract()

        # 遍历,
        for a in a_list:
            cate_url = 'http://snbook.suning.com' + a  # http://snbook.suning.com/web/trd-fl/260400/95.htm

            # 交给下一个函数(parse_cate_url),发送请求
            yield scrapy.Request(
                cate_url,
                callback=self.parse_cate_url
            )

    def parse_cate_url(self, response):

        # 分组，获取这一页所有的图书详情,和url(原价和折扣价)
        detail_list = response.xpath('//div[@class="filtrate-books list-filtrate-books"]/ul/li')

        # 遍历,获取,图书名字,作者,封面图片,简介信息,详情url
        for li in detail_list:
            item = SnbookItem()
            item["title"] = li.xpath('.//div[@class="book-title"]/a/@title').extract_first()
            item["href"] = li.xpath('.//div[@class="book-title"]/a/@href').extract_first()
            item["auth_name"] = li.xpath('.//div[@class="book-author"]/a/text()').extract_first()
            item["content_img"] = li.xpath('.//div[@class="book-img"]/a/img/@src').extract_first()
            item["content"] = li.xpath('.//div[@class="book-descrip c6"]/text()').extract_first()
            print(item)

            # 详情url,交给下一个函数处理，获取折扣价格和原价
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item":item}
            )
            break

        # 获取下一页的url
        # a = response.css('.snPages .next::attr(href)').extract_first()
        # print(a)
        # while i < 50:
        #     next_page_url = "http://snbook.suning.com/web/trd-fl/100301/46.htm?pageNumber={}&sort=0".format(i)
        #     i += 1
        #     print(next_page_url)

    def parse_detail(self, response):
        item = response.meta['item']
        # 获取,原价,折扣后的价格  "pbPrice":'15.00'
        # ret = re.search(r'"pbPrice":(.*?),',response)
        # print('*'*20)
        # print(ret)
        item["raw_price"] = response.xpath('//em[@class="c9"]/text()')
        item["discount_price"] = "nihao"
        print(item)

        #  交给pip

        pass
