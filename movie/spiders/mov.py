# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from movie.items import MovItem, MovieItem

class MovSpider(scrapy.Spider):
    name = 'mov'
    allowed_domains = ['www.jizzkontu.com']
    start_urls = ['http://www.jizzkontu.com//']

    def parse(self, response):
        """
        1. 获取列表信息
        2. 获取下一页
        """
        post_part = response.xpath("//ul[contains(@class,'listThumbs')]/li")
        for post_node in post_part:
            # 获取图片
            thumb = post_node.xpath("a[contains(@class,'thumb')]/img/@src").extract_first()
            # 获取标题
            title = post_node.xpath("a[contains(@class,'title')]/text()").extract_first()
            # 获取时长
            duration = post_node.xpath("a[contains(@class,'thumb')]/span[contains(@class,'duration')]/text()").extract_first()
            # 获取时间
            post_date = post_node.xpath("span[contains(@class,'info right')]/text()").extract_first()
            # 获取URL
            post_url = post_node.xpath("a[contains(@class,'thumb')]/@href").extract_first()

            # 抓取详情页信息
            yield Request(url=parse.urljoin(response.url, post_url),meta={"thumb": thumb, "title": title, "duration": duration, "post_date": post_date}, callback=self. parse_detail)

        # 下一页链接
        next_url = response.xpath("//div[contains(@class,'pager')]/a[text()='Next »']/@href").extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self,response):
        import re
        import codecs
        p = re.compile(r'(http:\/\/cdn.*?_240.mp4.*?\")')
        res = p.findall(str(response.body))
        res = re.sub('"', '', res[0]).split(':')
        res = 'http:' + res[len(res)-1]
        # for index, val in enumerate(res):
        #     if re.match('http://.*?\.m$', val):
        #         del res[index]
        video_url = '\r\n'.join(res)
        with codecs.open('mov.txt','a','utf-8') as f:
            f.write(video_url + '\r\n')
        item_loader = MovItem(item=MovieItem(),response=response)
        item_loader.add_value("url",response.url)
        item_loader.add_value("thumb",response.meta.get("thumb"))
        item_loader.add_value("title",response.meta.get("title"))
        item_loader.add_value("duration",response.meta.get("duration"))
        item_loader.add_value("post_date",response.meta.get("post_date"))
        item_loader.add_value("video_url",video_url)
        item_loader.add_xpath("views_num","//div[contains(@id,'tabInfo')]/div[contains(@class,'col3')]/p[1]/text()")
        item_loader.add_xpath("channel","//div[contains(@id,'tabInfo')]/div[contains(@class,'col3')]/p[2]/a/text()")
        movie_item = item_loader.load_item()
        yield movie_item