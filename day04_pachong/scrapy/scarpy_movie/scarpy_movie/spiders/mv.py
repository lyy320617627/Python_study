from day04_pachong import scrapy

from scarpy_movie.items import ScarpyMovieItem


class MvSpider(scrapy.Spider):
    name = "mv"
    allowed_domains = ["www.dygod.net"]
    start_urls = ["https://www.dygod.net/html/gndy/dyzz/index.html"]

    def parse(self, response):
        # pass
        # 要第一个的名字 和 第二页的图片
        src_list="//div[@class='co_content8']//td[2]//a[2]"
        a_list=response.xpath('//div[@class="co_content8"]//td[2]//a[2]')
        for a in a_list:
            name=a.xpath("./@title").extrzct_first()
            src=a.xpath("./@href").extract_first()
            print(name,src)
            # 第二页的地址是
            url="https://www.dygod.net"+src
            # 对第二页的链接发起访问
            yield scrapy.Request(url=url, callback=self.parse_second, meta={"name":name})
    def parse_second(self,response):
        # 注意：如果拿不到1数据 一定要检查你的xpath语法是否正确
        src=response.xpath("//div[@id='Zoom']//img/@src").extract_first()
        # 接收到请求的那个meta参数的值
        name=response.meta['name']
        print(src)
        # 记得要打开管道
        movie=ScarpyMovieItem(src=src,name=name)
        yield  movie
        print("==========")