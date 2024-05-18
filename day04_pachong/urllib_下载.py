"""
使用utllib下载数据和文件
"""
import urllib.request
url="http://www.baidu.com"
# response=urllib.request.urlopen(url)
# content=response.read()
# print(content)
# # 下载网页
# urllib.request.urlretrieve(url,'baidu.html')
# # 下载图片
# url_img='https://www.google.com/url?sa=i&url=https%3A%2F%2Fzh.wikipedia.org%2Fzh-tw%2FLisa_%2528%25E6%25B3%25B0%25E5%259C%258B%25E6%25AD%258C%25E6%2589%258B%2529&psig=AOvVaw3m5v9OGmYKM3HnMKGBUayr&ust=1715669084251000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCNjbwtGDioYDFQAAAAAdAAAAABAE'
# urllib.request.urlretrieve(url_img,'lisa.jpg')
# 下载视频
# video_url="https://v.douyin.com/i2HvtCqt/ g@o.qE 10/22 sRX:/ https://v.douyin.com/i2HvtCqt/ g@o.qE 10/22 sRX:/ "
# urllib.request.urlretriev e(video_url,"video.mp4")
response=urllib.request.urlopen(url)
content=response.read().decode('utf8')
# 请求对象的定制
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0'
         }
url=urllib.request.Request(url=url,headers=headers)
urllib.request.urlopen(url)
print(content)