from pymysql import Connect
class Mysql:
    conn=Connect(
        host="localhost",
        port=3306,
        user='root',
        password="abc123")

if __name__ == '__main__':
    conn=Mysql.conn
    print(Mysql.conn.get_server_info())
    # 执行非查询的语句
    cursor=conn.cursor()
    conn.select_db("test")
    # 注意：执行sql语句时，需要通过游标来执行
    # cursor.execute("create table Py_mysql(id int);")
    cursor.execute("select * from gsqd;")
    # 对数据库中的数据有修改时，需要通过连接对象进行修改
    conn.commit()
    #获取查询的结果数据
    result:tuple=cursor.fetchall()
    print(result)
    conn.close()
    #执行查询的dql语句，需要通过游标调用execute方法来实现


