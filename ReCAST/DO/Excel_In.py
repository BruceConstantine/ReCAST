import json
from django.core import serializers

class Excel_In():
    # Python构造函数只有一个: 参数列表最长的一个覆盖其他的构造函数
    # 构造函数，初始化 -1 is an impossible value thus to assigned here for initialization
    #List of List (2D list )
    def __init__(self, plantATP=[], ATP_NTA=-1, customerList=[], excelTable=[], productName=''): #plantATP->One Dimision; customerList->two dimension
        # private
        self.__plantATP = plantATP;
        self.__productName = productName;
        self.ATP_NTA = ATP_NTA
        self.__customerList = customerList; # List of Customers
        self.__excelTable = excelTable;

    def get_productName(self):
        return self.__productName

    def get_plantATP(self):
        return self.__plantATP

    def get_ATP_NTA(self):
        return self.ATP_NTA

    def get_customerList(self):
        return self.__customerList

    def get_customerJsonList(self):
        result = []
        for customer in self.__customerList:
            result.append(customer.getDict())
        return result

    def get_excelTable(self):
        return self.__excelTable


    #这里是建立一个字典，把list作为值存入字典中去。
    # 不知道前端能不能处理 含有Python的List类型作为value 的JSON对象
    def getDict(self):
       return  {
            'productName': self.__productName,
            'plantATP': self.__plantATP,
            'ATP_NTA' : self.ATP_NTA,
            'customerList': self.__customerList,
            'excelTable'  : self.__excelTable
        }
    #https://www.youtube.com/watch?v=-5umzZ4yJAo

    def getJSON(self):
         return json.dumps(self,
            default=lambda obj:{
                'productName' : obj.get_productName(),
                'plantATP'    : obj.get_plantATP(),
                'ATP_NTA'     : obj.get_ATP_NTA(),
                'excelTable'  : obj.get_excelTable(),
                'customerList': obj.get_customerJsonList() #<--这个地方不是可序列化的类型
            })
       # return json.dumps(self,
       #       default=lambda obj:obj.__dict__,
       #       sort_keys=False,
       #       indent=4) ;

