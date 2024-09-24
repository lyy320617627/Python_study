from day04_pachong import scrapy


class TcSpider(scrapy.Spider):
    name = "tc"
    allowed_domains = ["hz.58.com"]
    start_urls = ["https://hz.58.com/quanzhizhaopin/?key=%E5%89%8D%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%88&cmcskey=%E5%B8%8C%E6%9C%9B%E8%8A%82&final=1&jump=1&specialtype=gls&classpolicy=LBGguide_B%2Cmain_B%2Cjob_B%2Chitword_false%2Cuuid_nkEA3Tm6PjT4WAPZZGaNTTxRKtniSpHy%2Cdisplocalid_79%2Cfrom_main%2Cto_jump%2Ctradeline_job%2Cclassify_B&search_uuid=nkEA3Tm6PjT4WAPZZGaNTTxRKtniSpHy&search_type=input"]

    def parse(self, response):
        print("山东菏泽曹县")
        # 返回的是响应的字符串
        content=response.text
        # 返回的是响应的二进制数据
        response_content=response.body
        print(content)
        print("-----------------------------------------------------------------------")
        span=response.xpath("//div[@class='filter']/div[@class='tabs']/a/span")[0]
        print(f"span:{span}")
