"""
通过代码演示代理池的用法
"""
import random
proxies_pool=[
    {'http':'118.24.219.151:1877777'},
    {'http':'118.24.219.151:174555'},
    {'http':'118.24.219.151:174555'}
]
proxies=random.choice(proxies_pool)
print(proxies)