# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块
import locale

import pymysql
import requests
from datetime import datetime, timedelta
import time
# -*- encoding: utf-8 -*-

import pymysql


# from basic.config import DbConfig


class MySQLUtil:
    """
    MySQL工具类
    """

    def __init__(self, host="127.0.0.1", port=3306, user=None, passwd=None, db=None, charset="utf8", *args, **kwargs):
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
        self.__conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset, *args,
                                      **kwargs)
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

    def execute(self, sql_cmd, data=None):
        try:
            if None == data:
                self._getCursor().execute(sql_cmd)
            else:
                self._getCursor().execute(sql_cmd, data)
            self.__conn.commit()
            data = self._getCursor().fetchall()
            return data
        except Exception:
            self.__conn.rollback()
            return None

    def executemany(self, sql, ins_dataList):
        try:
            self._getCursor().executemany(sql, ins_dataList)
            self.__conn.commit()
            data = self._getCursor().fetchall()
            return data
        except Exception as e:
            print("发生异常：", str(e))
            self.__conn.rollback()
            raise  # 往上继续抛出
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
            print("insert sql:", sql)
        return self.execute(sql)

    def batchInsert(self, table, keyList, ins_dataList):
        str = ''
        keys = ''
        for item in keyList:
            str = str + '%s,'
            keys = keys + item + ','
        str = str[0:len(str) - 1]
        keys = keys[0:len(keys) - 1]

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
            sql = "UPDATE {table} SET {values} WHERE {condition}".format(table=table, values=update_data,
                                                                         condition=condition_data)
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

    def createDbConn(self):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # mysqlUtil = MySQLUtil(host="v35921399s.yicp.fun",port=45246, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        return mysqlUtil

    def insertOrUpdateFinishTime(self, programeName):
        mysqlUtil = self.createDbConn()
        # 使用INSERT ON DUPLICATE KEY UPDATE插入或更新数据
        # 获取当前时间
        current_time = datetime.now()
        dataList = []
        item = [programeName, current_time]
        dataList.append(item)
        print(dataList)
        sql = """
            INSERT INTO yindao_program_finished_time (
                yingdao_program_name, update_time
            ) VALUES (
                %s, %s
            ) ON DUPLICATE KEY UPDATE
                update_time = VALUES(update_time);
        """
        try:
            mysqlUtil.executemany(sql, dataList)
        except ValueError:
            print(ValueError)
            raise  # 往上继续抛出
    # 检查指定应用程序的最新当前时间跟更新时间比是否正常，超过一个小时则判断为不正常


if __name__== "__main__":
    access_token='Bearer 599e482c-ac9a-45c8-a85d-e680c9b04e45'
    conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    url = 'https://api.yingdao.com/api/console/app/queryAppUseRecordList'
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    data = conn2.select_all("yindao_program_base_info")
    data = list(data)
    program_list_takeTime = []
    program_list = []
    for row in data:
        uuid = row[1]
        appName = row[2]
        tel_num = row[4]
        start_time = row[7]
        end_time = row[8]
        data = {
            "page": 1,
            "size": 1,
            "appId": uuid
        }
        response = requests.post(url, headers=headers, json=data)
        runstateName = (response.json()['data'][0]['runStatusName'])

        if runstateName == "运行中":
            row_list = [appName, tel_num, runstateName, start_time, end_time]
            program_list.append(row_list)
        # else:
        #     conn2.insertOrUpdateFinishTime(str(appName))
    print(program_list)
    current_time=datetime.now()
    print(f"current_time:{current_time}")
    formatted_time = current_time.strftime("%H:%M:%S")
    print(f"formatted_time：{formatted_time}")
    hours, minutes, seconds = map(int, formatted_time.split(":"))
    time_interval_from_str = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    print(type(formatted_time))
    for program in program_list:
        print(program[0])
        print(type(program[3]))
        print(type(program[4]))


        if program[3]<=time_interval_from_str and time_interval_from_str<=program[4]:
            print(f"{program[0]},继续循环")




