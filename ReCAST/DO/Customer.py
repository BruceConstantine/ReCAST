import json


class Customer():
    # Python构造函数只有一个: 参数列表最长的一个覆盖其他的构造函数
    def __init__(self,name='',CMAD=[]): #,TA=[], MR=[]):
        #构造函数，初始化
        self.__name = name;
        self.__CMAD = CMAD
        '''No need TA & MR Currently'''
        #self.__TA = TA; # Target Allocation List
        #self.__MR = MR; # Min. Run Rate List

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def getCMAD(self):
         return self.__CMAD

    def setCMAD(self, CMAD):
         self.__CMAD = CMAD

    def getDict(self):
        return {
            'name': self.__name,
            'CMAD': self.__CMAD,
        }

    def getJSON(self):
        return json.dumps({
            'name': self.__name,
            'CMAD': self.__CMAD,
        })

    # def getJSON_of_TA_MR(self):
    #      return json.dumps({
    #         'name': self.__name,
    #         'CMAD': self.__CMAD,
    #         'TA': self.__TA,
    #         'MR': self.__MR
    #     })
    # def getMR(self):
    #     return self.__CMAD
    #
    # def setTA(self, CMAD):
    #     self.__CMAD = CMAD
    #
    # def getTA(self):
    #     return self.__TA
    # def getMR(self):
    #     return  self.__MR
    # def setTA(self,TA):
    #     self.__TA = TA
    # def setMR(self,MR):
    #     self.__MR = MR
