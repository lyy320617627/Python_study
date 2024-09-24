
from DataCollection import DataCollection
from MySQLUtil import MySQLUtil
class DataLoadUpToDataBase:
    def __init__(self,dataList):
        self.__conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        self.dataList=dataList

    def dataLoadUpToDataBase(self):
        execute_query = """
        INSERT INTO bs_ref_environment_data (curr_date, curr_time,deviceAddress,deviceName, temperature, humidity)
        VALUES (CURRENT_DATE(), CURRENT_TIME(), %s,%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        deviceAddress=VALUES(deviceAddress),
        deviceName = VALUES(deviceName),
        temperature = VALUES(temperature),
        humidity = VALUES(humidity)
        """
        self.__conn2.executemany(execute_query, self.dataList)
        sql="CALL proc_bs_LargeScreen();"
        self.__conn2.execute(sql)
if __name__ == '__main__':
    FinaldeviceInfoList = {}
    User = [{
        "username": "h230221zhej",
        "password": "h230221zhej"
    }, {
        "username": "zhejiang",
        "password": "zhejiang2023"
    }]
    for user in User:
        dataCenter = DataCollection(user["username"], user["password"])
        dataCenter.getDeviceList()
        dataCenter.getRealTimeDataByDeviceAddr()
        deviceInfoList = dataCenter.deviceInfoListDict
        if deviceInfoList:
            for key, values in deviceInfoList.items():
                print(f"{key}:{values}")
                FinaldeviceInfoList[key] = values
    dataList=[]
    for key, values in FinaldeviceInfoList.items():
        if values["deviceAddrs"]=="10053452":
            data=[values["deviceAddrs"],"电气与光学性能检测室A区",values["温度"],values["湿度"]]
        elif values["deviceAddrs"]=="10053466":
            data=[values["deviceAddrs"],"力学实验室-1",values["温度"],values["湿度"]]
        elif values["deviceAddrs"]=="10053475":
            data=[values["deviceAddrs"],"力学实验室-2",values["温度"],values["湿度"]]
        elif values["deviceAddrs"]=="10053424":
            data=[values["deviceAddrs"],"力学实验室-3",values["温度"],values["湿度"]]
        else:
            data=[values["deviceAddrs"],key,values["温度"],values["湿度"]]
        dataList.append(data)
        print(f"{key}:{values}")
    print(f"dataList:\n{dataList}")
    dataLoadUpToDataBase=DataLoadUpToDataBase(dataList)
    dataLoadUpToDataBase.dataLoadUpToDataBase()
