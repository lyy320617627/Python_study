import pandas as pd
def ScmLowerFileFilter(excel_path):
    data = pd.read_excel(excel_path, index_col=None,  dtype={'客户': str, '销售订单号': str}, keep_default_na=False)
    print(data)
    print(data.columns)
    data['一机两票金额'] = data['一机两票金额'].astype(float)
    data['订单金额'] = data['订单金额'].astype(float)
    data['客户'] = data['客户'].astype(str)
    data['销售订单号'] = data['销售订单号'].astype(str)
    data=data[((data["订单拒绝原因"]!="00") & (data["订单拒绝原因"]!="01")) & (data["创建人"]!="RFCUSER") ]
    # 选中指定的四列
    selected_columns = data[['客户','销售订单号', '一机两票金额', '订单金额']]

    # 根据销售订单号进行分组并计算差额
    result = selected_columns.groupby(['客户', '销售订单号']).apply(
        lambda x: abs((x['订单金额'] - x['一机两票金额']).sum())
    ).reset_index()
    # 将列转换为浮点数类型
    # 重命名列
    result.columns = ['客户','销售订单号', '差额']
    result.values.tolist()
    return result
excel_path = r'C:\Users\ly320\Desktop\三系统余额稽核二阶段\scmLower\24.6.12-1.xlsx'
result=ScmLowerFileFilter(excel_path)
print(result)