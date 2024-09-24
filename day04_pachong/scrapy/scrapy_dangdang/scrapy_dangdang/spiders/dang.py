from day04_pachong import scrapy
from day04_pachong.scrapy.scrapy_dangdang.scrapy_dangdang.items import ScrapyDangdangItem


class DangSpider(scrapy.Spider):
    name = "dang"
    # 如果是多页下载的话 那么必须要调整的是allow_domains的范围 一般情况下只写域名
    allowed_domains = ["bang.dangdang.com"]
    start_urls = ["http://bang.dangdang.com/books/bestsellers/01.01.00.00.00.00-recent7-0-0-1-1"]
    base_url="http://bang.dangdang.com/books/bestsellers/01.01.00.00.00.00-recent7-0-0-1-"
    page=1

    def parse(self, response):
        print("==================")
    # pipelines 下载数据
    # items 定义数据结构
    # src=//ul[@class="bang_list clearfix bang_list_mode"]/li//ul[@class="bang_list clearfix bang_list_mode"]/li//img/@src
    # alt= //ul[@class="bang_list clearfix bang_list_mode"]/li//div[@class='name']/a/@title
    # price=//ul[@class="bang_list clearfix bang_list_mode"]/li//div[@class='price']//span[@class='price_n']
    # 所有的seletor的对象 都可以再次调用xpath方法
        li_list=response.xpath('//ul[@class="bang_list clearfix bang_list_mode"]/li')
        for li in li_list:
            src=li.xpath('.//img/@src').extract_first()
            name=li.xpath('.//div[@class="name"]/a/@title').extract_first()
            price=li.xpath('.//div[@class="price"]//span[@class="price_n"]/text()').extract_first()
            print(src,name,price)
        book=ScrapyDangdangItem(src=src,name=name,price=price)
        # 简单理解：yield就是return返回一个值，并且记住这个返回的位置，下次迭代就从这个位置后（下一行）开始
        # 获取一个book 就交给pipelines
        yield book
        if self.page<100:
            self.page=self.page+1
            url=self.base_url+str(self.page)
            # 怎么去调用parse方法
            # scrapy.Request就是scrapy的get请求
            # url就是请求地址
            # callback是你要执行的那个函数 注意不要加()
        yield scrapy.Request(url, callback=self.parse)



