"""
通过代码演示Python类中内置方法的使用
"""
class Person:
    def __init__(self,name,age,tel):
        self.name = name
        self.age = age
        self.tel = tel
    # 当我们直接输出对象时，输出的是对象的内存地址
    # 我们可以通过修改__str__方法来修改输出对象时输出对的语句
    def __str__(self):
        return f"{self.name} is {self.age} years,tel is: {self.tel}"
    # __lt__小于符号的比较
    # 当我们直接比较两个对象时，会报错，我们可以通过修改__lt__方法来修改比较的规则
    def __lt__(self, other):
        return self.age<other.age
    # 定义两个对象之间使用<=或者>=方法时的比较原则
    def __le__(self, other):
        return self.age<=other.age
    # 定义两个对象之间使用==符号进行比较的原则
    # 方法：__eq__(slef,other):
    def __eq__(self, other):
        return self.age==other.age
if __name__ == '__main__':
    p1=Person("lyy",18,"123456")
    print(p1)
    p2=Person("zmk",19,"111")
    print(p1<p2)
    print(p1==p2)
