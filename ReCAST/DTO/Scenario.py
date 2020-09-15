import json


class Scenario():
    def __init__(self, number, customerList, cusW, stoW):
        # the order number of a cenario at list
        self.__number = number;
        # customer list is the list of Diction containing the AATP, ASTOCK and CMAD
        self.__customerList =  customerList;
        # 这里要搞清楚前端到底要什么样的数据格式，是list of list? 还是 List of dictionary?
        self.__cusW =  cusW;
        self.__stoW =  stoW;

    customerNameList = []

    def getDict(self):
        return {
            'number': self.__number,
            'customerList': self.__customerList,
            'customerNameList': Scenario.customerNameList,
            'cusW': self.__cusW,
            'stoW': self.__stoW
        }

    def getJSON(self):
        return json.dumps(self.getDict())

    @staticmethod
    def setCustomerNameList(customerNameList):
        Scenario.customerNameList = customerNameList;

    # auto-print when a scenario object being called
    def __str__(self):
        res_string = 'Scenario Object: number='+str(self.__number)+', customerList=' +self.__customerList.__str__() \
                            +', cusW=' + str(self.__cusW) \
                            +', stoW=' + str(self.__stoW)+', customerNameList=' \
                            + Scenario.customerNameList.__str__()+"\n";
        return res_string;

class Result():
    def __init__(self, rid, tid, cusW, stoW, customerName):
        self.__rid = rid;   #rid is sid -> scenario ID3 (int)
        self.__tid = tid;   # Task id
        #Scenario's Weight
        self.__cusW = cusW; # Customer Weight
        self.__stoW = stoW; # Stock Weight

        self.__customerName = customerName; # One line
       # self.__AATP = AATP; # Min. Run Rate List
       # self.__Astock = Astock; # Min. Run Rate List

   # def getName(self):
   #    return self.__name
   # def setName(self, name):
   #     self.__name = name

    def getJSON(self):
        return json.dumps({
        })