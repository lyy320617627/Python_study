"""
演示对象的创建和构造方法的使用
Python类可以使用:_init_()方法，称之为构造方法
可以实现：
        在创建类对象(构造类)的时候，会自动执行
        在创建类对象(构造类)的时候，将传入参数自动传递给_init_方法使用
"""
class Person:
    name=None
    age=None
    tel=None
    # 在类的声明中也可以不用声明属性，即在构造方法中声明，这样的话就相当于同时声明变量并且赋值
    def __init__(self,name,age,tel):
        self.name=name
        self.age=int(age)
        self.tel=tel

if __name__ == '__main__':
    p1=Person("lyy",18,"123456")
    print(p1.name)

