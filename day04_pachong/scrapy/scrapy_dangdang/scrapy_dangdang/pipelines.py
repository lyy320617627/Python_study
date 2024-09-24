# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import urllib.request

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 如果想使用管道的话 那么就必须在settings中开启管道
class ScrapyDangdangPipeline:
    # 在爬虫文件执行之前，执行的方法
    def open_spider(self, spider):
        self.fp=open("book.json",'w',encoding='utf-8')
        print("++++++++")
    # item就是yield后买你的book对象
    def process_item(self, item, spider):
        self.fp.write(str(item))
        # 下面这种方法会频繁的打开文件和关闭文件
        # with open('book.json','a',encoding='utf-8') as fp:
        #     # (1) wirte方法必须要写一个字符串 而不能是其他的对象
        #     # （2）w模式 会每一个对象都打开一次文件 覆盖之前的内容
        #     fp.write(str(item))
        return item
    # 在爬虫文件执行之后，执行的方法
    def close_spider(self, spider):
        self.fp.close()
        print("---------")
# 多条管道的开启
# （1）定义管道类
#  (2) 在settings中开启管道
class DangdangDownloadPipeline:
    def process_item(self, item, spider):
        url='http:'+item.get('src')
        filename=item.get('name')
        urllib.request.urlretrieve(url=url,filename=filename)
        return item