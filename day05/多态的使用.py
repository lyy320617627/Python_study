"""
通过代码演示对多态的理解
多态：指的是多种状态，即完成某个行为时，使用不同的对象会得到不同的状态
抽象类：什么是抽象类(接口)
     包含抽象方法的类，称之为抽象类。抽象方法是指：没有具体实现的方法(pass)
     称之为抽象方法
抽象类的作用
多用于做顶层设计(设计标准)，以便于子类做具体实现
"""
class Animal(object):
    def speak(self):
        pass
class Dog(Animal):
    def speak(self):
        print("汪汪汪")
class Cat(Animal):
    def speak(self):
        print("喵喵喵")
def makeNoise(animal:Animal):
    animal.speak()
if __name__ == '__main__':
    dog=Dog()
    cat=Cat()
    makeNoise(dog)
    makeNoise(cat)