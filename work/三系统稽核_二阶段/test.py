import pandas as pd


def GetFinallyExcelFile(dataList, FinallyExcelPath):
    # 创建 DataFrame
    df = pd.DataFrame(dataList,
                      columns=['渠道商名称', '渠道商编码', 'scm余额', '惠购+和动力余额', '同步失败订单', '惠购生态订单',
                               '本次差异金额', '上次差异金额', '两次差异金额', '差异原因', '上次差异原因'])

    # 去重
    df = df.drop_duplicates()

    # 定义汇总函数
    def aggregate_reason(group):
        group['差异原因'] = ' '.join(group['差异原因'].unique())
        return group.iloc[0]

    # 根据渠道商编码分组，并汇总差异原因
    grouped_df = df.groupby('渠道商编码').apply(aggregate_reason).reset_index(drop=True)

    # 保存到 Excel 文件
    grouped_df.to_excel(FinallyExcelPath, index=False)


if __name__ == '__main__':
    dataList = [
        # 示例数据
        ['渠道商A', '001', 100, 200, 1, 2, 300, 400, 700, '原因1', '上次原因1'],
        ['渠道商B', '002', 150, 250, 1, 3, 400, 500, 900, '原因2', '上次原因2'],
        ['渠道商A', '001', 200, 300, 2, 4, 500, 600, 1100, '原因3', '上次原因3'],
        # 更多数据...
    ]
    FinallyExcelPath = r'C:\Users\ly320\Desktop\FinallyExcelFile.xlsx'
    GetFinallyExcelFile(dataList, FinallyExcelPath)
