"""
通过代码演示对私有成员方法和私有成员属性的使用
# 私有成员方法无法直接被类对象使用
# 私有变量无法赋值，也无法获取值
# 私有成员无法被类对象使用，但是可以被其他的成员使用
"""
class Phone:
    __colvatage=0 # 定义类的私有属性
    def __run_by_singleCore(self):
        return print(f'手机已经进入单核运行模式')
    def call_by_5g(self):
        if self.__colvatage>=1:
            print(f"当前电压为{self.__colvatage},满足5g通话要求，已经开启5g通话")
        else:





            print(f"当前电压为{self.__colvatage},不满足5g通话要求")
if __name__ == '__main__':
    p1=Phone()
    p1.call_by_5g()


