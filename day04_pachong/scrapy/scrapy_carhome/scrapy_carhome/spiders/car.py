from day04_pachong import scrapy


class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ["car.autohome.com.cn"]
    # 注意：如果你的请求的接口是html为结尾的 那么是不需要加/
    start_urls = ["https://car.autohome.com.cn/price/brand-15.html"]

    def parse(self, response):
        print("==========")
        name_list=response.xpath('//div[@class="main-title"/a/text()]')
        price_list=response.xpath('//div[@class="main-title"/a/text()]')
        print(type(name_list))
        print(name_list)
        for i in range(len(name_list)):
            # name.extract：提取目标页面的data数据
            name=name_list[i].extract()
            price=price_list[i].extract()
