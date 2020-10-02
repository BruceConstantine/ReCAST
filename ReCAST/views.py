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
from ReCAST.DTO.Scenario import Scenario
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

def back_previews_page_html_str_with_alert(alert_str):
    return '<html><head><script>alert("'+alert_str+'");history.go(-1);</script></head><body></body></html>'


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
    print("in function getTaskAtSession(request): task = ")
    print(task)
    if task == None:
        task = {}
    return task

def index(request):
    #print(request.headers)
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
    # However, when user logined, it is possible let user access our platform buy GET method.
    if request.method == 'GET':
        if request.session.has_key('username') and request.session['username'] != None:
            return render(request, 'index.html')
        else:
            return render(request, 'login.html', {'msg': "Login Fristly."})

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
    # This means the request must from a page rather than user'input or GET method HTTP request.
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
        #print(request.POST)
        if file is None:
            return HttpResponse("No File are uploaded!")
        #if file:  # len(request.FILES.keys()) != 0
            # Load Excel data to session
        else:
            excel_data_json = ExcelFileOpearator.handle_upload_file(file)  # str(request.FILES['file']) --> None
            jsonObj=json.loads(excel_data_json)
            # pid is productname
            request.session["pid"]      = jsonObj["productName"]
            request.session["plantATP"] = jsonObj["plantATP"]
            request.session["ATP_NTA_row"]  = jsonObj["ATP_NTA_row"]
            request.session["excelTable"]   = jsonObj["excelTable"]
            #customerList is a list of Customer object
            request.session["customerList"] = jsonObj["customerList"]
            request.session["filename_upload"] = jsonObj["filename"]
            request.session["CW_list"] = jsonObj["CW_list"]
            request.session["date_list"] = jsonObj["date_list"]
            # a = request.session.get('username')
            #return JsonResponse(excel_data_json)
            #print(jsonObj)
            print( request.session["customerList"] )
            print( "--------------------------" )
            print( request.session["customerList"][0]['CMAD'] )
            print( "--------####################################------------" )
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
    #task = getTaskAtSession(request)
    #TODO: task here should not be a session, which should be a task--- that need to be updated at upload function
    task = request.session;
    if request.method == "POST":
        #print(request.POST)
        taskName = request.POST.get('taskName')
        packingUnit = request.POST.get('packingUnit')
        taskDescription = request.POST.get('taskDescription')
        CW_start = int(request.POST.get('CW_start'))
        CW_end   = int(request.POST.get('CW_end'))
        SW_input_list = request.POST.getlist('SW_input')
        CW_input_list = request.POST.getlist('CW_input')
        scenarioList=[]; arr_index = 0;

        #TODO: bug here, we can't use absoluate value directly to get the len,as its length is not centainable
        #request.session['CW_len']  = abs(CW_end-CW_start)
        cw_list_origin = request.session['CW_list']
        request.session['CW_list'] = generateCWList(cw_list_origin, CW_start, CW_end);
        request.session['CW_len'] = get_slelectedCW_len(request.session['CW_list'])

        request.session['CW_start']  = CW_start
        request.session['CW_end']  = CW_end

        # NOTE: update date_list
        request.session["date_list"] = getRealValuelistByCW(CW_start, CW_end, cw_list_origin,  request.session["date_list"])
        print("request.session['date_list']"+str(request.session["date_list"]))

        #update PlantATP once CW start\end are given
        request.session["plantATP"] = getRealValuelistByCW(CW_start,CW_end,cw_list_origin, request.session['plantATP'] )
        print('request.session["plantATP"] = '+str(request.session["plantATP"] ))

        #record the original CMAD for each customer
        origin_CMAD_order = []
        CMAD_order = []
        customer_unparsed_dictlist = request.session["customerList"]
        for customerDict in customer_unparsed_dictlist:
            selectedCMADList = getRealValuelistByCW(cw_start=CW_start, cw_end=CW_end,
                                                             cw_list_origin=cw_list_origin,
                                                             valuelist=customerDict["CMAD"]);
            #TODO: bug here
            origin_CMAD_order.append(customerDict["CMAD"]);
            customerDict["CMAD"] = selectedCMADList;
            CMAD_order.append(selectedCMADList);
        request.session["origin_CMAD_order"] = origin_CMAD_order
        request.session["CMAD_order"] = CMAD_order
        print(' request.session["origin_CMAD_order"]='+str(request.session["origin_CMAD_order"]))
        print(request.session["customerList"])

        for stockWeight in SW_input_list:
            scenarioList.append([stockWeight,CW_input_list[arr_index]])
            arr_index+=1

        #try:
        pid = request.session["pid"]
        plantATP = request.session["plantATP"]
        def get_index(cw_list, CW_value ):
            print('CW_value='+str(CW_value))
            print(cw_list)
            i=0;
            for cw in cw_list:
                print('cw='+str(cw)+'.')
                if CW_value == cw:
                    return i;
                i+=1;
            return -1;
        #get the real ATP_NTA value at the line, the index of that should based on the first element.
        print('CW_LIST'+str(request.session["CW_list"]))
        i = get_index_atSelectedCWList(request.session["CW_list"], CW_start)
        print('request.session["ATP_NTA_row"]')
        print(request.session["ATP_NTA_row"])
        print(i)
        ATP_NTA = getRealValuelistByCW(cw_start=CW_start, cw_end=CW_end,cw_list_origin=cw_list_origin, valuelist=request.session["ATP_NTA_row"])
        #ATP_NTA = getRealValuelistBySelectedCW(cw_start=CW_start, cw_end=CW_end,cw_list=cw_list_origin, valuelist=request.session["ATP_NTA_row"])
        print(i)
        print(ATP_NTA)
        ATP_NTA = ATP_NTA[0]

        print("-------------")
        print("in view.config: ATP_NTA = "+str(ATP_NTA))
        print("-------------")

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


        #except :
        #    print("No file detect!")
        #    return config(request)
        '''    
        def reorder(CW_start,CW_end,rowName):
            
            if rowName == 'plantATP':
                
            elif rowName == 'ATP_NTA':
        '''
        task = Task(taskName, taskDescription, currentPage, username, pid, CW_start, CW_end, packingUnit,
                    plantATP=plantATP, ATP_NTA=ATP_NTA, scenarioList=scenarioList)
        # MBS =[], RBS =[]
       # maxDelay=None, enableRub=False, TA_rid=None, cid=None, date='')
        '''
        createdObj = Taskmodel.objects.create(taskName=taskName, taskDescription=taskDescription,
                                              currentPage='createTask',
                                              username=request.session["username"],
                                              pid=pid,CW_start=CW_start, CW_end=CW_end, 
                                              packingUnit=packingUnit,plantATP=plantATP,
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
                    {'CW_list':request.session['CW_list'],
                    'plantATP' :json.dumps(taskDict["plantATP"]),
                    'ATP_NTA'  :json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerList':json.dumps(request.session["customerList"])}) #JSONfy/serialization
   # if request.method == "GET":
   #     return render(request, '403.html')

def run(request):
    if request.method == "POST":
        task = getTaskAtSession(request)
        task["maxDelay"] = request.POST.get('maxdelay')
        # what type of task["MBS"] is ? a big string.
        task["MBS"] =request.POST.get('MBS')
        task["bin_use_from_stock"] =  json.loads(request.POST.get('bin_use_from_stock'))
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
    #customerList = run_gurobi(abs_filename=request.session["filename_upload"],
    scenarioList_objList = run_gurobi(abs_filename=request.session["filename_upload"],
                                  CW_start=taskDict['CW_start'],
                                  CW_end=taskDict['CW_end'],
                                  CW_start_date=None,CW_end_date=None,
                                  packingUnit_in=taskDict["packingUnit"],
                                  MBS_in=taskDict["MBS"],RBS_in=taskDict["RBS"],
                                  plantATP_in=taskDict["plantATP"],
                                  ComfirmedOrder_in=request.session["customerList"],
                                  #ComfirmedOrder_in=request.session["origin_CMAD_order"],
                                  bin_usefrom_stock_in=taskDict["bin_use_from_stock"],
                                  ATP_NTA_in=int(taskDict["ATP_NTA"]),
                                  scenarioList_in=taskDict["scenarioList"],
                                  maxDelay_in=taskDict["maxDelay"]
                              )
    if scenarioList_objList == None:
        return HttpResponse(back_previews_page_html_str_with_alert("your input is not correct! Please re-configratue your input parameters!"));
    request.session["scenarioList_objList"] = scenarioList_objList
    '''
    print("___________request.session['customerList'] ___________")
    print( request.session["customerList"] )
    print("_________type_____________")
    print( type( request.session["customerList"] ) )
    print('__________json.dumps(request.session["customerList"])___________')
    print(json.dumps(request.session["customerList"]))
    print("_________type_____________")
    print( type( json.dumps(request.session["customerList"]) ) )
    '''
    return render(request, 'result.html',{
                    'CW_list':request.session['CW_list'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #a row rather than ATP_NTA vlaue,
                    'origin_CMAD_order': request.session["origin_CMAD_order"],
                    'scenarioList_objList': scenarioList_objList,
                    # 'customerNameList':json.dumps(Scenario.customerNameList),
                    'customerNameList':Scenario.customerNameList,
                    'customerList':json.dumps(request.session["customerList"]),
                    'customerList_forTemplate':request.session["customerList"],
                    #'customerList':json.dumps(customerList),
                    'datalist': dl})

#return customerList
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
    print('The Value for Checking infeasibility = '+str(sum(atp) - sum(reserve_Buffer)))

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
    reCAST.Params.TimeLimit = 20

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
        columns_ATP = df_list[1].copy() #date
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
        columns_Stock = df_list[1].copy()
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
        #columns_buffer is date, which also need to cooresoponding to the expected CW length.
        columns_buffer = df_list[1].copy()#[CW_start-1:CW_end]
        buffer_Plan = pd.DataFrame(columns=columns_buffer, index=rows_buffer, data=0.0)

        for t in var_BufferStock.keys():
            if (abs(var_BufferStock[t].x > 1e-6)):
                buffer_Plan.iloc[0, t] += np.round(var_BufferStock[t].x * packingUnit, 0)

        #print(buffer_Plan.to_dict())

        scenarioList_result.append(allocationPlan_to_customerList(customers, allocation_ATP_Plan.to_dict(), allocation_Stock_Plan.to_dict(), buffer_Plan.to_dict()))

    print("------------------------------------------------")
    print("------------------------------------------------")
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
    columns_ATP = df_list[1].copy()
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
    print( allocation_Stock_Plan )

    return  scenarioList_result;

def toScenarioObj_DictList(scenariolist, scenarioWeight_list):
    objList = toScenarioObj_List(scenariolist, scenarioWeight_list)
    result = [];
    for scenarioObj in objList :
        result.append(scenarioObj.getDict())
    return result;

def toScenarioObj_List(scenariolist, scenarioWeight_list):
    index = 0;
    scenario_list = [];
    customerNameList = [];
    for customer_dict_list in scenariolist:
        if Scenario.customerNameList == []:
            for eachCustomerName in customer_dict_list.keys():
                customerNameList.append(eachCustomerName);

        customer_AATP_ASTOCK_CMAD_list = []; # list of dictionary
        for eachCustomer_AATP_ASTOCK_CMAD in customer_dict_list.values():
            customer_AATP_ASTOCK_CMAD_list.append(eachCustomer_AATP_ASTOCK_CMAD);

        scenario = Scenario(number=(index+1), customerList=customer_AATP_ASTOCK_CMAD_list,
                            cusW = scenarioWeight_list[index][1],
                            stoW=  scenarioWeight_list[index][0]);
        Scenario.setCustomerNameList(customerNameList);
        scenario_list.append(scenario);
        index += 1 ;
    return scenario_list;

def allocationPlan_to_customerList(customers, allocation_ATP_Plan, allocation_Stock_Plan, buffer_Plan):
    customerList_dict = {}
    for customer in customers:
        aCustomer_dict = {}
        #aCustomer_dict["name"] = customer
        aCustomer_dict["AATP"] = []
        aCustomer_dict["AStock"] = []
        #aCustomer_dict["BufferPlan"] = []
        aCustomer_dict["CMAD"]   =  []
        customerList_dict[customer]= aCustomer_dict

    allocation_ATP_Plan_Values = allocation_ATP_Plan.values()
    for allocation_ATP_plan in allocation_ATP_Plan_Values:  #for each CW, it contains all customer's allocation_ATP plan
        for customer in customers:
            customerList_dict[customer]["AATP"].append( allocation_ATP_plan[customer] )

    allocation_Stock_Plan_Values = allocation_Stock_Plan.values()
    for allocation_ATP_plan in allocation_Stock_Plan_Values:#for each CW, it contains all customer's allocation_ATP plan
        for customer in customers:
            customerList_dict[customer]["AStock"].append( allocation_ATP_plan[customer] )

    CW_length = len(allocation_ATP_Plan)
    for customer in customers:
        CMAD_list = []
        allocation_Stock_Plan_list = customerList_dict[customer]["AStock"]
        allocation_ATP_plan_list   = customerList_dict[customer]["AATP"]
        for i in range(CW_length):
            CMAD_list.append( allocation_ATP_plan_list[i]+allocation_Stock_Plan_list[i])
        customerList_dict[customer]["CMAD"] = CMAD_list.copy()

    buffer_Plan_Values = buffer_Plan.values()
    return customerList_dict;

'''        
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
        # for each CW: CMAD_Result = AAT + AStock.
        for j in range(length):
            value.append(aatp[i][j] + astock[i][j])
        one_customer["CMAD"] = value

        one_customer["AATP"] = aatp[i]
        one_customer["AStock"] = astock[i]
        one_customer["scenarioOrder"] = i+1
        customerList.append(one_customer)
    aatp = None
    astock = None
    #print("---------------")
    #print(customerList)
    #print("---------------")
    return customerList;
'''

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
    taskDict = getTaskAtSession(request);
    scenarioList_objList = request.session["scenarioList_objList"];
    scenario_no =int( request.GET.get('s',1).strip());
    scenario_index = scenario_no - 1;
    #the selected scenario is actually the list of dictionary for each customer for one scenario case
    selected_scenario = scenarioList_objList[scenario_index];
    selected_customerList = selected_scenario['customerList'];
    print(selected_scenario)
    return render(request, 'modify.html', {'CW_start':taskDict['CW_start'],
                    'CW_end':taskDict['CW_end'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerNameList' : Scenario.customerNameList,
                    'customerList':json.dumps(selected_customerList) })


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
    customer_list = request.session['scenarioList_objList'][0]['customerList'];
    basedir = os.path.dirname(__file__)
    filename = 'Allocation_Template.xlsx'
    path = basedir ;
    path += "/static/excel/";
    #path += "/static/excel/";

    print('request.session["date_list"]'+str(request.session["date_list"]))

    targetFilePath = Parser.parse2_export_file(path=path, filename=filename,
                                               customer_list = customer_list,
                                               customername_list = Scenario.customerNameList,
                                               len_cw = request.session['CW_len'],
                                               cw_start = request.session['CW_start'],
                                               product_SP = request.session['pid'],
                                               date_list = request.session["date_list"])

    # Test
    print(targetFilePath);

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
    if request.method == "GET":
        request.GET.get("s")
        taskDict = getTaskAtSession(request)
        # customerList = run_gurobi(abs_filename=request.session["filename_upload"],
        scenarioList_objList = run_gurobi(abs_filename=request.session["filename_upload"],
                                          CW_start=taskDict['CW_start'], CW_end=taskDict['CW_end'], CW_start_date=None,
                                          CW_end_date=None,
                                          packingUnit_in=taskDict["packingUnit"],
                                          MBS_in=taskDict["MBS"], RBS_in=taskDict["RBS"],
                                          plantATP_in=taskDict["plantATP"],
                                          ComfirmedOrder_in=request.session["customerList"],
                                          bin_usefrom_stock_in=taskDict["bin_use_from_stock"],
                                          ATP_NTA_in=int(taskDict["ATP_NTA"]),
                                          scenarioList_in=taskDict["scenarioList"],
                                          maxDelay_in=taskDict["maxDelay"]
                                          )
        request.session["scenarioList_objList"] = scenarioList_objList
        '''
        print("___________request.session['customerList'] ___________")
        print( request.session["customerList"] )
        print("_________type_____________")
        print( type( request.session["customerList"] ) )
        print('__________json.dumps(request.session["customerList"])___________')
        print(json.dumps(request.session["customerList"]))
        print("_________type_____________")
        print( type( json.dumps(request.session["customerList"]) ) )
        '''
        return render(request, 'result.html', {'CW_start': taskDict['CW_start'],
                                               'CW_end': taskDict['CW_end'],
                                               'plantATP': json.dumps(taskDict["plantATP"]),
                                               'ATP_NTA': json.dumps(taskDict["ATP_NTA"]),
                                               # a row rather than ATP_NTA vlaue,
                                               'scenarioList_objList': scenarioList_objList,
                                               # 'customerNameList':json.dumps(Scenario.customerNameList),
                                               'customerNameList': Scenario.customerNameList,
                                               'customerList': json.dumps(request.session["customerList"]),
                                               'customerList_forTemplate': request.session["customerList"] })

def delete(request):
    return None

#must every one element at the list is unique.
# if not found the element at the, then return None as error.
def get_index_atSelectedCWList( cw_list , cw_value ):
    index = 0;
    for item in cw_list:
        if cw_value == item:
            return index;
        index += 1;
    return None;

# if return None, it means user's inpout CW is not at the list.
# else return the selected segment of user's input.
def generateCWList(cw_list_origin, cw_start, cw_end):
    result = [];
    index = 0;
    start_index = None;
    end_index   = None;
    max_index = len(cw_list_origin) - 1;
    for i in cw_list_origin:
        if start_index == None and  i == cw_start:
            start_index = index;
            print("start_index="+str(index))
        #it must get cw_start firstly
        elif (cw_start!= None) and (end_index == None) and (i == cw_end):
            end_index = index;
            print("end_index=" + str(index))
        index+=1;
    # if index has be founded
    #if end_index != None and start_index != None :
        #return cw_list_origin[start_index: end_index+1];
    result = cw_list_origin[start_index: end_index+1];
    #User's input value are out of range.
    # after one pass traverse of the list, if CW_end > max(cw_list), or
    # CW_start < the fist_beginning min(cw_list), then throw an error.
    #cw_end > cw_list_origin[max_index] or cw_start < cw_list_origin[0]:
    if [] == result :
        return None;
    else:
        return result;
def get_slelectedCW_len(cw_list):
    return  cw_list.__len__();

#get the CW length of a unselected list array/list.
def get_cw_len(cw_list_origin, cw_start, cw_end):
    count = 0;
    start = False ;
    for i in cw_list_origin:
        if start:
            count+=1;
            if i == cw_end:
                start = False;
                break;
        else:
            if i == cw_start:
                start = True;
                count+=1;
    return count;

#def getATP_NAT(ATP):


#k考虑是否允许出现end 比 start大的情况
#NOTE: cw_list here must be original CW list.
#def getRealValuelistBySelectedCW(cw_start, cw_end, cw_list, valuelist):



def getRealValuelistBySelectedCW(cw_start, cw_end, cw_list, valuelist):
    #print("Start of getRealValuelistByCW")
    #print("cw_start=" + str(cw_start) + "cw_end=" + str(cw_end))
    #print("valuelist= " + str(valuelist)  )
    l = cw_list.__len__()
    #print("l =  " + str(l)  )
    index_start = -1
    index_end = -1
    print("--------------")
    for index in range(l):
        print(cw_list[index])
        if cw_list[index] == cw_start :
            index_start = index;
        if cw_list[index] == cw_end :
            index_end = index;
    #print("end of getRealValuelistByCW")
    return valuelist[index_start: index_end +1]


#k考虑是否允许出现end 比 start大的情况
#NOTE: cw_list here must be original CW list.
def getRealValuelistByCW(cw_start, cw_end, cw_list_origin, valuelist):
    #print("Start of getRealValuelistByCW")
    #print("cw_start=" + str(cw_start) + "cw_end=" + str(cw_end))
    #print("valuelist= " + str(valuelist)  )
    l = cw_list_origin.__len__()
    #print("l =  " + str(l)  )
    index_start = -1
    index_end = -1
    print("--------------")
    cw_start_found = False
    cw_end_found = False
    for index in range(l):
        print(cw_list_origin[index])
        if not cw_start_found and cw_list_origin[index] == cw_start :
            index_start = index;
            cw_start_found = True;
        if not cw_end_found and cw_list_origin[index] == cw_end :
            index_end = index;
            cw_end_found = True;
        if cw_end_found and cw_start_found:
            break;
    #print("end of getRealValuelistByCW")
    #print([cw_start, cw_end])
    #print([index_start, index_end +1])
    #print(valuelist[index_start: index_end +1])
    return valuelist[index_start: index_end +1]
