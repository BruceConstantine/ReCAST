import json

from ReCAST import DAO


class Task():
    def __init__(self,taskName=None,taskDescription=None, currentPage=None,
                    username=None, pid='', CW_start=None, CW_end=None, packingUnit=None,
                    MBS = [], RBS = [], plantATP=None, ATP_NTA=None, scenarioList=None,
                    maxDelay=None,  enableRub=False,  TA_rid=None, cid=None, date=''):
        #Get Max ID + 1
        self.tid = DAO.getMaxID("Task") + 1
        # Task descriptions
        self.taskName = taskName
        self.taskDescription = taskDescription
        # No ".html" added into DB, we need to take it from DB and add the extension in code.
        self.currentPage = currentPage
        # RLC's Username
        self.username = username

        #Excel Data
        self.pid = pid
        self.CW_start = CW_start
        self.CW_end = CW_end
        self.enableRub = enableRub
        self.RBS = RBS
        self.MBS = MBS
        # This is a big string for stroing all vlaues of plant ATP
        self.plantATP = self.__getList(plantATP)
        self.ATP_NTA = self.__getList(ATP_NTA)
        self.maxDelay = maxDelay
        self.packingUnit = packingUnit

        # The rid of result scenario. aka. Target allocation which selected by RLC's final decision
        self.TA_rid = TA_rid
        self.scenarioList = scenarioList
        # Reference to Config table 使用ForeignKey扩展Task表
        self.cid =cid  # ForeignKey(Config,on_delete=models.CASCADE, null=True)
        self.date=date

    def getCWlength(self):
        l = self.CW_end - self.CW_start
        return l if l > 0 else self.CW_start - self.CW_end

    @staticmethod
    def copy(taskmodel):
        self = Task();
        #Get Max ID + 1
        self.tid = taskmodel.tid
        # Task descriptions
        self.taskName = taskmodel.taskName
        self.taskDescription = taskmodel.taskDescription
        # No ".html" added into DB, we need to take it from DB and add the extension in code.
        self.date = taskmodel.date
        self.currentPage = taskmodel.currentPage
        # RLC's Username
        self.username = taskmodel.username

        #Excel Data
        self.pid = taskmodel.pid
        self.CW_start = taskmodel.CW_start
        self.CW_end = taskmodel.CW_end
        self.enableRub = taskmodel.enableRub
        self.RBS = taskmodel.RBS
        self.MBS = taskmodel.MBS
        # This is a big string for stroing all vlaues of plant ATP
        self.plantATP = taskmodel.plantATP
        self.ATP_NTA = taskmodel.ATP_NTA
        self.maxDelay = taskmodel.maxDelay
        self.packingUnit = taskmodel.packingUnit

        # The rid of result scenario. aka. Target allocation which selected by RLC's final decision
        self.TA_rid = taskmodel.TA_rid
        self.scenarioList = taskmodel.scenarioList
        # Reference to Config table 使用ForeignKey扩展Task表
        self.cid =taskmodel.cid  # ForeignKey(Config,on_delete=models.CASCADE, null=True)
        return self;

    #input must be dictionary type
    def assignDict(self,dict):
        self.tid = dict.tid
        self.taskName = dict.taskName
        self.taskDescription = dict.taskDescription
        self.currentPage = dict.currentPage
        self.username = dict.username
        # Excel Data
        self.pid = dict.pid
        self.CW_start = dict.CW_start
        self.CW_end = dict.CW_end
        self.MBS  = dict.MBS
        self.RBS  = dict.RBS
        self.enableRub = dict.enableRub
        self.plantATP = dict.plantATP
        self.ATP_NTA = dict.ATP_NTA
        self.maxDelay = dict.maxDelay
        self.packingUnit = dict.packingUnit
        self.TA_rid = dict.TA_rid
        self.cid = dict.cid
        return self.getDict()

    def getDict(self):
        return {
            'tid': self.tid,
            'taskName': self.taskName,
            'taskDescription': self.taskDescription,
            'username': self.username,
            'pid': self.pid,
            'CW_length': self.getCWlength(),
            'CW_start': self.CW_start,
            'CW_end': self.CW_end,
            'maxDelay': self.maxDelay,
            'packingUnit': self.packingUnit,
            'enableRub': self.enableRub,
            'TA_rid': self.TA_rid,
            'cid': self.cid,
            'plantATP': self.plantATP,
            'ATP_NTA': self.ATP_NTA,
            'RBS': self.RBS,
            'MBS': self.MBS,
        }

    def getJSON(self):
        return json.dumps(self.getDict())

    def __getList(self,stringfiedList):
        if stringfiedList == None:
            return []
        else:
            return stringfiedList #.split(',')

# class Task():
#     def __init__(self,taskName='',taskDescription='', currentPage='',
#                     username='', pid='', CW_start=-1, CW_end=-1,
#                     enableRub=False, plantATP='', ATP_NTA="",
#                     maxDelay=-1, packingUnit=100, TA_rid=-1, cid=-1):
#         #Auto generate ID
#         #self.__tid = DAO.getMaxID("Task")
#         # Task descriptions
#         self.__taskName = taskName
#         self.__taskDescription = taskDescription
#         # No ".html" added into DB, we need to take it from DB and add the extension in code.
#         self.__currentPage = currentPage
#         # RLC's Username
#         self.__username = username
#
#         #Excel Data
#         self.__pid = pid
#         self.__CW_start = CW_start
#         self.__CW_end = CW_end
#         enableRub = enableRub
#         # This is a big string for stroing all vlaues of plant ATP
#         self.__plantATP = plantATP
#         self.__ATP_NTA = ATP_NTA
#         self.__maxDelay = maxDelay
#         self.__packingUnit = packingUnit
#
#         # The rid of result scenario. aka. Target allocation which selected by RLC's final decision
#         self.__TA_rid = TA_rid
#         # Reference to Config table 使用ForeignKey扩展Task表
#         self.__cid =cid  # ForeignKey(Config,on_delete=models.CASCADE, null=True)
#
#     def getCWlength(self):
#         l = self.__CW_end - self.__CW_start
#         return l if l > 0 else self.__CW_start - self.__CW_end
#
#     def getTaskName(self):
#         return self.__taskName
#     def setTaskName(self, taskname):
#         self.__taskName = taskname
#     def getTaskDescription(self):
#         return self.__taskDescription
#     def setTaskDescription(self, description):
#         self.__taskDescription = description
#     def getTaskUsername(self):
#         return self.__username
#     def setUsername(self, username):
#         self.__username = username
#     def getPid(self):
#         return self.__pid
#     def setPid(self, pid):
#         self.__pid = pid
#
#     def getJSON(self):
#         return json.dumps({
#             'name': self.__name,
#             'CMAD': self.__CMAD,
#         })
#     def getJSON_of_TA_MR(self):
#         return json.dumps({
#             'name': self.__name,
#             'TA': self.__TA,
#             'MR': self.__MR
#         })