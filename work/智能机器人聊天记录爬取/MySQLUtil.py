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


if __name__ == "__main__":

    # print(DbConfig.dbinfo)

    # mysqlUtil = MySQLUtil("127.0.0.1", "root", "123456", "huohua")
    # mysqlUtil = MySQLUtil(host="127.0.0.1", user="root", passwd="123456", db="test")
    # mysqlUtil = MySQLUtil(host="v35921399s.yicp.fun",port=45246, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    url = 'https://api.yingdao.com/api/console/app/queryAppUseRecordList'
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    #conn2 = MySQLUtil(host="127.0.0.1",port=3306, user="root", passwd="abc123", db="gsqd")
    data=conn2.select_all("yindao_program_base_info")
    data=list(data)
    print(type(data))
    print(data)
    for row in data:
        uuid=row[1]
        appName=row[2]
        tel_num=row[4]
        data={
            "page":1,
            "size":1,
            "appId":uuid
        }
        response=requests.post(url,headers=headers,json=data)
        runstateName = (response.json()['data'][0]['runStatusName'])
        if runstateName != "运行中":
            row_list = [appName, tel_num, runstateName]
            program_list.append(row_list)



    # mysqlUtil.get_version()
    # dbs = mysqlUtil.list_databases()
    # print(dbs)
    # conn = mysqlUtil.get__conn()
    # mysqlUtil.select_db("huohua")
    # print(type(conn.db), conn.db)
    # databases = mysqlUtil.list_databases()
    # print(type(databases), databases)
    # tables = mysqlUtil.list_tables()
    # print(type(tables), tables)
    # sql = "SELECT * FROM test_user"
    # result = mysqlUtil.execute(sql)
    # for i in result:
    #     print(i)
    # result = mysqlUtil.table_metadata("huohua", "test_user")
    # for i in result:
    #     print(i)
    # result = mysqlUtil.get_table_fields("huohua", "test_user")
    # for i in result:
    #     print(i)
