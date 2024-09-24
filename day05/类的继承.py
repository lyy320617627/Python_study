""""
通过代码演示类的继承的使用
继承的方式:
# 方式一：单继承
class class1(class2):
其中class2表明是继承的类
其中class2叫做父类
class1叫做子类+
# 方式二：多继承
class class_sub(class1,class2,class3):
表明子类class_sub同时继承多个类
当继承的多个类中含有共同的属性和方法时，优先级class1>class2>class3,即谁先来的谁优先
"""
# 父类的定义
class Phone:
    IMEI=None
    producer="HM"
    def call_by_4g(self):
        print("已经开启4g通话")
class Phone2022(Phone):
    face_id=True
    def call_by_5g(self):

        print("2022年已经支持5g通话")
if __name__ == '__main__':
    phone=Phone2022()
    producer=phone.producer="LYY"
    print(producer)
