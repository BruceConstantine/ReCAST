import json


class Scenario():
    def __init__(self, cusW, stoW):
        # Scenario's Weight
        self.__cusW = cusW;  # Customer Weight
        self.__stoW = stoW;  # Stock Weight

    def getDict(self):
        return {
            'cusW': self.cusW,
            'stoW': self.stoW
        }

    def getJSON(self):
        return json.dumps(self.getDict())

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