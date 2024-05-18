import  pymysql
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
def main(name_list):
    conn2 = MySQLUtil(host="192.168.0.148", port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    my_tuple = name_list.split('.')
    print(f"分割之后的数组是：{my_tuple}")
    program_name = my_tuple[0][-2:]
    print(program_name)
    target_list = conn2.get_warn_or_timeout('bs_rtime_oper_eff_warn', program_name)
    print(f"warn_sitution={target_list[0][0]}")
    print(f"delay_time={target_list[0][1]}")
    return (f"{program_name} 环节 ，超{target_list[0][1]}时未处理:{target_list[0][0]}请及时处理")