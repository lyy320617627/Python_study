
# -------------------------------------------------
import pandas as pd


def jiabaofanli_list_item(data_list):
    for data in data_list:
        data[13] = data[13][-10:]
        # print(len(data))
    # 将列表转换为 DataFrame
    df = pd.DataFrame(data_list, columns=[
        '列1', '列2', '列3', '列4', '列5', '列6', '列7', '列8', '列9', '列10',
        '列11', '列12', '列13', '销售订单号', '列15', '列16', '列17', '列18', '列19', '列20', '列21', '列22'
    ])
    # 选中指定的三列
    selected_columns = df[['销售订单号', '列11', '列12']]
    # 将列转换为浮点数类型
    selected_columns['列11'] = selected_columns['列11'].astype(float)
    selected_columns['列12'] = selected_columns['列12'].astype(float)
    selected_columns['销售订单号'] = selected_columns['销售订单号'].astype(str)
    # 计算列12和列11的差的绝对值
    selected_columns['差额'] = (selected_columns['列12']).abs()
    # 根据销售订单号进行分组并计算差额之和
    result = selected_columns.groupby('销售订单号')['差额'].sum().reset_index()
    # 重命名列
    result.columns = ['销售订单号', '差额']
    dataList = result.values.tolist()
    print(result)
    return dataList


data_list = [
    ['', 'hs13738111178', '0080290698', '桐庐县城南街道宏胜通讯器材商店', '2024年06月', '', '', '', '', '1', '2.00',
     '2.00', '', '客户退货5000722558', '价保返利退款', '', '2024年06月', '审核通过', '', '正常',
     '客户退货5000722558', ''],
    ['', 'Cmdc80191048', '0080191048', '话机世界通信集团股份有限公司', '2024年05月', '', '', '', '', '1', '2185.82',
     '2185.82', '202405101139000375916', '5000855584', '价保返利退款', '', '2024年05月', '审核通过', '', '正常',
     '客户退货5000855584', '']
]
result = jiabaofanli_list_item(data_list)
print(result)
if __name__ == '__main__':
    data_list=[1,2,3,4,5,6,7,8,9,10]
    data_list2=[1,2,3,4,5,6,7,8,9,10,11]
    total_list=data_list+data_list2
    print(total_list)