import json
import os
import time
import random
import hashlib

from django.contrib.auth import authenticate
from django.http import FileResponse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
#from ReCAST.DTO import DataTransferObj_GurobiInterface
from ReCAST.DTO.Task import Task
from ReCAST.models import Task as Taskmodel
from ReCAST.models import User as Usermodel
from ReCAST.util.ExcelFileOperator import ExcelFileOpearator
from ReCAST.util.Parser import Parser

from django.core.mail import send_mail
from gurobipy import *
import pandas as pd
import numpy as np


def back_previews_page_html_str():
    return '<html><head><script>history.go(-1)</script></head><body></body></html>'

def getRouter(url_fullpath):
    parts = url_fullpath.split('/')
    i_upbound = len(parts) - 1
    i = 0
    for part in parts:
        if part.endswith('8000') and i < i_upbound:
            return parts[i + 1]
        else:
            i += 1
    return None;

def __hash(password):
    h = hashlib.md5()
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def getTaskAtSession(request):
    task = request.session.get("task")
    if task == None:
        task = {}
    return task

def index(request):
    print(request.headers)
    if request.method == 'POST':
        form = request.POST
        # if form.is_valid():
        uname = form.get('username')
        # * SSL at HTTPS protocol shall encoding its content for confidentiality
        #   But another method is passing the Hash value instead of the plaintext password -> but hacker may can know the encrypting algorithm.
        password = form.get('password')
        hasspw = __hash(password)
        # Authentication
        user = Usermodel.objects.filter(username=uname)
        if user: # if exists
            #check if password hash code are matching
            login_success = hasspw == user[0].hassPW
            if login_success:
                #Write user account info into session
                request.session['username'] = uname;
                return render(request, 'index.html')
            else: #nothing changed and return to login page.
                return render(request, 'login.html', {'msg': "Password not correct" })
        else: # if user not exist
            # Refactor: return render(request, 'login.html', {"msg": user is not registered})
            return render(request, 'login.html',{'msg':"Username not exist"})
    # Generally 'login function' can not be implemented by GET. 
    #elif request.method == 'GET' or others
    return render(request, 'login.html')

def login(request):
    return HttpResponse('login.html')


def logout(request):
    # return redirect('http://www.baidu.com')
    # print all attributes items at request.session object
    # print('\n'.join(['%s:%s' % item for item in request.session.__dict__.items()]))

    # clean up all parameters in session.
    request.session.clear();
    # print (request.session.has_key('username')) to test if all seted session attributes are cleaned up.
    return render(request, 'login.html')

# Create your views here.
def display(request):
    now_time = time.strftime('%Y-%m-%d %X', time.localtime())
    return render(request, 'modify.html', {'now_time': now_time})


def createTask(request):
    #request.headers['type'] is string type.
    if request.headers.__contains__('Referer'):
        url_origin = request.headers['Referer']
        if getRouter(url_origin) == 'index':
            return render(request, 'createTask.html')
        elif request.method == "POST":
            return render(request, 'createTask.html') # ,{"data":[]} initialization
        #create task
        elif request.method == "GET":
            return HttpResponse(back_previews_page_html_str)
        #Check username
        #Check pid
        # whatever, must to let the system stay at one state no matter from back to forward or forward to back.
        #return render(request, 'createTask.html')
        else:
            return HttpResponse(back_previews_page_html_str)

# return JSON object contains plantATP, ATPvsNET, Confirmed Orders and all exceldata
def upload(request):
    if request.method == "POST":
        file = request.FILES['excel_in']
        print(request.POST)
        #if file:  # len(request.FILES.keys()) != 0
            # Load Excel data to session
        excel_data_json = ExcelFileOpearator.handle_upload_file(file)  # str(request.FILES['file']) --> None
        jsonObj=json.loads(excel_data_json)
        # pid is productname
        request.session["pid"]      = jsonObj["productName"]
        request.session["plantATP"] = jsonObj["plantATP"]
        request.session["ATP_NTA"]  = jsonObj["ATP_NTA"]
        request.session["excelTable"]   = jsonObj["excelTable"]
        request.session["customerList"] = jsonObj["customerList"]
        # a = request.session.get('username')
        #return JsonResponse(excel_data_json)
        print(jsonObj)
        return HttpResponse(excel_data_json)

        # file = request.FILES['excel_in']
        # if file:  # len(request.FILES.keys()) != 0
        #     # Load Excel data to session
        #     excel_data_json = ExcelFileOpearator.handle_upload_file(file)  # str(request.FILES['file']) --> None
        #     # a = request.session.get('username')
        #     return render(request, 'createTask.html', {"data":excel_data_json})
        #     # return HttpResponse(excel_data_json)
    else:
        return render(request, 'createTask.html')
    # return render('course/upload.html')

def downloadManual(request):
    # Absolute path of User manual here
    file = open('/static/manual/ReCAST_Use_Manual.pdf', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="ReCAST Use Manual.pdf"'
    return response


def config(request):
    task = getTaskAtSession(request)
    if request.method == "POST":
        #print(request.POST)
        taskName = request.POST.get('taskName')
        packageUnit = request.POST.get('packagingUnit')
        taskDescription = request.POST.get('taskDescription')
        CW_start = int(request.POST.get('CW_start'))
        CW_end   = int(request.POST.get('CW_end'))
        SW_input_list = request.POST.getlist('SW_input')
        CW_input_list = request.POST.getlist('CW_input')
        scenarioList=[]; arr_index = 0;
        for stockWeight in SW_input_list:
            scenarioList.append([stockWeight,CW_input_list[arr_index]])
            arr_index+=1
        try:
            pid = request.session["pid"]
            plantATP = request.session["plantATP"]
            ATP_NTA = request.session["ATP_NTA"]
            customerList = request.session["customerList"]
            username = request.session["username"]
            currentPage = 'createTask'
            #get Scenario list
            '''print(pid)
            print(plantATP)
            print(ATP_NTA)
            print(excelTable)
            print(customerList)
            print(username)
            print(currentPage) '''
        except :
            print("No file detect!")
            return config(request)
        '''    
        def reorder(CW_start,CW_end,rowName):
            
            if rowName == 'plantATP':
                
            elif rowName == 'ATP_NTA':
        '''
        task = Task(taskName, taskDescription, currentPage, username, pid, CW_start, CW_end, packageUnit,
                    plantATP=plantATP, ATP_NTA=ATP_NTA, scenarioList=scenarioList)
        # MBS =[], RBS =[]
       # maxDelay=None, enableRub=False, TA_rid=None, cid=None, date='')
        '''
        createdObj = Taskmodel.objects.create(taskName=taskName, taskDescription=taskDescription,
                                              currentPage='createTask',
                                              username=request.session["username"],
                                              pid=pid,CW_start=CW_start, CW_end=CW_end, 
                                              packageUnit=packageUnit,plantATP=plantATP,
                                              enableRub=ATP_NTA, scenarioList=scenarioList)
                            
                            
                            )
        '''
        #Cache task dto into session
        # request.session["task"] = {"task" : task} #--> task is not JSON serializable
        request.session["task"] = task.getDict()
        #print( task.getDict() )
        taskDict = getTaskAtSession(request)#request.session["task"] ;
        # print(json.loads(request.session.get("task"))["tid"])
        # task = task.getJSON()

        print('CW_start: '+str(taskDict['CW_start']))
        print('CW_end: '+str(taskDict['CW_end']))
        print("plantATP: "+str(taskDict["plantATP"]))
        print("ATP_NTA: "+str(taskDict["ATP_NTA"])) # [0],
        print("customerList: "+str(request.session["customerList"])) # [0],
    return render(request, 'config.html',
                    {'CW_start':taskDict['CW_start'],
                    'CW_end':taskDict['CW_end'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerList':json.dumps(request.session["customerList"])}) #JSONfy/serialization
   # if request.method == "GET":
   #     return render(request, '403.html')

def run(request):
    if request.method == "POST":
        task = getTaskAtSession(request)
        task["maxDelay"] = request.POST.get('maxdelay')
        task["MBS"] =request.POST.get('MBS')
        task["RBS"] =request.POST.get('RBS')
        request.session["task"]=task;
        print(task)
        print('request.session["username"]=')
        print(request.session["username"])
        #resultlist = DataTransferObj_GurobiInterface.run_with_Task(task)
        #dl=json.dumps(resultlist)
    datalist = [[93, 93, 0, 100.01], [20, 23, 26, 29]]
    dl=json.dumps(datalist)
    taskDict = getTaskAtSession(request)
    customerList = run_gurobi()
    request.session["customerList"] = customerList
    return render(request, 'result.html',{'CW_start':taskDict['CW_start'],
                    'CW_end':taskDict['CW_end'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerList':json.dumps(request.session["customerList"]),
                    #'customerList':json.dumps(customerList),
                    'datalist': dl})

#return customerList
def run_gurobi( CW_start=None, CW_end=None,      # int: integer value of CW start and end time
                 CW_start_date=None, CW_end_date=None,  # string type: date value in string
                 packingUnit_in=None,  # int: integer value >= 100
                 MBS_in=[],  #(M ) int list: integer list, from index CW_start to CW_end
                 RBS_in=[],  #(Reserve Buffer stock) int list: integer list, from index CW_start to CW_end
                 plantATP_in=None,  # int list: integer list, from index CW_start to CW_end
                 ComfirmedOrder=None,  #the list of dictionary whose key is the name of customer and
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
                 enableRub=False,  # boolean list: integer value of the CW_start
                 PGL=[]  # int list: integer list, possible gain or loss from index CW_start to CW_end
                 ):

    # list of all points for connecting to parser

    # 1- The confirmedOrder is pycharm should change from list of dictionaries to
    #    one dictionary with customers name as key and list of their order as value

    # 2- The results calculate for each loops (based on scenarios). [refer to @zhikang comment].
    #    you should read the values in each loop and store them according to you code.
    # This is just a sample creation for model. It load an excel file frol local system.
    df = pd.read_excel(io='181218_TASUI extract_SP000646194.xls', header=None,
                       skiprows=2, usecols="I:BE")  # H:BF manualy added

    df_main = df.iloc[[1, 11, 14, 21]]
    # extract CW
    #CW_list = [i for i in range(CW_start, CW_end)]

    # extract Date
    #date_list = lambda d_from, d_to: [d_from, d_to]

    # extract CMAD


    # df_list = df_main.to_numpy().tolist() df_list is the list of CMAD
    df_list = df_main.to_numpy().tolist()

    #print(df_list)
    len(df_list[1])
    # fit with Matlab file to compare the results

    #confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3]}
    confirmedOrder = ComfirmedOrder

    plantATP = df_list[0]
    #plantATP = plantATP_in
    MBS = [400000] * len(df_list[0])
    #MBS = MBS_in
    RBS = [100000] * len(df_list[0])
    #RBS = RBS_in
    ATP_NTA = ATP_NTA_in
    packingUnit = packingUnit_in
    scenarioList = scenarioList_in
    #scenarioList = [[0.9, 0.1], [0.7, 0.3], [0.4, 0.6]]
    maxDelay = maxDelay_in

    ######################################
    confirmedOrder = {"customer1": df_list[2], "customer2": df_list[3] }
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
    bin_usefrom_stock = bin_usefrom_stock_in
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

    #allocation_ATP_Plan

    rows_stock = customers.copy()
    columns_Stock = df_list[1].copy()
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
    columns_buffer = df_list[1].copy()
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

    def getAllocationPlanList(plan_list):
        value_list = plan_list.values.tolist()
        plan_dict = plan_list.to_dict()
        #date_list = plan_list.keys().array.to_numpy().tolist()
        customer_list = []
        for CW_date_key in plan_dict:
            CW_result = AStock_dict[CW_date_key]
            for customer in CW_result:
                # print(str(customer) + ":" + str(CW_result[customer])) # for test
                customer_list.append(customer)
            break
        return [customer_list, value_list]

    aatp = getAllocationPlanList(allocation_ATP_Plan)
    customerNamelist = aatp[0]
    aatp = aatp[1]
    astock = getAllocationPlanList(allocation_Stock_Plan)[1]
    length = aatp[0].__len__()
    customerList = []

    for i in range(customerNamelist.__len__()):
        one_customer = {}
        one_customer["name"] = customerNamelist[i]
        value = []
        for j in range(length):
            value.append(aatp[i][j] + astock[i][j])
        one_customer["CMAD"] = value
        one_customer["AATP"] = aatp[i]
        one_customer["AStock"] = astock[i]
        customerList.append(one_customer)
    aatp = None
    astock = None
    print("---------------")
    print(customerList)
    print("---------------")
    return customerList;

def adv(request):
    print(request.headers)
    #Host
    url_origin = request.headers['Host']
    #Referer
    #differ(Referer,Host)
    #url_origin = request.headers['Referer']
    if getRouter(url_origin) != "config":
        return render(request, 'config.html')
    return render(request, 'advOpt.html')


def modify(request):
    taskDict = getTaskAtSession(request)
    return render(request, 'modify.html', {'CW_start':taskDict['CW_start'],
                    'CW_end':taskDict['CW_end'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerList':json.dumps(request.session["customerList"]) })


def details(request):
    cid = request.POST.get('cid')
    if None == cid:
        pid = ''
    else:
        cid = cid.strip()
    # Query
    targetTasks = Taskmodel.objects.filter(cid=cid)
    #as cid is primary key, thus can sure that:
    # one and only one queried object must be returned.
    task = targetTasks[0]
    # process data to render at the frontend
    task = task.__dict__
    if task['TA_rid'] == None:
        task["TA_rid"] = 'Ongoing: No senario exported'
    else:
        task["TA_rid"] = 'Finished: Senario No.' + str(task["TA_rid"]) + ' has exported'
    print(task)
    return render(request, 'details.html', {'task': task})

def export(request):
    basedir = os.path.dirname(__file__)
    filename = 'Allocation_Template.xlsx'
    path = basedir ;
    path += "/static/excel/";
    #path += "/static/excel/";
    targetFilePath = Parser.parse2_export_file(path, filename)

    # Test
    print(targetFilePath)

    file = open(targetFilePath, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="Allocation_Template.xls"'
    return response

def viewHistory(request):
    tasklist_all_list = []
    tasklist_all = Taskmodel.objects.all()
    # print(tasklist_all.__dict__) 不适用->因为.__dict__不是返回数据
    for eachtask in tasklist_all:
        #task = Task.copy(eachtask)
        #print(task.getDict())
        tasklist_all_list.append(eachtask.__dict__)
        print(eachtask.__dict__)
    return render(request, 'histroy.html',{'tasklist':tasklist_all_list })

# model to dict by reflection
# def props_with_(obj):
#     pr = {}
#     for name in dir(obj):
#         value = getattr(obj, name)
#         if not name.startswith('__') and not callable(value):
#             pr[name] = value
#     return pr


def search(request):
    pid = request.POST.get('pid')
    if None == pid:
        pid = ''
    else:
        pid = pid.strip()
    #Query
    targetTasks = Taskmodel.objects.filter(pid=pid)
    tasklist_all_list = []
    # print(tasklist_all.__dict__) 不适用->因为.__dict__不是返回数据
    for eachtask in targetTasks:
        # process data to render at the frontend
        eachtask_dict = eachtask.__dict__
        if eachtask_dict['TA_rid'] == None:
            eachtask_dict["TA_rid"] = 'Ongoing: No senario exported'
        else:
            eachtask_dict["TA_rid"] = 'Finished: <b>Senario No.'+str(eachtask_dict["TA_rid"])+'</b> has exported'
        tasklist_all_list.append(eachtask_dict)
        print(eachtask_dict)
    return render(request, 'search.html', {'tasklist': tasklist_all_list, 'pid': pid})


def save(request):
    return None


def discard(request):
    return None


def quit(request):
    return None


def default(request):
    return render(request, 'login.html')
    # return render(request, 'child.html')


def advOpt(request):
    return render(request, 'advOpt.html')


def register(request):
    return render(request, 'register.html')

def generateOTC():
    OTC=''
    for i in range(4):
        OTC+= str(random.randint(0,9));
    print(OTC)
    return OTC

def sendMail(request):
    to_email = request.POST.get('to_email')
    otc = generateOTC();
    try:
        a=1
        # send_mail('One-Time Verification Code', #subject
        #       '\nYour One Time Verification Code for Register on ReCAST is: '
        #       +otc+'\n ',   # content
        #       'ZhikangTian@126.com',    # from
        #       [to_email],               # to
        #       fail_silently=False)
    finally:
        request.session["otc"] = otc;
        return JsonResponse( {
            'success': True
            # 'oct': otc
        } )

def regist(request):
    if request.method == "POST":
        otc_session = request.session.get("otc") #
        username = request.POST.get("username") #
        password = request.POST.get("password") #
        empnum = request.POST.get("empnum") #
        email = request.POST.get("email") #
        otc = request.POST.get("otc") #
        hasspw=__hash(password)
        if otc != otc_session:
            return render(request, 'registerResult.html',{
                                'header': 'Register Successful!',
                                'content': 'Click the below button for login',
                                })
        else :
            createdObj = Usermodel.objects.create(username=username, hassPW=hasspw,
                                        employeeID=empnum,
                                        email=email,
                                        userType=1)
            return render(request, 'registerResult.html', {
                'header': 'Register Successful!',
                'content': 'Click the below button for login',
            })

def checkUsername(request):
    if request.method == "POST":
        username = request.POST.get("username")
        user =  Usermodel.objects.filter(username=username)
        if user.count() == 0:
            return JsonResponse({"valid": True})
        else:
            return JsonResponse({"valid": False})

def restore(request):
    return None

def reset(request):
    return render(request, 'reset.html')


def doreset(request):
    username = request.POST.get("username")
    user = Usermodel.objects.get(username=username)
    user.hassPW = __hash(request.POST.get("password"))
    try:
        user.save()
    except:
        return render(request, 'registerResult.html', {
            'header': 'Reset Failure!',
            'content': 'Please try later or send email to technique support stuff',
        })
    return render(request, 'registerResult.html', {
        'header': 'Reset Successful!',
        'content': 'Click the below button for login',
    })

def getActiveCode(request):
    return None


def update(request):
    return None


def delete(request):
    return None

