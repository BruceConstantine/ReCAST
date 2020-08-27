class DataTransferObj_GurobiInterface():
    def __init__(self, CW_start=None, CW_end=None,      # int: integer value of CW start and end time
                 CW_start_date=None, CW_end_date=None,  # string type: date value in string
                 packingUnit=None,  # int: integer value >= 100
                 MBS=[],  #(M ) int list: integer list, from index CW_start to CW_end
                 RBS=[],  #(Reserve Buffer stock) int list: integer list, from index CW_start to CW_end
                 plantATP=None,  # int list: integer list, from index CW_start to CW_end
                 ComfirmedOrder=None,  #the list of dictionary whose key is the name of customer and
                                        # whose value (CMAD) is the integer list from index CW_start to CW_end
                                        # format :
                                        # [
                                        #  {"Customer_Name_1": [1000,20020,300,0 ... ] } # Customer list
                                        #  {"Customer_Name_2": [1000,20020,300,0 ... ] } # Customer list
                                        #  {"Customer_Name_3": [1000,20020,300,0 ... ] } # Customer list
                                        #  ... ...
                                        # ]
                 bin_use_stock=[],  # here is the binary two dimension array for allowance of using (only 1 or 0 at here)
                 ATP_NTA=None,  # int: integer value of the CW_start
                 scenarioList=None, # the list of two-element integer list, format :
									#[
									#  [Customer_Weight_s1, Stock_Weight_s1], # for scenario 1
									#  [Customer_Weight_s2, Stock_Weight_s2], # for scenario 2
									#  [Customer_Weight_s3, Stock_Weight_s3], # for scenario 3
									#  ...
									# ]
                                    # e.g.            Customer Weight   Stock Weight
                                    #       scenario1  0.2               0.8
                                    #       scenario2  0.6               0.4
                                    #       scenario3  0.1               0.9
                                    #
                                    #Then, the array list should be: [ [0.2, 0.8], [0.6, 0.4] , [0.1, 0.9] ]
                 maxDelay=None,  # int: integer value
                 enableRub=False,  # boolean list: integer value of the CW_start
                 PGL=[]  # int list: integer list, possible gain or loss from index CW_start to CW_end
                 ):
        # class attributes:

        # ###### Start of INPUT parameters ######
        self.CW_start = CW_start
        self.CW_end = CW_end
        self.RBS = RBS

        self.MBS = MBS
        self.ComfirmedOrder = ComfirmedOrder
        self.bin_use_stock  = bin_use_stock
        self.scenarioList = scenarioList
        self.plantATP = plantATP


        self.ATP_NTA = ATP_NTA
        self.maxDelay = maxDelay
        self.packingUnit = packingUnit
        # ###### End of INPUT parameters ######

        # ###### output parameters and data structure format #######
        self.ComfirmedOrder_result = None
        '''# the list of dictionary whose key is the name of customer and 
        # whose value is the integer pair list from index CW_start to CW_end
        # format :
          [	#the first parameter at list pair is 'AATP' and the second one is 'A-Stock', they shall be used at the page 'modify' for adjusting dual visualization.
            #list at here is {'customer name': [ [AATP_CW1,A-Stock_CW1]，[AATP_CW2,A-Stock_CW2] ... ...]}
            #   also: AATP + A-Stock = Sum, and Sum value shall be placed at the page 'result'
            {"Customer_Name_1": [[100,200],[2600,200],[0,300],[0,0] ... ] } # ComfirmedOrder result list
            {"Customer_Name_2": [[100,200],[2600,200],[0,300],[0,0] ... ] } # ComfirmedOrder result list
            {"Customer_Name_3": [[100,200],[2600,200],[0,300],[0,0] ... ] } # ComfirmedOrder result list
            ... ... 
          ]'''

    # ###### End   of OUTPIT parameters ######
    # -------------------------------------------------

    # ######@Zhikang, TODO: Second method (Another way) for assigning result to the data transfering object ######


    # --------End of Second method-----------
    @staticmethod
    def run_with_Task(self, task):
        aTask = DataTransferObj_GurobiInterface(task.CW_start, task.CW_end, task.packingUnit,
                                              task.MBS,task.RBS,task.plantATP,
                                              task.ComfirmedOrder,task.ATP_NTA ,
                                              task.scenarioList ,task.maxDelay,
                                              task.enableRub,task.PGL)
        aTask.run();
        return aTask.getResult();

    # for output
    def getResult(self):
        self.run()
        return self.ComfirmedOrder_result

        # here define the python code for mathmetical model

    # --------------------------------------------------

    # @Behrouz, TODO Refactor this method by ---------------------------
    def run(self): #you can variable function parameters here
        # ... ...
        # the last line should update 'self.ComfirmedOrder_result' attribute
        # And its content should can be directly passed to JS (JSON Obj)
        #@TODO: paste the mathmetical model python code at here.

        #if it result format can be constructed as a list, that could be great.
        self.ComfirmedOrder_result = []


    # --------------------------------------------------
    # class setter
    def setCW_start(self,CW_start):
        self.CW_start = CW_start

    def setCW_end(self,CW_end):
        self.CW_end = CW_end

    def setRBS(self,RBS):
        self.RBS = RBS

    def setMBS(self,MBS):
        self.MBS = MBS

    def setScenarioList(self,scenarioList):
        self.scenarioList = scenarioList

    def setPlantATP(self,plantATP):
        self.plantATP = plantATP

    def setATP_NTA(self,ATP_NTA):
        self.ATP_NTA = ATP_NTA

    def setMaxDelay(self,maxDelay):
        self.maxDelay = maxDelay

    def setPackingUnit(self,packingUnit):
        self.packingUnit = packingUnit

    def setComfirmedOrder(self,ComfirmedOrder):
        self.ComfirmedOrder = ComfirmedOrder

    def setComfirmedOrder_result(self,ComfirmedOrder_result):
        self.ComfirmedOrder_result = ComfirmedOrder_result

    # class getter
    def getCW_start(self):
        return self.CW_start

    def getCW_end(self):
        return self.CW_en

    def getRBS(self):
        return self.RBS

    def getMBS(self):
        return self.MBS

    def getScenarioList(self):
        return self.scenarioList

    def getPlantATP(self):
        return self.plantATP

    def getATP_NTA(self):
        return self.ATP_NTA

    def getMaxDelay(self):
        return self.maxDelay

    def getPackingUnit(self):
        return self.packingUnit

    def getComfirmedOrder(self):
        return self.ComfirmedOrder