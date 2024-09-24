import numpy as np
"""
通过代码调用numpy中的loadtxt方法，来读取文件数据
# 方法名：np.loadtxt(frame,dtype=np.float,delimiter=None,skiprows=0,usecols=None,unpack=False)
# frname:表示读取的文件名（包含文件路径），文件、字符串或产生器，可是.gz或者是bz2压缩文件
# dtype:数据类型，可选，csv的字符串以什么数据类型读入数组中，默认是np.float
# delimiter:分隔字符串，默认是任何空格，改为逗号
# skiprows:跳过前x的列，索引，元组类型
# usecols：读取指定的列，索引，元组类型
# unpack:如果True，读取属性将分别写入不同数组变量，False  读入数据只写入一个数组变量，默认False
         如果为True，将按照对角线进行转置，即将x周和y轴按照对角线旋转一下
# 转置的其余三种方法：即将x轴和y轴交换
# （1）:t1.transpose()
#  (2):t1.T
#  (3):t1.swapxes(1,0)  注意：默认情况下，轴的情况为（0,1）
"""
t1=np.loadtxt("1.csv",delimiter=",",dtype="float",skiprows=0,usecols=None,unpack=False)
print(t1)

