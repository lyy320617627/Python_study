from MySQLUtil import MySQLUtil
from datetime import datetime, timedelta
import time
#
#author:henry date:20240508 desc: 影刀应用运行完成后，调用该程序，写入或者更新yindao_program_finished_time表。
#
class yindaoProgram:
    def createDbConn(self):
        mysqlUtil = MySQLUtil(host="172.16.8.241", user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        # mysqlUtil = MySQLUtil(host="v35921399s.yicp.fun",port=45246, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        return mysqlUtil
    def insertOrUpdateFinishTime(self,programeName):
        mysqlUtil = self.createDbConn()
        # 使用INSERT ON DUPLICATE KEY UPDATE插入或更新数据
        # 获取当前时间
        current_time = datetime.now()
        dataList = []
        item=[programeName,current_time]
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
            mysqlUtil.executemany(sql,dataList)
        except ValueError:
            print(ValueError)
            raise#往上继续抛出
    #检查指定应用程序的最新当前时间跟更新时间比是否正常，超过一个小时则判断为不正常
    def checkYindaoProgramFinishTimeIsOk(self,yingdao_program_name):
        sql = """
            SELECT update_time FROM yindao_program_finished_time
            WHERE yingdao_program_name = %s
        """
        mysqlUtil = self.createDbConn()
        row = mysqlUtil.execute(sql,yingdao_program_name)
        print(row)
        # print(row[0][0])
        # 检查是否查询到了数据
        if row:
            print(row[0][0])
            update_time = row[0][0]
            print(update_time)
            # 计算时间差
            time_diff = datetime.now() - update_time
            print(f"time_diff:{time_diff}")
            # 检查是否超过一个小时
            if time_diff > timedelta(hours=1):
                return yingdao_program_name+"失败：update_time超过一个小时"
            else:
                 return yingdao_program_name+"失败：update_time超过一个小时"
        else:
            return yingdao_program_name+"失败：update_time超过一个小时"
        # return message



if __name__ == "__main__":
    print(f"当前时间："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
    yindaoProgram1 = yindaoProgram()
    # result = yindaoProgram.insertOrUpdateFinishTime("多部门数字大屏-数据支撑-第二代")
    conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
    table='yindao_program_base_info'
    data=conn2.select_all(table)
    program_name_list=[]
    for data1 in data:
        program_name_list.append(data1[2])
    print(f"program_name_list:{program_name_list}")
    print("---------------------------------------------")
    for program_name in program_name_list:
        yindaoProgram1.insertOrUpdateFinishTime(program_name)
        message=yindaoProgram1.checkYindaoProgramFinishTimeIsOk(program_name)
        print(message)
        # print(f"检查是否插入成功的结果是：{message}")

    # result = yindaoProgram.checkYindaoProgramFinishTimeIsOk("多部门数字大屏-数据支撑-第二代")
    # print(result)
    # print(f"当前时间："+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))