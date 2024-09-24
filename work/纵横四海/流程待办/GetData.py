from MySQLUtil import MySQLUtil
class GetData:
    def getData(self):
        conn2 = MySQLUtil(host="192.168.0.148",port=3306, user="ZSD", passwd="Cmdc2023", db="zhelixing_data")
        data=conn2.select_all("bs_pur_purchase_result_bill")
        # print(f"从数据库bs_pur_purchase_result_bill中查询出来的数据为:{data}")
        print(f"从数据库bs_pur_purchase_result_bill中查询出来的数据类型为:{type(data)}")
        print(f"从数据库bs_pur_purchase_result_bill中查询出来的数据总数是{len(data)}")
        TodoList=[]
        data=list(data)
        for item in data:
            if item[-3]=="是" and item[7]=="流转中":
                TodoList.append(item)
        print(f"需要待办的数据长度是:{len(TodoList)}")
        return TodoList
if __name__ == '__main__':
    getdata=GetData()
    TodoList=getdata.getData()

