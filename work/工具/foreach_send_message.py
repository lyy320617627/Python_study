from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib, os, time
import requests, json, os, time, re
from email.mime.image import MIMEImage
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
    def send_message(file_path1):
        # 1.获取接口凭证
        def getAccess_token():
            # 从小程序应用信息处获取
            appkey = 'dingc8wtmaib95vi3ifz'  # 不要配置服务器ip
            appsecret = 'XR4vKpX7Wt4iLK2WE-1IbI_THLwaynDYC6Be0j0j9Fl3e_ev39P9WRu_Fin4GhFt'  # 不要配置服务器ip

            url = 'https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s' % (appkey, appsecret)

            headers = {
                'Content-Type': "application/x-www-form-urlencoded"
            }
            data = {'appkey': appkey,
                    'appsecret': appsecret}
            r = requests.request('GET', url, data=data, headers=headers)
            access_token = r.json()["access_token"]

            return access_token

        # 2.获取Midia_id
        def getMedia_id(file_path):
            access_token = getAccess_token()
            # 本地文件的绝对路径
            url = r'https://oapi.dingtalk.com/media/upload?access_token=%s&type=file' % access_token
            files = {'media': open(file_path, 'r')}
            data = {'access_token': access_token,
                    'type': 'file'}
            response = requests.post(url, files=files, data=data)
            json = response.json()
            print(json["media_id"])
            return json["media_id"]

        # 3.文件发送
        def SendFile():
            access_token = getAccess_token()

            # 循环获取指定列表文件，发送指定钉钉群聊

            file_path = file_path1
            # file_path=r"C:\Users\RPA1-1\Desktop\OAO自动生成通报表格\固定表格模板.xlsx"

            print(file_path)
            # 将文件名传给getMedia_id
            media_id = getMedia_id(file_path)
            # 获取群聊Id
            chatid = 'chat58714d2798355e1f579ebe9c09958a2f'
            url = 'https://oapi.dingtalk.com/chat/send?access_token=' + access_token
            header = {
                'Content-Type': 'application/json'
            }
            data = {'access_token': access_token,
                    'chatid': chatid,
                    'msg': {
                        'msgtype': 'file',
                        'file': {'media_id': media_id}
                    }
                    }
            r = requests.request('POST', url, data=json.dumps(data), headers=header)
            print(r.json())
            print('发送成功')
        SendFile()
        conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        my_tuple = file_path1.split('.')
        print(f"分割之后的数组是：{my_tuple}")
        program_name = my_tuple[0][-2:]
        print(program_name)
        target_list = conn2.get_warn_or_timeout('bs_rtime_oper_eff_warn', program_name)
        print(f"warn_sitution={target_list[0][0]}")
        print(f"delay_time={target_list[0][1]}")
        return(f"{program_name} 环节 ，超{target_list[0][1]}时未处理:{target_list[0][0]}请及时处理")
def concat():
    concat_list=['18458125250','13605810514']
    return concat_list



