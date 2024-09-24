import pandas as pd


class FanQuanPiLiangZhuiZongFile:
    def FanquanPiLiangZhuiZongFile(self, file_path):
        data = pd.read_excel(file_path, keep_default_na=False, index_col=None)
        # 将“日期”列转换为datetime类型
        data["日期"] = pd.to_datetime(data["日期"])
        # 过滤掉“操作类型”列等于“采购退货”和“采购退货出库”的数据
        data = data[~data["操作类型"].isin(["采购退货", "采购退货出库"])]
        # 对“串号”进行分组，并取“日期”列数据最新的一条
        data = data.sort_values(by=["串号", "日期"]).groupby("串号").tail(1)
        data = data["串号"].values.tolist()
        print(f"泛全批量追踪的文件数据为:\n{data}")
        return data

    def scmXiaoShouchuanMaJiLu(self, file_path1, file_path2):
        scmXiaoChuanMa = pd.read_excel(file_path1, keep_default_na=False)
        scmXiaoChuanMa = scmXiaoChuanMa[["串码", "销售订单"]]
        scmXiaoChuanMa["日期"] = ""

        print(f"从SCM销售串码记录文件中读取到的数据为:\n{scmXiaoChuanMa}")
        print(f"从SCM销售串码记录文件中读取到的数据长度为:{len(scmXiaoChuanMa)}")

        scmXiaoShouDingdan = pd.read_excel(file_path2, keep_default_na=False)
        print(f"从SCM销售订单文件中读取的数据列名为:{scmXiaoShouDingdan.columns}")

        # 筛选出项目类别为Z004的数据
        scmXiaoShouDingdan = scmXiaoShouDingdan[scmXiaoShouDingdan["项目类别"] == "Z004"]

        # 检查是否包含“销售订单号”和“创建日期”列
        if "销售订单号" in scmXiaoShouDingdan.columns and "创建日期" in scmXiaoShouDingdan.columns:
            scmXiaoShouDingdan = scmXiaoShouDingdan[["销售订单号", "创建日期"]]

            # 将“创建日期”转换为所需格式
            scmXiaoShouDingdan["创建日期"] = scmXiaoShouDingdan["创建日期"].apply(lambda x: x.strftime('%Y%m'))
            print(f"从SCM销售订单文件中读取的数据为:\n{scmXiaoShouDingdan}")
            print(f"从SCM销售订单文件中读取的数据长度为:{len(scmXiaoShouDingdan)}")

            # 将销售订单列的数据中的销售订单号变成列表并作为参照匹配列
            targetList = list(scmXiaoShouDingdan["销售订单号"])

            # 更新匹配后的销售串码记录的日期
            for index, row in scmXiaoChuanMa.iterrows():
                if row["销售订单"] in targetList:
                    match_row = scmXiaoShouDingdan[scmXiaoShouDingdan["销售订单号"] == row["销售订单"]]
                    scmXiaoChuanMa.at[index, "日期"] = match_row["创建日期"].values[0]

            # 过滤出已匹配到创建日期的记录
            scmXiaoChuanMa_filtered = scmXiaoChuanMa[scmXiaoChuanMa["日期"] != ""]
            print(f"过滤后的scm销售串码中的销售订单号的数据长度为:{len(set(list(scmXiaoChuanMa_filtered['销售订单'])))}")
            print(f"在匹配完销售订单号数据文件后的scm销售串码为:\n{scmXiaoChuanMa_filtered}")
            print(f"在匹配完销售订单号数据文件后的scm销售串码数据的长度为:{len(scmXiaoChuanMa_filtered)}")
        else:
            print("SCM销售订单文件中不包含'销售订单号'或'创建日期'列")
        return scmXiaoChuanMa_filtered.values.tolist()


if __name__ == '__main__':
    file_path = r"C:\Users\ly320\Desktop\二系统稽核\泛全系统文件下载\串号全程跟踪查询报表.xlsx"
    fanquanpiliangzhuizongfileFilter = FanQuanPiLiangZhuiZongFile()
    TargetList=fanquanpiliangzhuizongfileFilter.FanquanPiLiangZhuiZongFile(file_path)
    # 读取销售订单列中全部的销售组织为z004的数据
    file_path1 = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM销售串码记录文件.xlsx'
    file_path2 = r'C:\Users\ly320\Desktop\二系统稽核\ScmDownLoad\SCM销售订单.xlsx'
    scmXiaoChuanMa_filtered=fanquanpiliangzhuizongfileFilter.scmXiaoShouchuanMaJiLu(file_path1, file_path2)
    rawDataListTargetList=[]
    for item in scmXiaoChuanMa_filtered:
        if item[0]  in TargetList:
            print(f"SCM已出库泛全未处理的数据有:{item}")
            rawDataListTargetList.append(item)
    print(f"SCM已出库泛全未处理的数据为:{rawDataListTargetList}")
    print(f"SCM已出库泛全未处理的数据的长度为:{len(rawDataListTargetList)}")
