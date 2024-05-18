# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块


import pymysql
import json
import pandas as pd
import xlwt
import numpy as np
import openpyxl
# -*- encoding: utf-8 -*-

import pymysql
# from basic.config import DbConfig


class MySQLUtil:
    """
    MySQL工具类
    """
    def __init__(self, host="127.0.0.1",port=3306,user=None, passwd=None, db=None, charset="utf8", *args, **kwargs):
        # print('对象的创建')
        # try:
        #     self.__host = host
        #     self.__user = user
        #     self.__passwd = passwd
        #     self.__db = db
        #     self.__conn = pymysql.connect(host, user, passwd, db, charset=charset, *args, **kwargs)
        #     self.__cursor = self.__conn.cursor()
        #     if self.__conn is None or self.__cursor is None:
        #         raise Exception('Error while connect to database.')
        # except Exception as e:
        #     raise e
        self.__host = host
        self.__port = port
        self.__user = user
        self.__passwd = passwd
        self.__db = db
        self.__conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db,port=port, charset=charset, *args, **kwargs)
        self.__cursor = self.__conn.cursor()

    def __del__(self):
        # print('对象的销毁')
        self.__cursor.close()
        self.__cursor = None
        self.__conn.close()
        self.__conn = None

    def _getConnection(self):
        if self.__conn is not None:
            return self.__conn

    def _getCursor(self):
        if self.__cursor is not None:
            return self.__cursor

    def _deal_values(self, value):
        if isinstance(value, str):
            value = ("{value}".format(value=value))
        elif isinstance(value, dict):
            result = []
            for key, value in value.items():
                value = self._deal_values(value)
                res = "{key}={value}".format(key=key, value=value)
                result.append(res)
            return result
        else:
            value = (str(value))
        return value

    def execute(self, sql_cmd,data=None):
        try:
            if None == data:
                self._getCursor().execute(sql_cmd)
            else:
                self._getCursor().execute(sql_cmd,data)
            self.__conn.commit()
            data = self._getCursor().fetchall()
            return data
        except Exception:
            self.__conn.rollback()
            return None
    def executemany(self, sql , ins_dataList):
        try:
            self._getCursor().executemany(sql,ins_dataList)
            self.__conn.commit()
            data = self._getCursor().fetchall()
            return data
        except Exception as e:
            print("发生异常：", str(e))
            self.__conn.rollback()
            raise#往上继续抛出
            return None
    def insert(self, table, ins_data):
        sql = ''
        for data in ins_data:
            key = ','.join(data.keys())
            values = map(self._deal_values, data.values())
            ins_data = ', '.join(values)
            sql = "INSERT INTO {table}({key}) VALUES ({val})".format(
                table=table,
                key=key,
                val=ins_data
            )
            print("insert sql:",sql)
        return self.execute(sql)

    def batchInsert(self, table,keyList, ins_dataList):
        str = ''
        keys = ''
        for item in keyList:
            str = str+'%s,'
            keys = keys+item+','
        str = str[0:len(str)-1]
        keys = keys[0:len(keys)-1]

        sql = "INSERT INTO {table}({keys}) VALUES ({str})".format(
            table=table,
            keys=keys,
            str=str
        )
        return self.executemany(sql, ins_dataList)

    def update(self, table, data, condition=None):
        update_list = self._deal_values(data)
        update_data = ",".join(update_list)
        if condition is not None:
            condition_list = self._deal_values(condition)
            condition_data = ' AND '.join(condition_list)
            sql = "UPDATE {table} SET {values} WHERE {condition}".format(table=table, values=update_data, condition=condition_data)
        else:
            sql = "UPDATE {table} SET {values}".format(table=table, values=update_data)
        return self.execute(sql)

    def select(self, table, filed, value):
        sql = "SELECT * FROM {table} WHERE {filed} = '{value}'".format(table=table, filed=filed, value=value)
        return self.execute(sql)

    def select_all(self, table):
        sql = "SELECT * FROM {table}".format(table=table)
        return self.execute(sql)

    def delete(self, table, condition={}):
        condition_list = self._deal_values(condition)
        condition_data = ' AND '.join(condition_list)
        sql = "DELETE FROM {table} {where} {condition}".format(
            table=table,
            where='' if condition_data == '' else 'WHERE',
            condition=condition_data
        )
        return self.execute(sql)
    def get_warn_or_timeout(self,table,program_name):
        sql=" SELECT warn_situation,Timeout FROM {table} WHERE order_status='{program_name}' limit 1".format(table=table,program_name=program_name)
        return self.execute(sql)

if __name__ == "__main__":
    conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    new_file_path='C:\\Users\\ly320\\Desktop\\test12.xlsx'
    print(new_file_path)
    data=conn2.select_all("bs_rtime_oper_eff_warn")
    data = list(data)
    list_data=[]
    for data2 in data:
        list_data.append(data2[2:])
    new_list = ['订单环节', '警告情况', '超时', '发货仓库', '移出货主', '移出库存地', '指令类型', '指令编号',
                '指令行项|交货序号', '数量', '业务执行状态', '移出物料'
        , '物料描述', '运单编号', '承运商名称', '售达方编号', '售达方名称', '收货人', '电话1', '省份描述', '城市描述',
                '地区描述', '收货地址', '创建日期']
    take_order_list=[]# 接单列表
    take_order_list.append(new_list)
    shipments_list=[] # 发货列表
    shipments_list.append(new_list)
    arrangement_list=[] # 拣配列表
    arrangement_list.append(new_list)
    review_list=[]     #复核列表
    review_list.append(new_list)
    wrap_list=[]       #包装列表
    wrap_list.append(new_list)
    shipments_list =[]  # 发货列表
    shipments_list.append(new_list)
    for i in list_data:
        if i[0]=='接单':
            take_order_list.append(list(i))
        elif i[0]=='拣配':
            arrangement_list.append(list(i))
        elif i[0]=='复核':
            review_list.append(list(i))
        elif i[0]=='包装':
            wrap_list.append(list(i))
        elif i[0]=='发货':
            shipments_list.append(list(i))
    write=pd.ExcelWriter(new_file_path)
    data_1=pd.DataFrame(list_data)
    data_2=pd.DataFrame(data=take_order_list)
    data_3=pd.DataFrame(data=arrangement_list)
    data_4=pd.DataFrame(data=review_list)
    data_5=pd.DataFrame(data=wrap_list)
    data_6=pd.DataFrame(data=shipments_list)
    data_1.to_excel(write,sheet_name='sheet1',float_format='%.2f',header=False,index=False)
    data_2.to_excel(write,sheet_name='接单',float_format='%.2f',header=False,index=False)
    data_3.to_excel(write,sheet_name='拣配',float_format='%.2f',header=False,index=False)
    data_4.to_excel(write,sheet_name='复核',float_format='%.2f',header=False,index=False)
    data_5.to_excel(write,sheet_name='包装',float_format='%.2f',header=False,index=False)
    data_6.to_excel(write,sheet_name='发货',float_format='%.2f',header=False,index=False)
    write.close()
    delay_time_list=[]
    name_list=[]
    excel_list=['接单','拣配','复核','包装','发货']
    for j in excel_list:
        df=pd.read_excel(new_file_path,sheet_name=j,usecols='D:X').astype("str")
        # new_list=['订单环节','警告情况','超时','发货仓库','移出货主','移出库存地','指令类型','指令编号','指令行项|交货序号','数量','业务执行状态','移出物料'
        #     ,'物料描述','运单编号','承运商名称','售达方编号','售达方名称','收货人','电话1','省份描述','城市描述','地区描述','收货地址','创建日期']
        # df._append(new_list,ignore_index=True)
        file_path1=new_file_path+j+'.xlsx'
        name_list.append(file_path1)
        df.to_excel(file_path1,index=False)
    print(name_list)

    # for j in excel_list:
    #     target_list=conn2.get_warn_or_timeout('bs_rtime_oper_eff_warn',j)
    #     warn_sitution=target_list[0][0]
    #     delay_time=target_list[0][1]
    #     print(f"warn_sitution:{warn_sitution}")
    #     print(f"delay_time:{delay_time}")
    #     print(type(target_list))
    #     print(target_list)
    excel_list = ['C:\\Users\\ly320\\Desktop\\接单.xlsx', 'C:\\Users\\ly320\\Desktop\\.xlsx',
                  'C:\\Users\\ly320\\Desktop\\复核.xlsx', 'C:\\Users\\ly320\\Desktop\\.xlsx',
                  'C:\\Users\\ly320\\Desktop\\发货.xlsx']
    for i in excel_list:
        data = pd.read_excel(i)
        num_rows = data.shape[0]
        if num_rows==0:
            excel_list.remove(i)
        # print(f"行数：{num_rows}")
    print(excel_list)

    for i in excel_list:
        my_tuple=i.split('.')
        print(f"分割之后的数组是：{my_tuple}")
        program_name=my_tuple[0][-2:]
        print(program_name)
        target_list=conn2.get_warn_or_timeout('bs_rtime_oper_eff_warn',program_name)
        print(f"warn_sitution={target_list[0][0]}")
        print(f"delay_time={target_list[0][1]}")

        print(f"{program_name} 环节 ，超{target_list[0][1]}时未处理:{target_list[0][0]}请及时处理")




















def  for_each_list():
    excel_list=['C:\\Users\\ly320\\Desktop\\test12.xlsx接单.xlsx', 'C:\\Users\\ly320\\Desktop\\test12.xlsx拣配.xlsx', 'C:\\Users\\ly320\\Desktop\\test12.xlsx复核.xlsx', 'C:\\Users\\ly320\\Desktop\\test12.xlsx包装.xlsx', 'C:\\Users\\ly320\\Desktop\\test12.xlsx发货.xlsx']
    for i in excel_list:
        data=pd.read_excel(i)
        num_rows=data.shape[0]
        print(f"行数：{num_rows}")