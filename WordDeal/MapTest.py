import json
from pyecharts.charts import Map
from pyecharts.options import *

# 读取数据文件
with open("D:/疫情.txt", "r", encoding="UTF-8") as f:
    data = f.read()

# 将字符串json转换为python的字典
data_dict = json.loads(data)
province_data_list = data_dict["areaTree"][0]["children"]

# 各地区数据
region_data = {
    "华北地区": ["北京", "天津", "河北", "山西", "内蒙古"],
    "华东地区": ["上海", "江苏", "浙江", "安徽", "福建", "江西", "山东"],
    "东北地区": ["辽宁", "吉林", "黑龙江"],
    "华中地区": ["河南", "湖北", "湖南"],
    "华南地区": ["广东", "广西", "海南"],
    "西南地区": ["重庆", "四川", "贵州", "云南", "西藏"],
    "西北地区": ["陕西", "甘肃", "青海", "宁夏", "新疆"],
}

# 计算各地区确诊总人数
region_confirm = {}
for region, provinces in region_data.items():
    region_confirm[region] = sum(
        province_data["total"]["confirm"]
        for province_data in province_data_list
        if province_data["name"] in provinces
    )

# 转换为 pyecharts 的数据格式
data_list = list(region_confirm.items())

# 创建地图对象
map = Map()

# 添加数据，并隐藏省份名字
map.add(
    "各地区确诊人数",
    data_list,
    "china",
    label_opts=LabelOpts(is_show=False)  # 隐藏省份名字
)

# 设置全局配置，定制分段的视觉映射
map.set_global_opts(
    title_opts=TitleOpts(
        title="全国疫情地图",
        pos_left="center"  # 标题居中
    ),
    visualmap_opts=VisualMapOpts(
        is_show=True,  # 是否显示
        is_piecewise=True,  # 是否分段
        pieces=[
            {"min": 1, "max": 99, "label": "1~99人", "color": "#CCFFFF"},
            {"min": 100, "max": 999, "label": "100~999人", "color": "#FFFF99"},
            {"min": 1000, "max": 4999, "label": "1000~4999人", "color": "#FF9966"},
            {"min": 5000, "max": 9999, "label": "5000~9999人", "color": "#FF6666"},
            {"min": 10000, "max": 99999, "label": "10000~99999人", "color": "#CC3333"},
            {"min": 100000, "label": "100000+", "color": "#990033"},
        ]
    ),
    tooltip_opts=TooltipOpts(
        is_show=True,
        formatter=lambda x: x.name + ": " + str(x.value) if x.value else "无数据"
    )
)

# 绘图
map.render("全国疫情地图.html")
