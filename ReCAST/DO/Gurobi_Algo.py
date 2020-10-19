import numpy as np
import pandas as pd

from ReCAST.views import allocationPlan_to_customerList, toScenarioObj_DictList


def run_gurobi( abs_filename=None, # filename for excel on disk (Not memory-> request.file["XXXX"]
                CW_start=None, CW_end=None,      # int: integer value of CW start and end time
                 CW_start_date=None, CW_end_date=None,  # string type: date value in string
                 packingUnit_in=None,  # int: integer value >= 100
                 MBS_in=[],  #(M ) int list: integer list, from index CW_start to CW_end
                 RBS_in=[],  #(Reserve Buffer stock) int list: integer list, from index CW_start to CW_end
                 plantATP_in=None,  # int list: integer list, from index CW_start to CW_end
                 ComfirmedOrder_in=None,  #the list of dictionary whose key is the name of customer and
                                        # whose value (CMAD) is the integer list from index CW_start to CW_end
                                        # format :
                                        # [
                                        #  {"Customer_Name_1": [1000,20020,300,0 ... ] } # Customer list
                                        #  {"Customer_Name_2": [1000,20020,300,0 ... ] } # Customer list
                                        #  {"Customer_Name_3": [1000,20020,300,0 ... ] } # Customer list
                                        #  ... ...
                                        # ]
                 bin_usefrom_stock_in=[],  # here is the binary two dimension array for allowance of using (only 1 or 0 at here)
                 ATP_NTA_in=None,  # int: integer value of the CW_start
                 scenarioList_in=None, # the list of two-element integer list, format :
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
                 maxDelay_in=None,  # int: integer value
                 date_list_in = [], #date_list_in to instand df[1], assinging date value to columns_ATP
                 enableRub=False,  # boolean list: integer value of the CW_start
                 PGL=[]  # int list: integer list, possible gain or loss from index CW_start to CW_end
                 ):

    # list of all points for connecting to parser

    # 1- The confirmedOrder is pycharm should change from list of dictionaries to
    #    one dictionary with customers name as key and list of their order as value

    # 2- The results calculate for each loops (based on scenarios). [refer to @zhikang comment].
    #    you should read the values in each loop and store them according to you code.
    # This is just a sample creation for model. It load an excel file frol local system.
    df = pd.read_excel(io=abs_filename, header=None,
                       skiprows=2, usecols="I:BE")  # H:BF manualy added
    '''181218_TASUI extract_SP000646194.xls'''


    # extract CW
    CW_list = [i for i in range(CW_start, CW_end)]

    # extract Date
    #date_list = lambda d_from, d_to: [d_from, d_to]

    # extract Date
    #df_main = df.iloc[[1, 11, 14, 21]]
    df_main = df.iloc[[1, 11]]
    df_list = df_main.to_numpy().tolist()
    '''
    # df_list = df_main.to_numpy().tolist() df_list is the list of CMAD
    df_list = df_main.to_numpy().tolist() 
    print("###############################################")
    print("-------- Plant ATP ---------")
    print(df_list[0])
    print("-------- Date ---------")
    print(df_list[1])
    print("-------- CMAD for Customer no.1 --------")
    print(df_list[2])
    print("-------- CMAD for Customer no.2 ---------")
    print(df_list[3])
    print("###############################################")

    len(df_list[1])
    '''

    # fit with Matlab file to compare the results

    #print("----------------------")
    #confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3]}
    len_CW= int(CW_end)-int(CW_start)+1;
    print("!!!!!!!!!!!!!!!!!!!! CW_start  CW_end !!!!!!!!!!!!!!!!!!!");
    print( CW_start, CW_end );
    confirmedOrder = ComfirmedOrder_in
    #confirmedOrder = [];
    for customerDict in confirmedOrder:
        customerDict['CMAD'] = list(map(int, customerDict['CMAD']))
        #customerDict['CMAD'] = list(map(int, customerDict['CMAD']))[CW_start-1:CW_end]
        #AcustomerCMAD = list(map(int, AcustomerCMAD));
        #confirmedOrder.append(AcustomerCMAD);
        #for item in customerDict :
        #     if type(item) == str:
        #         print("item is a 'str'")
        #         print("'"+item+"'")
        #customerDict['CMAD'] = list(map(int, customerDict['CMAD']))
        #print('customerDict["CMAD]"')
        #print(customerDict)
        #print(len(customerDict['CMAD']))
        #print()
    #print("----------------------")
    #plantATP = df_list[0]
    print("plantATP_in")
    print(plantATP_in)
    plantATP = list(map(int,plantATP_in))
    #if plantATP is the whole row, which is not been selected, then use the following line:
    #plantATP = list(map(int,plantATP_in))[CW_start-1:CW_end]
    print("plantATP")
    print(plantATP)
    print(len(plantATP))
    print()

    #plantATP = plantATP_in

    #print("----------------------")
    #MBS = [400000] * len(df_list[0])
    # MBS_in is a big string, rather than a list of string
    MBS = list(map(int,MBS_in.split(',')))
    #print("MBS")
    #print(MBS)
    #print()


    print("----------------------")
    #RBS = [100000] * len(df_list[0])
    RBS = list(map(int,RBS_in.split(',')))
    # print("RBS")
    #print(RBS)
    #print(len(RBS))
    #print()

    #print("----------------------")
    ATP_NTA = int(ATP_NTA_in)
    # print("ATP_NTA")
    #print(ATP_NTA)
    #print()


    #print("----------------------")
    packingUnit = int(packingUnit_in)
    #print("packingUnit")
    #print(packingUnit)
    #print()


    scenarioList = scenarioList_in
    len_scenarioList = len(scenarioList)
    for index in range(len_scenarioList):
        scenarioList[index]  = list(map(float, scenarioList[index] ))
        #print(scenarioList[index])
        #print()
    #print("---scenarioList=---")
    #print(scenarioList)
    #print( len(scenarioList))
    #scenarioList = [[0.9, 0.1], [0.7, 0.3], [0.4, 0.6]]

    #int            str
    maxDelay = int(maxDelay_in)
    #print("----------------------")
    #print("maxDelay")
    #print(maxDelay)

    ######################################
    #confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3] }
    #plantATP = df_list[0]
    # MBS = [400000] * len(df_list[0])
    # RBS = [100000] * len(df_list[0])
    # ATP_NTA = 535500
    # packingUnit = 500
    # scenarioList = [[0.9, 0.1], [0.7, 0.3], [0.4, 0.6]]
    # maxDelay = 10
    ######################################

    # defining list of index
    # From here you should take the code

    time_periods = plantATP
    allocation_time = plantATP

    atp = (np.array(plantATP)) / packingUnit
    buffer_stock_min = np.array(MBS) / packingUnit
    #print(atp)
    #print(buffer_stock_min)
    reserve_Buffer = np.array(RBS) / packingUnit
    intial_Buffer_Value = ATP_NTA / packingUnit

    #print("-----Customer orders-----")
    customers=[]
    for oder_dictItem in confirmedOrder:
        customers.append(oder_dictItem["name"])
    #print("customers:")
    #print(customers)
    #print()

    #extract CMAD
    order=[]
    for oder_dictItem in confirmedOrder:
        order.append(oder_dictItem["CMAD"])
    print("order:(CMAD)")
    print(order)
    print()

    '''
    #order is list of CMAD
    order = []
    for key in confirmedOrder:
        order.append(confirmedOrder[key])
    '''

    orders = np.array(order) / packingUnit
    '''
    # Strategic allocation decision for using from stock for specific customer or not
    bin_usefrom_stock = [1] * len(orders)
    for i in range(len(orders)):
        bin_usefrom_stock[i] = [1] * len(atp)
        #  this is multidimensional list based on number of weeks and number of custmers
    print(bin_usefrom_stock)
    '''

    #TODO: some problem occur on input '1' or '0'
    bin_usefrom_stock = bin_usefrom_stock_in
    #print(bin_usefrom_stock_in)
    # you have it in format of lists with dimension of number of customers * CW

    ###################
    #bin_usefrom_stock = [1] * len(orders)
    #for i in range(len(orders)):
    #    bin_usefrom_stock[i] = [1] * len(atp)
    ###################

    max_delay = maxDelay

    # Defining penalty function of allocation later than requested data
    penalty_coef = [[0] * len(atp) for i in range(len(atp))]

    for time in range(len(atp)):
        idx_max = min(time + max_delay - 1, len(atp))
        idx_min = time
        value_penalty = [0] * len(atp)
        for acceptable_penalty_loop in range(idx_min, idx_max):
            value_penalty[acceptable_penalty_loop] = round((1 - ((abs(time - acceptable_penalty_loop) / max_delay))), 3)
            # defined function here is linear and it could be shifted to exponentioal form to force the model
            # to allocate faster in time horizon

            penalty_coef[time] = value_penalty

    penalty_coef_Stock = [[0] * len(atp) for i in range(len(atp))]

    for time in range(len(atp)):
        idx_max = min(time + 1, len(atp))
        idx_min = time
        value_penalty_Stock = [0] * len(atp)
        for acceptable_penalty_loop in range(idx_min, idx_max):
            value_penalty_Stock[acceptable_penalty_loop] = 1

        penalty_coef_Stock[time] = value_penalty_Stock

    # print(penalty_coef_Stock)

    eps = 1e-4
    # this is the value for relaxing solver about binary constraint
    big_M = 1e+5

    reCAST = Model('20200707_ReCAST_04')

    var_Allocation_ATP = reCAST.addVars(len(orders), len(atp), len(atp), lb=0, vtype=GRB.INTEGER,
                                        name='Var_Allocation_ATP')

    var_Allocation_Stock = reCAST.addVars(len(orders), len(atp), len(atp), lb=0, vtype=GRB.INTEGER,
                                          name='Var_Allocation_Stock')

    var_BufferStock = reCAST.addVars(len(atp), vtype=GRB.INTEGER, name='Var_BufferStock')
    print("@@@@@@var_BufferStock@@@@@@")
    print(len(atp))
    print(var_BufferStock)

    var_ReserveBuffer = reCAST.addVars(len(atp), vtype=GRB.INTEGER, name='Var_ReserverBufferStock')

    var_z = reCAST.addVars(len(atp), vtype=GRB.BINARY, name='useStockOrNot')

    # var_Allocation_ATP = reCAST.addVars(len(orders), len(atp), len(atp),lb = 0,
    #                                vtype = GRB.CONTINUOUS, name = 'Var_Allocation_ATP')

    # var_Allocation_Stock = reCAST.addVars(len(orders), len(atp), len(atp), lb = 0,
    #                                     vtype = GRB.CONTINUOUS, name = 'Var_Allocation_Stock')

    # var_BufferStock = reCAST.addVars(len(atp), vtype = GRB.CONTINUOUS,
    #                                name = 'Var_BufferStock')

    # var_z = reCAST.addVars(len(atp), vtype = GRB.BINARY , name = 'Var_UseStockOrNot')

    #Test here for output orders details
    #print("orders"+str(orders))

    reCAST.addConstrs((var_Allocation_ATP.sum(i, r, '*') + var_Allocation_Stock.sum(i, r, '*') <= orders[i][r]
                       for i in range(len(orders)) for r in range(len(atp))), name='cons_orders');

    # here I should read the value of buffer stock in time 0 from the excel file - Solved
    #reCAST.addConstrs((var_BufferStock[t] == intial_Buffer_Value
    #                   for t in range(1)), name='con_Buffer_Initial');
    #new constraint
    reCAST.addConstr((var_BufferStock[0] == intial_Buffer_Value), name='con_Buffer_Initial');

    reCAST.addConstrs((var_BufferStock[t] - var_BufferStock[t - 1] +
                       var_Allocation_ATP.sum('*', '*', t - 1) +
                       var_Allocation_Stock.sum('*', '*', t - 1) == atp[t - 1]
                       for t in range(1, len(atp))), name='con_Buffer');

    reCAST.addConstrs((var_Allocation_ATP.sum('*', '*', t) + var_ReserveBuffer[t] <= atp[t]
                       for t in range(len(atp))), name='con_Resources');

    reCAST.addConstrs((var_ReserveBuffer[t] <= reserve_Buffer[t] for t in range(len(atp))), name='RBS_Goal');

    reCAST.addConstrs((var_Allocation_Stock.sum('*', '*', t) <= var_BufferStock[t]
                       for t in range(len(atp))), name='con_stock');

    reCAST.addConstrs((var_BufferStock[t] >= buffer_stock_min[t]
                       for t in range(len(atp))), name='con_buffer_stock_min');

    #reCAST.addConstr((var_Allocation_ATP.sum('*', '*', '*') >= sum(atp) - sum(reserve_Buffer))
    #                 , name='con_reserve_buffer')

    ##### This constraint can make the model infeasible when sum(atp) - sum(reserve_Buffer) is bigger than
    ##### all orders which limit the value of allocation from ATP AQ
    #print('The Value for Checking infeasibility = '+str(sum(atp) - sum(reserve_Buffer)))

    # reCAST.addConstrs((var_Allocation_Stock.sum(i,'*',t) - var_Allocation_Stock.sum(i,r,'*') == 0
    #                   for i in range(len(orders)) for t in range(len(atp)) for r in range(len(atp))),
    #                  name = 'con_AsAq');

    ### This constraint solved with penalty in objective function

    z_indx_posi_list = [i for i in range(len(atp)) if atp[i] != 0]

    reCAST.addConstrs((var_z[t] - (var_Allocation_ATP.sum('*', '*', t) / atp[t]) <= eps
                       for t in z_indx_posi_list), name='con_bin_allocation');

    # print(z_indx_posi_list)

    z_indx_atp0 = [i for i in range(len(atp)) if atp[i] == 0]

    reCAST.addConstrs((var_z[t] == 1 for t in z_indx_atp0), name='con_bin_z_eqOne');
    # print(z_indx_atp0)

    reCAST.addConstrs((var_Allocation_Stock[i, r, t] - (bin_usefrom_stock[i][t] * big_M * var_z[t]) <= 0
                       for i in range(len(orders)) for r in range(len(atp)) for t in range(len(atp))),
                      name='con_bin_UseStockorNot');
    # bin_usefrom_stock[i][t] *

    obj_Allocation = quicksum((var_Allocation_ATP[i, r, t] * penalty_coef[r][t]) + (
                (var_Allocation_Stock[i, r, t]) * penalty_coef_Stock[r][t])
                              for t in range(len(atp)) for i in range(len(orders)) for r in range(len(atp)))

    obj_ReserveStock = quicksum(var_ReserveBuffer[t] for t in range(len(atp)))

    # try with multiobjective of Gurobi
    reCAST.Params.MIPGap = 1e-9  # -4 00
    reCAST.Params.IntFeasTol = 1e-9  # -5 -9
    reCAST.Params.FeasibilityTol = 1e-9  # -6 -9
    reCAST.Params.OptimalityTol = 1e-9
    reCAST.Params.TimeLimit = 300

    len_scenarioList = len(scenarioList)

    scenarioList_result = []

    for scenario in range(len_scenarioList):
        weight_Allocation = scenarioList[scenario][0]
        weight_ReserveBuffer = scenarioList[scenario][1]

        reCAST.setObjective(weight_Allocation * obj_Allocation + weight_ReserveBuffer * obj_ReserveStock, GRB.MAXIMIZE)

        reCAST.optimize()

        #Check for infeasibility
        if reCAST.Status == 4:# or 3:
            print('The inputs are WRONG!\nYou should modify inputs and re-run ReCAST')
            #TODO: If this prints, the model is infeasible and we can pup up an alarm page
            return None;

        #     Exteraction of allocated quantities from ATP in format of dataframe
        rows_ATP = customers.copy()

        #TODO: MAYBE EEEOR HERE!
        #columns_ATP = df_list[1].copy() #date
        #@Behrouz, I comment the old one, and put new statement for the date selection
        columns_ATP = date_list_in;

        allocation_ATP_Plan = pd.DataFrame(columns=columns_ATP, index=rows_ATP, data=0.0)

        for i, r, t in var_Allocation_ATP.keys():
            if (abs(var_Allocation_ATP[i, r, t].x > 1e-6)):
                allocation_ATP_Plan.iloc[i, t] += np.round(var_Allocation_ATP[i, r, t].x * packingUnit, 0)

        # what is the means for 'var_Allocation_ATP[i, r, t].x'
        # [i,r,t]
        # i -> cutomer
        # r & t -> different times
        # r: Week customer request for  // request time
        # t: time allo.. // ....

        #print(allocation_ATP_Plan.to_dict())

        #     Exteraction of allocated quantities from Stock in format of dataframe

        # @Zhikang: the printed values in each loop are the solution that you should take for result tabels.

        rows_stock = customers.copy()
        #columns_Stock = df_list[1].copy() # df_list[1] is date_list
        columns_Stock = date_list_in
        allocation_Stock_Plan = pd.DataFrame(columns=columns_Stock, index=rows_stock, data=0.0)

        for i, r, t in var_Allocation_Stock.keys():
            if (abs(var_Allocation_Stock[i, r, t].x > 1e-6)):
                allocation_Stock_Plan.iloc[i, t] += np.round(var_Allocation_Stock[i, r, t].x * packingUnit, 0)

        #print("allocation_Stock_Plan: length:")
        #print(allocation_Stock_Plan.__len__())
        #print("allocation_Stock_Plan: length:")
        #print(allocation_Stock_Plan.to_dict())

        #     Exteraction of buffer stock level
        rows_buffer = ["Buffer Plan"]
        #columns_buffer is date_list
        #columns_buffer = df_list[1].copy() #[date of CW_start to the date of CW_end]
        columns_buffer = date_list_in
        print("columns_buffer="+str(columns_buffer))
        buffer_Plan = pd.DataFrame(columns=columns_buffer, index=rows_buffer, data=0.0)

        for t in var_BufferStock.keys():
            if (abs(var_BufferStock[t].x > 1e-6)):
                buffer_Plan.iloc[0, t] += np.round(var_BufferStock[t].x * packingUnit, 0)

        #print(buffer_Plan.to_dict())

        scenarioList_result.append(allocationPlan_to_customerList(customers, allocation_ATP_Plan.to_dict(), allocation_Stock_Plan.to_dict(), buffer_Plan.to_dict()))

    print("------------------------------------------------")
    print(allocation_ATP_Plan.to_dict())
    print("------------------------------------------------")
    print("------------------------------------------------")
    print(scenarioList_result)
    print("!!!!!!!!!!!END of scenarioList_result!!!!!!!!")
    """Finished scenarioList loop"""
    result = toScenarioObj_DictList(scenarioList_result,scenarioList)
    print( "scenarioList=" + scenarioList.__str__() )
    print()
    for eachScenario in result:
        print( eachScenario )
    return result;

    #     Values of objectives for test

    #     obj_MAX_Allocation_Alone = reCAST.getObjective()

    #     value_MAX_Obj_Allocation_Alone = obj_MAX_Allocation_Alone.getValue()

    #     print(value_MAX_Obj_Allocation_Alone)
    #     for v in reCAST.getVars():
    #         if v.X != 0:
    #             print("%s %f" %(v.Varname, v.X))

    # reCAST.write('ReCAST12.lp')
    scenarioList_result
    rows_ATP = customers.copy()
    #columns_ATP = df_list[1].copy() #df_list[1].copy() is the copy of selected date list
    columns_ATP = date_list_in
    allocation_ATP_Plan = pd.DataFrame(columns=columns_ATP, index=rows_ATP, data=0.0)
    print("--------customers----------")
    print(customers)
    print("---------columns_ATP-------------")
    print(columns_ATP)
    print("---------BeforeAssignment: allocation_ATP_Plan-------------")
    print(allocation_ATP_Plan)

    for i, r, t in var_Allocation_ATP.keys():
        if (abs(var_Allocation_ATP[i, r, t].x > 1e-6)):
            allocation_ATP_Plan.iloc[i, t] += np.round(var_Allocation_ATP[i, r, t].x * packingUnit, 0)

    print("---------After : allocation_ATP_Plan-------------")
    print(allocation_ATP_Plan)
    print("---------END of After : allocation_ATP_Plan-------------")

    #allocation_ATP_Plan

    rows_stock = customers.copy()
    #columns_Stock = df_list[1].copy() # df_list[1].copy() is the selected date list
    columns_Stock = date_list_in
    allocation_Stock_Plan = pd.DataFrame(columns=columns_Stock, index=rows_stock, data=0.0)

    for i, r, t in var_Allocation_Stock.keys():
        if (abs(var_Allocation_Stock[i, r, t].x > 1e-6)):
            allocation_Stock_Plan.iloc[i, t] += np.round(var_Allocation_Stock[i, r, t].x * packingUnit, 0)

    # allocation_Stock_Plan

    # buffer_Plan = []
    # for t in var_BufferStock.keys():
    # #     if (var_BufferStock[t].x > 1e-6):
    #      buffer_Plan.append(np.round(var_BufferStock[t].x * packingUnit,0))
    # print(buffer_Plan)

    rows_buffer = ["Buffer Plan"]
    #columns_buffer = df_list[1].copy() # df_list[1].copy() is date_list
    columns_buffer = date_list_in
    buffer_Plan = pd.DataFrame(columns=columns_buffer, index=rows_buffer, data=0.0)

    for t in var_BufferStock.keys():
        if (abs(var_BufferStock[t].x > 1e-6)):
            buffer_Plan.iloc[0, t] += np.round(var_BufferStock[t].x * packingUnit, 0)

    # buffer_Plan
    buffer_Plan_list = buffer_Plan.values.tolist()
    #print(buffer_Plan_list)
    # reCAST.write('ReCAST1.mps')

    #AATP_dict = allocation_ATP_Plan.to_dict()
    AStock_dict = allocation_Stock_Plan.to_dict()
    print( allocation_Stock_Plan )

    return  scenarioList_result;