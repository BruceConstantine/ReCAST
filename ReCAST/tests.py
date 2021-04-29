from django.test import TestCase

from ReCAST.DO.Excel_In import Excel_In
import hashlib
from gurobipy import *
import pandas as pd
import numpy as np

def __hash(password):
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

print(__hash("123"))

# e = Excel_In([1,222],[[1,2],[111,2]]);
# print(e.get_plantATP());
# print(e.getJSON());
# print(e.getDict());
#print(e.toJSON());


# from oct2py import Oct2Py
# oc = Oct2Py()
#
#
# script = "function y = myScript(x)\n" \
#          "    y = x-5" \
#          "end"
#
# with open("myScript.m","w+") as f:
#     f.write(script)
#
# oc.myScript(7)


# list of all points for connecting to parser

# 1- The confirmedOrder is pycharm should change from list of dictionaries to
#    one dictionary with customers name as key and list of their order as value

# 2- The results calculate for each loops (based on scenarios). [refer to @zhikang comment].
#    you should read the values in each loop and store them according to you code.
# This is just a sample creation for model. It load an excel file frol local system.
##df = pd.read_excel(io='../181218_TASUI extract_SP000646194.xls', header=None,
#                 skiprows=2, usecols="I:BE")  # H:BF manualy added

df_main = df.iloc[[1, 11, 14, 21]]
# extract CW
# CW_list = [i for i in range(CW_start, CW_end)]

# extract Date
# date_list = lambda d_from, d_to: [d_from, d_to]

# extract CMAD


# df_list = df_main.to_numpy().tolist() df_list is the list of CMAD
df_list = df_main.to_numpy().tolist()

# print(df_list)
len(df_list[1])
# fit with Matlab file to compare the results

# confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3]}

plantATP = df_list[0]
# plantATP = plantATP_in
MBS = [400000] * len(df_list[0])
# MBS = MBS_in
RBS = [100000] * len(df_list[0])
# RBS = RBS_in
# scenarioList = [[0.9, 0.1], [0.7, 0.3], [0.4, 0.6]]

######################################
confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3]}
plantATP = df_list[0]
MBS = [400000] * len(df_list[0])
RBS = [100000] * len(df_list[0])
ATP_NTA = 535500
packingUnit = 500
scenarioList = [[0.9, 0.1], [0.7, 0.3], [0.4, 0.6]]
maxDelay = 10
######################################

# defining list of index
# From here you should take the code

time_periods = plantATP
allocation_time = plantATP
customers = list(confirmedOrder.keys())

atp = (np.array(plantATP)) / packingUnit
buffer_stock_min = np.array(MBS) / packingUnit
reserve_Buffer = np.array(RBS) / packingUnit
intial_Buffer_Value = ATP_NTA / packingUnit

order = []
for key in confirmedOrder:
    order.append(confirmedOrder[key])

orders = np.array(order) / packingUnit
'''
# Strategic allocation decision for using from stock for specific customer or not
bin_usefrom_stock = [1] * len(orders)
for i in range(len(orders)):
    bin_usefrom_stock[i] = [1] * len(atp)
    #  this is multidimensional list based on number of weeks and number of custmers
print(bin_usefrom_stock)
'''
# you have it in format of lists with dimension of number of customers * CW

###################
bin_usefrom_stock = [1] * len(orders)
for i in range(len(orders)):
    bin_usefrom_stock[i] = [1] * len(atp)
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

var_z = reCAST.addVars(len(atp), vtype=GRB.BINARY, name='useStockOrNot')

# var_Allocation_ATP = reCAST.addVars(len(orders), len(atp), len(atp),lb = 0,
#                                vtype = GRB.CONTINUOUS, name = 'Var_Allocation_ATP')

# var_Allocation_Stock = reCAST.addVars(len(orders), len(atp), len(atp), lb = 0,
#                                     vtype = GRB.CONTINUOUS, name = 'Var_Allocation_Stock')

# var_BufferStock = reCAST.addVars(len(atp), vtype = GRB.CONTINUOUS,
#                                name = 'Var_BufferStock')

# var_z = reCAST.addVars(len(atp), vtype = GRB.BINARY , name = 'Var_UseStockOrNot')

reCAST.addConstrs((var_Allocation_ATP.sum(i, r, '*') + var_Allocation_Stock.sum(i, r, '*') <= orders[i][r]
                   for i in range(len(orders)) for r in range(len(atp))), name='cons_orders');

# here I should read the value of buffer stock in time 0 from the excel file - Solved
reCAST.addConstrs((var_BufferStock[t] == intial_Buffer_Value
                   for t in range(1)), name='con_Buffer_Initial');

reCAST.addConstrs((var_BufferStock[t] - var_BufferStock[t - 1] +
                   var_Allocation_ATP.sum('*', '*', t - 1) +
                   var_Allocation_Stock.sum('*', '*', t - 1) == atp[t - 1]
                   for t in range(1, len(atp))), name='con_Buffer');

reCAST.addConstrs((var_Allocation_ATP.sum('*', '*', t) <= atp[t]
                   for t in range(len(atp))), name='con_Resources');

reCAST.addConstrs((var_Allocation_Stock.sum('*', '*', t) <= var_BufferStock[t]
                   for t in range(len(atp))), name='con_stock');

reCAST.addConstrs((var_BufferStock[t] >= buffer_stock_min[t]
                   for t in range(len(atp))), name='con_buffer_stock_min');

reCAST.addConstr((var_Allocation_ATP.sum('*', '*', '*') >= sum(atp) - sum(reserve_Buffer))
                 , name='con_reserve_buffer')

##### This constraint can make the model infeasible when sum(atp) - sum(reserve_Buffer) is bigger than
##### all orders which limit the value of allocation from ATP AQ
print(sum(atp) - sum(reserve_Buffer))

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

obj_ReserveStock = quicksum(- var_Allocation_ATP.sum('*', '*', t)
                            for t in range(len(atp)))

# try with multiobjective of Gurobi
reCAST.Params.MIPGap = 1e-9  # -4 00
reCAST.Params.IntFeasTol = 1e-9  # -5 -9
reCAST.Params.FeasibilityTol = 1e-9  # -6 -9
reCAST.Params.OptimalityTol = 1e-9

for scenario in range(len(scenarioList)):
    weight_Allocation = scenarioList[scenario][0]
    weight_ReserveBuffer = scenarioList[scenario][1]

    reCAST.setObjective(weight_Allocation * obj_Allocation + weight_ReserveBuffer * obj_ReserveStock, GRB.MAXIMIZE)

    reCAST.optimize()

    #     Exteraction of allocated quantities from ATP in format of dataframe

    rows_ATP = customers.copy()
    columns_ATP = df_list[1].copy()
    allocation_ATP_Plan = pd.DataFrame(columns=columns_ATP, index=rows_ATP, data=0.0)

    for i, r, t in var_Allocation_ATP.keys():
        if (abs(var_Allocation_ATP[i, r, t].x > 1e-6)):
            allocation_ATP_Plan.iloc[i, t] += np.round(var_Allocation_ATP[i, r, t].x * packingUnit, 0)

    print(allocation_ATP_Plan)

    #     Exteraction of allocated quantities from Stock in format of dataframe

    # @Zhikang: the printed values in each loop are the solution that you should take for result tabels.

    rows_stock = customers.copy()
    columns_Stock = df_list[1].copy()
    allocation_Stock_Plan = pd.DataFrame(columns=columns_Stock, index=rows_stock, data=0.0)

    for i, r, t in var_Allocation_Stock.keys():
        if (abs(var_Allocation_Stock[i, r, t].x > 1e-6)):
            allocation_Stock_Plan.iloc[i, t] += np.round(var_Allocation_Stock[i, r, t].x * packingUnit, 0)

    print(allocation_Stock_Plan)

    #     Exteraction of buffer stock level
    rows_buffer = ["Buffer Plan"]
    columns_buffer = df_list[1].copy()
    buffer_Plan = pd.DataFrame(columns=columns_buffer, index=rows_buffer, data=0.0)

    for t in var_BufferStock.keys():
        if (abs(var_BufferStock[t].x > 1e-6)):
            buffer_Plan.iloc[0, t] += np.round(var_BufferStock[t].x * packingUnit, 0)

    print(buffer_Plan)

#     Values of objectives for test

#     obj_MAX_Allocation_Alone = reCAST.getObjective()

#     value_MAX_Obj_Allocation_Alone = obj_MAX_Allocation_Alone.getValue()

#     print(value_MAX_Obj_Allocation_Alone)
#     for v in reCAST.getVars():
#         if v.X != 0:
#             print("%s %f" %(v.Varname, v.X))

# reCAST.write('ReCAST12.lp')

rows_ATP = customers.copy()
columns_ATP = df_list[1].copy()
allocation_ATP_Plan = pd.DataFrame(columns=columns_ATP, index=rows_ATP, data=0.0)

for i, r, t in var_Allocation_ATP.keys():
    if (abs(var_Allocation_ATP[i, r, t].x > 1e-6)):
        allocation_ATP_Plan.iloc[i, t] += np.round(var_Allocation_ATP[i, r, t].x * packingUnit, 0)

# allocation_ATP_Plan

rows_stock = customers.copy()
columns_Stock = df_list[1].copy()
allocation_Stock_Plan = pd.DataFrame(columns=columns_Stock, index=rows_stock, data=0.0)

for i, r, t in var_Allocation_Stock.keys():
    if (abs(var_Allocation_Stock[i, r, t].x > 1e-6)):
        allocation_Stock_Plan.iloc[i, t] += np.round(var_Allocation_Stock[i, r, t].x * packingUnit, 0)

# allocation_Stock_Plan
print("#####################")
#print(allocation_Stock_Plan.to_dict())
#print("-+++++++++++++++++++++++++-")
AATP_dict = allocation_ATP_Plan.to_dict()
AStock_dict = allocation_Stock_Plan.to_dict()
def printAStock_dict(AStock_dict):
    for CW_date_key in AStock_dict:
        CW_result = AStock_dict[CW_date_key]
        print(str(CW_date_key) + ":" + str(CW_result))
        for customer in CW_result:
            print(str(customer) + ":" + str(CW_result[customer]))
        print()

#printAStock_dict(AATP_dict)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!111")
def getAllocationPlanList(plan_list):
    value_list = plan_list.values.tolist()
    plan_dict = plan_list.to_dict()
    date_list = plan_list.keys().array.to_numpy().tolist()
    customer_list = []
    for CW_date_key in plan_dict:
        CW_result = AStock_dict[CW_date_key]
        for customer in CW_result:
            print(str(customer) + ":" + str(CW_result[customer])) # for test
            customer_list.append(customer)
        break
    return [customer_list , value_list]


aatp   = getAllocationPlanList(allocation_ATP_Plan)
print(aatp)
print(allocation_ATP_Plan)
'''
customerNamelist   = aatp[0]
aatp   = aatp[1]
astock = getAllocationPlanList(allocation_Stock_Plan)[1]
length = aatp[0].__len__()
customerList = []

for i in range(customerNamelist.__len__()):
    one_customer = {}
    one_customer["name"] = customerNamelist[i]
    value = []
    for j in range(length):
        value.append(aatp[i][j]+astock[i][j])
    one_customer["CMAD"] = value
    one_customer["AATP"] = aatp[i]
    one_customer["AStock"] = astock[i]
    customerList.append(one_customer)
aatp=None
astock=None
print("---------------")
print(customerList)
print("---------------")

'''

'''
print("-+++++++++++++++++++++++++-")
print(allocation_Stock_Plan.keys().array.to_numpy().tolist())
print("-+++++++++++++++++++++++++-")
print(allocation_Stock_Plan.values.tolist())
print("-+++++++++++++++++++++++++-")
print(type(allocation_Stock_Plan.values.tolist()))
'''
print("#####################")


# buffer_Plan = []
# for t in var_BufferStock.keys():
# #     if (var_BufferStock[t].x > 1e-6):
#      buffer_Plan.append(np.round(var_BufferStock[t].x * packingUnit,0))
# print(buffer_Plan)

'''
rows_buffer = ["Buffer Plan"]
columns_buffer = df_list[1].copy()
buffer_Plan = pd.DataFrame(columns=columns_buffer, index=rows_buffer, data=0.0)

for t in var_BufferStock.keys():
    if (abs(var_BufferStock[t].x > 1e-6)):
        buffer_Plan.iloc[0, t] += np.round(var_BufferStock[t].x * packingUnit, 0)

# buffer_Plan
print("----------------------------buffer_Plan.to_numpy----------------------------")
print(buffer_Plan.keys().array.to_numpy)
print("------------to_numpy()--------------")
lista = buffer_Plan.keys().array.to_numpy().tolist()
#print(lista.append(1))
print(lista)
print(type(lista)) # <class 'list'>
print(type([1,2,1,3,4,2,5])) # <class 'list'>
print(type(lista) == type([1,2,1,3,4,2,5])) # True
print(type(lista) is type([1,2,1,3,4,2,5])) # True

print("--------------------------")
#error : AttributeError: 'PandasArray' object has no attribute 'append'
#print(buffer_Plan.keys().array.append(1))
#print(buffer_Plan.keys().array.insert(2,'123sdadsa'))
#error end
print("--------------------------")
print(dir(buffer_Plan.keys().array))
print("#####################")
print(buffer_Plan.to_dict())
print("#####################")
print(buffer_Plan.__dict__)
print("#####################")
print(buffer_Plan.values.tolist())
print()
# reCAST.write('ReCAST1.mps')
'''