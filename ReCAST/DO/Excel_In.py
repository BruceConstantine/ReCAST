import json

class Excel_In():
    # Python构造函数只有一个: 参数列表最长的一个覆盖其他的构造函数
    # 构造函数，初始化 -1 is an impossible value thus to assigned here for initialization
    def __init__(self, plantATP=[], ATP_NTA=-1, customerList=[]): #plantATP->One Dimision; customerList->two dimension
        # private
        self.__plantATP = plantATP;
        self.ATP_NTA = ATP_NTA
        self.__customerList = customerList; # List of Customers

    def get_plantATP(self):
        return self.__plantATP

    def get_plantCustomerList(self):
        return self.__customerList

    #这里是建立一个字典，把list作为值存入字典中去。
    # 不知道前端能不能处理 含有Python的List类型作为value 的JSON对象
    def getDict(self):
       return  {
            'plantATP': self.__plantATP,
            'customerList': self.__customerList
        }
    #https://www.youtube.com/watch?v=-5umzZ4yJAo
    def getJSON(self):
        #  return json.dumps({
        #     'plantATP': self.__plantATP,
        #     'customerList': self.__customerList #<--这个地方不是可序列化的类型
        # })
       return json.dumps(self, default=lambda obj:obj.__dict__, sort_keys=True, indent=4) ;

