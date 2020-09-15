import json
from django.core import serializers

class Excel_In():
    # Python构造函数只有一个: 参数列表最长的一个覆盖其他的构造函数
    # 构造函数，初始化 -1 is an impossible value thus to assigned here for initialization
    #List of List (2D list )
    def __init__(self, plantATP=[], ATP_NTA_row=[], customerList=[], CW_list=[], excelTable=[], productName='', filename=''): #plantATP->One Dimision; customerList->two dimension
        # private
        self.__plantATP = plantATP;
        self.__productName = productName;
        self.ATP_NTA_row = ATP_NTA_row
        # Customer ObjectList
        self.__customerList = customerList;
        self.__CW_list = CW_list; # List of CW, for all date at uploaded excel.
        self.__excelTable = excelTable;
        self.__filename = filename;

    def get_productName(self):
        return self.__productName

    def get_CW_list(self):
        return self.__CW_list

    def get_plantATP(self):
        return self.__plantATP

    def get_ATP_NTA_row(self):
        return self.ATP_NTA_row

    def get_customerList(self):
        return self.__customerList

    def get_customerJsonList(self):
        result = []
        for customer in self.__customerList:
            result.append(customer.getDict())
        return result

    def get_excelTable(self):
        return self.__excelTable

    def get_filename(self):
        return  self.__filename;

    #这里是建立一个字典，把list作为值存入字典中去。
    # 不知道前端能不能处理 含有Python的List类型作为value 的JSON对象
    def getDict(self):
       return  {
            'productName': self.__productName,
            'plantATP': self.__plantATP,
            'ATP_NTA_row' : self.ATP_NTA_row,
            'customerList': self.__customerList,
            'CW_list': self.__CW_list,
            'excelTable'  : self.__excelTable,
            'filename'  : self.__filename
        }

    '''e.g. customerList ==> {'name': 'A_4006047_WF00', 'CMAD': [0.0, 0.0, 0.0, 0.0, 170000.0, 0.0, 60000.0, 50000.0, 0.0, 0.0, 0.0, 195000.0, 50000.0, 50000.0, 45000.0, 0.0, 0.0, 155000.0, 50000.0, 15000.0, 0.0, 135000.0, 50000.0, 0.0, 0.0, 85000.0, 35000.0, 0.0, 0.0, 0.0, 0.0, 170000.0, 0.0, 0.0, 149000.0, 0.0, 0.0, 0.0, 149000.0, 0.0, 0.0, 0.0, 149000.0, 0.0, 0.0, 0.0, 0.0, 149000.0, 0.0, 0.0, 0.0, 149000.0, 0.0, 0.0, 0.0, 298000.0], 'AATP': [], 'AStock': [], 'scenarioOrder': ''}, {'name': 'B_WF00', 'CMAD': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 66000.0, 68000.0, 68000.0, 0.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0, 75000.0, 74000.0, 0.0, 0.0, 70000.0, 80000.0, 80000.0, 80000.0, 0.0, 80000.0, 150000.0, 80000.0, 80000.0, 80000.0, 60000.0, 130000.0, 40000.0, 30000.0, 30000.0, 70000.0, 70000.0, 104000.0, 100000.0, 70000.0, 60000.0, 80000.0, 80000.0, 76000.0, 76000.0, 76000.0, 76000.0, 76000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'AATP': [], 'AStock': [], 'scenarioOrder': ''}, {'name': 'C_WF00', 'CMAD': [0.0, 0.0, 0.0, 0.0, 1000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'AATP': [], 'AStock': [], 'scenarioOrder': ''}]'''

    #https://www.youtube.com/watch?v=-5umzZ4yJAo
    #customerList is the list of dictionarized Customer-object
    def getJSON(self):
         return json.dumps(self,
            default=lambda obj:{
                'productName' : obj.get_productName(),
                'plantATP'    : obj.get_plantATP(),
                'ATP_NTA_row' : obj.get_ATP_NTA_row(),
                'excelTable'  : obj.get_excelTable(),
                'customerList': obj.get_customerJsonList(), #<--这个地方不是可序列化的类型,
                'CW_list'     : obj.get_CW_list(),
                'filename'    : obj.get_filename()
            })
       # return json.dumps(self,
       #       default=lambda obj:obj.__dict__,
       #       sort_keys=False,
       #       indent=4) ;

