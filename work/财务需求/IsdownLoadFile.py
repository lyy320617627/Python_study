from datetime import datetime


class IsdownLoadFile:
    def get_cuurent_day(self):
        self.__today = datetime.today().day
        print(f"当前日期为当月的第{self.__today}号")

    def isDownStreamLoad(self):
        self.get_cuurent_day()
        if 1 <= self.__today <= 4 or 8 <= self.__today <= 15 or 22 <= self.__today <= 31:
            return True
        return False

    def isUpStreamLoad(self):
        self.get_cuurent_day()
        if 1 <= self.__today <= 4 or 20 <= self.__today <= 31:
            return True
        return False


if __name__ == '__main__':
    isDownLoad = IsdownLoadFile()
    isDownStreamLoadFile = isDownLoad.isDownStreamLoad()
    isUpStreamLoadFile = isDownLoad.isUpStreamLoad()
    print(f"是否进行下游价保返利文件下载: {isDownStreamLoadFile}")
    print(f"是否进行上游价保返利文件下载: {isUpStreamLoadFile}")
