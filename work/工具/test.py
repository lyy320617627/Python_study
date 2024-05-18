# -*- encoding: utf-8 -*-
import os

import pymysql
import xlwt
import numpy as np
import pandas as pd
import openpyxl


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


if __name__ == "__main__":
    conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")

    #conn2 = MySQLUtil(host="127.0.0.1",port=3306, user="root", passwd="abc123", db="gsqd")
    file_path=None
    data=conn2.select_all("bs_rtime_oper_eff_warn")
    # data=data[3:-1]
    data=list(data)
    list_data=[]
    for data2 in data:
        list_data.append(data2[2:])
    print(list_data)
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


    file_path='C:\\Users\\ly320\\Desktop\\test.xlsx'

    write=pd.ExcelWriter(file_path)

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
    write._save()
    name_list=[]
    delay_time_list=[]
    warn_status_list=[]
    excel_list=['接单','拣配','复核','包装','发货']
    for j in excel_list:
        # delay_time=pd.read_excel(file_path,sheet_name=j,keep_default_na=False,index_col=False,skiprows=1,usecols='E',nrows=1)
        # delay_time=delay_time.iloc[0,0]
        # print(f"delay_time:{delay_time}")
        # if  delay_time.empty:
        #     delay_time=None
        # warn_status=pd.read_excel(file_path,sheet_name=j,keep_default_na=False,index_col=False,skiprows=1,usecols='D',nrows=1)
        # warn_status=warn_status.iloc[0,0]
        # print(f"warn_status:{warn_status}")
        # if  warn_status.empty:
        #     warn_status=None
        df=pd.read_excel(file_path,sheet_name=j,usecols='D:X',keep_default_na=False).astype("str")
        file_path1='C:\\Users\\ly320\\Desktop\\'+j+'.xlsx'
        name_list.append(file_path1)
        # delay_time_list.append(delay_time)
        # warn_status_list.append(warn_status)
        df.to_excel(file_path1,index=False)
    print(name_list)
    print(f"超时时间的列表是:{list(delay_time_list)}")
    print(f"警告情况是:{list(warn_status_list)}")






