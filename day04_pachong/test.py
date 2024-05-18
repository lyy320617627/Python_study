import urllib.request, urllib.parse, urllib.error
import json1
from urllib.parse import unquote
from bs4 import BeautifulSoup

# 定义 HTML 字符串

# URL 编码的字符串
encoded_string =[{'uuId': 'iTWCgI8BATsnTWoGtNqh', 'chatId': '6ab4ea8b-92e6-470b-9532-2b03180f47ed', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%3Cp%3E%3Cspan%3E%E6%82%A8%E8%BF%99%E8%BE%B9%E5%8F%AF%E4%BB%A5%E5%B0%9D%E8%AF%95%E8%81%94%E7%B3%BB%E4%B8%8B%E5%BF%AB%E9%80%92%E5%B0%8F%E5%93%A5%EF%BC%8C%E7%9C%8B%E8%83%BD%E5%90%A6%E6%9A%82%E5%AD%98%E5%93%88%EF%BC%8C%E4%BA%B2%3C%2Fspan%3E%3C%2Fp%3E', 'icon': '', 'flag': 'agent', 'username': '1024', 'timestamp': 1715848000655, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': '0puBgI8BFCuCKgV0YwFW', 'chatId': '6ab4ea8b-92e6-470b-9532-2b03180f47ed', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E6%80%8E%E4%B9%88%E5%8A%9E', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847914309, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'iDWBgI8BATsnTWoGW9o_', 'chatId': '6ab4ea8b-92e6-470b-9532-2b03180f47ed', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E5%A6%82%E6%9E%9C%E5%8A%9E%E7%90%86%E5%92%8C%E7%BA%A6%E4%BA%86%EF%BC%8C%E4%BD%A0%E5%8F%91%E8%B4%A7%E4%BA%86%EF%BC%8C%E6%88%91%E4%B8%8D%E5%9C%A8%E7%8E%B0%E5%9C%A8%E7%9A%84%E5%9C%B0%E5%9D%80%E5%9C%B0%E6%96%B9', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847912239, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': '0ZuBgI8BFCuCKgV0UQEr', 'chatId': '6ab4ea8b-92e6-470b-9532-2b03180f47ed', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%3Cp%3E%3Cul%3E%3Cul%3E%3Cli%3E%3Cdiv%3E%3Cp%3E%E8%BF%99%E8%BE%B9%E4%BC%9A%E5%B8%AE%E6%82%A8%E5%8A%9E%E7%90%86%E5%90%88%E7%BA%A6%E7%9A%84%EF%BC%8C%E5%90%88%E7%BA%A6%E5%8A%9E%E7%90%86%E6%88%90%E5%8A%9F%E5%90%8E%E9%A2%84%E8%AE%A1%E5%9B%9B%E5%8D%81%E5%85%AB%E5%B0%8F%E6%97%B6%E5%86%85%E4%BC%9A%E5%AE%89%E6%8E%92%E5%8F%91%E8%B4%A7%E7%9A%84%E5%93%88%EF%BC%8C%E4%BA%B2%3Cbr%2F%3E%3C%2Fp%3E%3Cspan%3E%3C%2Fspan%3E%3C%2Fdiv%3E%3C%2Fli%3E%3Cli%3E%3C%2Fli%3E%3Cli%3E%3Cdiv%3E%3C%2Fdiv%3E%3C%2Fli%3E%3C%2Ful%3E%3Cli%3E%3C%2Fli%3E%3C%2Ful%3E%3Cp%3E%3Cbr%2F%3E%3C%2Fp%3E%3C%2Fp%3E', 'icon': '', 'flag': 'agent', 'username': '1024', 'timestamp': 1715847909654, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'z5uAgI8BFCuCKgV0wgGb', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E3%80%82%E3%80%82%E3%80%82', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847873160, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'hjWAgI8BATsnTWoGjNpL', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%3Cp%3E%E8%BF%99%E8%BE%B9%E4%BC%9A%E5%B8%AE%E6%82%A8%E5%8A%9E%E7%90%86%E5%90%88%E7%BA%A6%E7%9A%84%EF%BC%8C%E5%90%88%E7%BA%A6%E5%8A%9E%E7%90%86%E6%88%90%E5%8A%9F%E5%90%8E%E9%A2%84%E8%AE%A1%E5%9B%9B%E5%8D%81%E5%85%AB%E5%B0%8F%E6%97%B6%E5%86%85%E4%BC%9A%E5%AE%89%E6%8E%92%E5%8F%91%E8%B4%A7%E7%9A%84%E5%93%88%EF%BC%8C%E4%BA%B2%3Cbr%2F%3E%3C%2Fp%3E', 'icon': '', 'flag': 'agent', 'username': '1024', 'timestamp': 1715847859247, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'zpt_gI8BFCuCKgV06QEy', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E4%BD%A0%E9%99%A4%E4%BA%86%E5%A4%8D%E5%88%B6%E7%B2%98%E8%B4%B4%E4%B8%8D%E4%BC%9A%E5%8E%BB%E6%A0%B8%E5%AE%9E%E4%B8%8B%E5%95%8A', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847817502, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'hTV_gI8BATsnTWoGtNpL', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E3%80%82%E3%80%82%E3%80%82%E3%80%82', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847803961, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'lgR_gI8BsC4BCFHRowmC', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%3Cp%3E%E4%BA%B2%EF%BC%8C%E4%B8%8B%E5%8D%95%E6%A0%B8%E5%AE%9E%E5%90%8E%E6%97%A0%E7%89%B9%E6%AE%8A%E6%83%85%E5%86%B5%E6%98%AF48%E5%B0%8F%E6%97%B6%E5%8F%91%E8%B4%A7%E7%9A%84%E5%93%88%EF%BC%8C%E9%BA%BB%E7%83%A6%E6%82%A8%E8%BF%99%E8%BE%B9%E8%80%90%E5%BF%83%E7%AD%89%E5%BE%85%3C%2Fp%3E', 'icon': '', 'flag': 'agent', 'username': '1024', 'timestamp': 1715847799652, 'android': False, 'mine': True, 'play': False, 'read': True}, {'uuId': 'zZt_gI8BFCuCKgV0fgGJ', 'chatId': 'e18fe818-9a5a-4988-894d-9a25289cdfcc', 'tenantId': 'ff8080826537c4fc016538bd3b010089', 'content': '%E9%83%BD%E5%8F%91%E9%80%81%E7%9F%AD%E4%BF%A1%E4%BA%86%EF%BC%8C%E4%BB%8A%E5%A4%A9%E5%8F%AF%E4%BB%A5%E5%8F%91%E8%B4%A7%E5%90%97', 'icon': '', 'flag': 'customer', 'username': '18758255905', 'timestamp': 1715847790198, 'android': False, 'mine': True, 'play': False, 'read': True}]


# 解码
for item in encoded_string:
    decoded_string = unquote(item['content'])
    print(decoded_string)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(decoded_string, 'html.parser')
    # 提取文本部分
    text = soup.get_text()
    print(text)
    item['content'] = text
print(encoded_string)
# {
# 'agentId': "undefined",
# 'customer': "18258165237",
# 'desc': "true"
# 'pageNum': 0,
# 'pageSize': 20,
# 'tenantId': "ff8080826537c4fc016538bd3b010089"
# }
# Connection was forcibly closed by a peer.