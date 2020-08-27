class ComfirmedOrder():
    #customerName:String,  CW_start: int, CW_end: int, valueList: int list
    def __init__(self, customerName, CW_start, CW_end, valueList):
        self.customerName = customerName;
        self.CW_start = CW_start
        self.CW_end = CW_end
        self.valueList = valueList
        temp = []
        time_length = CW_end-CW_start + 1;
        for i in range(time_length):
            temp.append(1)
        self.allowList = temp

    def setAllowAsNo(self, CW):
        self.valueList[CW-self.CW_start] = 0  # 0 is Not Allow

    # Dictionary Format: {"Customer_Name_1": [1000, 20020, 300, 0...]}
    def getDict(self):
        return {
            'customerName': self.customerName,
            'allowList': self.allowList,
            'valueList': self.valueList
        }

