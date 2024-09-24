"""
通过代码演示对父类中的属性进行复写的方法、
当子类对父类中的属性进行重写时，则新创建的类中的属性以重写之后的为准
即：在子类中重新定义同名的属性或者方法即可
重写父类中的方法或者属性之后，如果还想要调用父类中的方法或者属性的方法
方式一：
        使用父类成员
        使用成员变量：父类名.成员变量
        使用成员方法:父类名.成员方法(self）
方式二:
        使用super()调用父类成员
        使用成员变量：super().成员变量
        使用成员方法:super().成员方法()
"""
class Person(object):
    name="lYY"
    age=18
    tel="987654321"
    def PersonInfo(self):
        print("name:",self.name,"age:",self.age,"tel:",self.tel,)
class Student(Person):
    name="zmk"
    age=22
    tel="9876543210"
    def PersonInfo(self):
        # 方式一：通过父类名直接调用
        print(f"父类的名字是：{Person.name}")
        #方式二:
        print(f"父类中的年龄是:{super().age}")
        print(f"name:{self.name},age:{self.age},tel:{self.tel}")
if __name__ == '__main__':
    st1=Student()
    st1.PersonInfo()
    print(st1.name)
