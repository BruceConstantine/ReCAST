import json
import os
import time
import random

from django.contrib.auth import authenticate
from django.http import FileResponse
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect

#from ReCAST.DTO import DataTransferObj_GurobiInterface
from ReCAST.DO import Gurobi_Algo
from ReCAST.DTO.Scenario import Scenario
from ReCAST.DTO.Task import Task
from ReCAST.models import Task as Taskmodel
from ReCAST.models import User as Usermodel
from ReCAST.util import WebUtils, Algo
from ReCAST.util.ExcelFileOperator import ExcelFileOpearator
from ReCAST.util.HTMLGenerator import *
from ReCAST.util.Parser import Parser

from django.core.mail import send_mail
from gurobipy import *
import pandas as pd
import numpy as np


def index(request):
    #print(request.headers)
    if request.method == 'POST':
        form = request.POST
        # if form.is_valid():
        uname = form.get('username')
        # * SSL at HTTPS protocol shall encoding its content for confidentiality
        #   But another method is passing the Hash value instead of the plaintext password -> but hacker may can know the encrypting algorithm.
        password = form.get('password')
        hasspw = WebUtils.get_hashDigest_0x(password)
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
                return render(request, 'login.html', {'msg': "Password not correct"})
        else: # if user not exist
            # Refactor: return render(request, 'login.html', {"msg": user is not registered})
            return render(request, 'login.html', {'msg': "Username not exist"})
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
    # This statement only for test.
    return render(request, 'createTask.html')
    #correct one should be this statement:
    #__createTask(request);

def __createTask(request):
    # This means the request must from a page rather than user'input or GET method HTTP request.
    #request.headers['type'] is string type.
    if request.headers.__contains__('Referer'):
        url_origin = request.headers['Referer']
        print("url_origin = "+str(url_origin))
        if WebUtils.getRouter(url_origin) in ['index', 'config'] :
            return render(request, 'createTask.html')
        elif request.method == "POST":
            print("createTask invoked by: POST, request.session['username'] = "+str(request.session['username']))
            return render(request, 'createTask.html') # ,{"data":[]} initialization
        #TODO: check here!
        elif request.method == "GET":
            print("createTask invoked by: GET, request.session['username'] = "+str(request.session['username']))
            if request.session['username'] == None:
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
            #TODO: alert window here.!.
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
            print( request.session["customerList" ]   )
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

'''
def config(request):
    try:
        __config(request);
    except:
        return HttpResponse(back_previews_page_html_str_with_alert("Input parameters incorrect"))
'''

def config(request):
    #task = WebUtils.getTaskAtSession(request)
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
        print("at config: packingUnit="+str(packingUnit))
        #TODO: bug here, we can't use absoluate value directly to get the len,as its length is not centainable
        #request.session['CW_len']  = abs(CW_end-CW_start)
        cw_list_origin = request.session['CW_list']
        #request.session['CW_list'] = generateCWList(cw_list_origin, CW_start, CW_end);
        cw_select = Algo.select_cw_arr(CW_start, CW_end,cw_list_origin);
        #request.session['CW_select'] = cw_select
        request.session["CW_list"] = cw_select.getSelectedArr();
        request.session['CW_len'] = len(request.session['CW_list']);

        request.session['CW_start']  = cw_select.firstElement();
        request.session['CW_end']  = cw_select.lastElement();
        request.session['CW_start_index']  = cw_select.get_originArrIndex_startElement();
        request.session['CW_end_index']  = cw_select.get_originArrIndex_endElement();
        request.session['ATP_NAT_index_at_origin_CW_list']  = cw_select.get_originArrIndex_startElement();

        print("CW_start_index="+str(request.session['CW_start_index']))
        print("CW_end_index="+str(request.session['CW_end_index']) )

        #update PlantATP once CW start\end are given
        #request.session["plantATP"] = getRealValuelistByCW(CW_start,CW_end,cw_list_origin, request.session['plantATP'] )

        print("config: plantATP " + str())
        index_start = request.session["CW_start_index"];
        index_end = request.session["CW_end_index"];
        request.session["plantATP"] = request.session["plantATP"][ index_start : 1 + index_end ]
        #request.session["plantATP"] = getRealValuelistByCW(CW_start,CW_end,cw_list_origin, request.session['plantATP'] )
        print('request.session["plantATP"] = '+str(request.session["plantATP"] ))

        # NOTE: update date_list
        print("Before: request.session['date_list']="+str(request.session["date_list"]))
        #Error Here, abandon this method for selecting.
        #request.session["date_list"] = getRealValuelistByCW(CW_start, CW_end, cw_list_origin,  request.session["date_list"])
        request.session['date_list'] = request.session['date_list'] [index_start : 1+index_end]
        print("request.session['date_list']="+str(request.session["date_list"]))


        #record the original CMAD for each customer
        origin_CMAD_order = []
        CMAD_order = []
        customer_unparsed_dictlist = request.session["customerList"]
        print("customer_unparsed_dictlist:"+str(customer_unparsed_dictlist))
        for customerDict in customer_unparsed_dictlist:
            # selectedCMADList = getRealValuelistByCW(cw_start=CW_start, cw_end=CW_end,
            #                                                 cw_list_origin=cw_list_origin,
            #                                             valuelist=customerDict["CMAD"]);
            #TODO: bug here
            origin_CMAD_order.append(customerDict["CMAD"]);
            customerDict["CMAD"] = customerDict["CMAD"][index_start : 1+index_end];
            CMAD_order.append(customerDict["CMAD"]);
        request.session["origin_CMAD_order"] = origin_CMAD_order
        request.session["CMAD_order"] = CMAD_order
        print(' request.session["origin_CMAD_order"]='+str(request.session["origin_CMAD_order"]))
        request.session["customerList"]=customer_unparsed_dictlist
        print(request.session["CMAD_order"] )
        #print(request.session["customerList"])

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
        #i = get_index_atSelectedCWList(request.session["CW_list"], CW_start)
        print('request.session["ATP_NTA_row"]')
        print(request.session["ATP_NTA_row"])
        #print(i)
        ATP_NTA =  request.session["ATP_NTA_row"][request.session['ATP_NAT_index_at_origin_CW_list']]
        #ATP_NTA = getRealValuelistByCW(cw_start=CW_start, cw_end=CW_end,cw_list_origin=cw_list_origin, valuelist=request.session["ATP_NTA_row"])
        #ATP_NTA = getRealValuelistBySelectedCW(cw_start=CW_start, cw_end=CW_end,cw_list=cw_list_origin, valuelist=request.session["ATP_NTA_row"])

        #ATP_NTA = ATP_NTA[0]

        print("-------------")
        print("in view.config: ATP_NTA = "+str(ATP_NTA))
        print("-------------")

        customerList = request.session["customerList"]
        username = request.session["username"]
        currentPage = 'createTask'
        CW_length = request.session['CW_len']
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
        task = Task(taskName=taskName, taskDescription=taskDescription, currentPage=currentPage, username=username,
                    pid=pid, CW_start=CW_start, CW_end=CW_end, packingUnit=packingUnit,
                    plantATP=plantATP, ATP_NTA=ATP_NTA, scenarioList=scenarioList,CW_length=CW_length)
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
        # print(json.loads(request.session.get("task"))["tid"])
        # task = task.getJSON()

    taskDict = WebUtils.getTaskAtSession(request)#request.session["task"] ;

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
    task = WebUtils.getTaskAtSession(request);
    #Here we have problem for: access ReCAST running GUrobi at page config.html
    if request.method == "GET":
        #do nothing, as POST has done previously.
        pass;
    elif request.method == "POST":
        task["maxDelay"] = request.POST.get('maxdelay')
        # what type of task["MBS"] is ? a big string.
        """
        task["MBS"] =request.GET.get('MBS')
        task["bin_use_from_stock"] =  json.loads(request.GET.get('bin_use_from_stock'))
        task["RBS"] =request.GET.get('RBS')
        """
        task["RBS"] =request.POST.get('RBS');
        task["MBS"] =request.POST.get('MBS');

        bin_use_from_stock_list = json.loads(request.POST.get('bin_use_from_stock'));
        ''' #json.loads() will take the str as the list of int list.
        print(" request.POST.get('bin_use_from_stock') = " + str( bin_use_from_stock ));
        print(" typeof('bin_use_from_stock') = " + str( type(bin_use_from_stock )) );
        print(" typeof('bin_use_from_stock') = " + str( type(bin_use_from_stock[0] )) );
        print(" typeof('bin_use_from_stock') = " + str( type(bin_use_from_stock[0][0] )) );
        '''
        task["bin_use_from_stock"] =  bin_use_from_stock_list;

        request.session["task"]=task;
        print(task)
        print('request.session["username"]=')
        print(request.session["username"])
        #resultlist = DataTransferObj_GurobiInterface.run_with_Task(task)
        #dl=json.dumps(resultlist)
    datalist = [[93, 93, 0, 100.01], [20, 23, 26, 29]]
    dl=json.dumps(datalist)
    #customerList = run_gurobi(abs_filename=request.session["filename_upload"],
    print("before run Gurobi:"+str(request.session["customerList"]))
    try:
        scenarioList_objList = Gurobi_Algo.run_gurobi(abs_filename = request.session["filename_upload"],
                                  CW_start = task['CW_start'],
                                  CW_end   = task['CW_end'],
                                  CW_start_date = None, CW_end_date = None,
                                  packingUnit_in= task["packingUnit"],
                                  MBS_in = task["MBS"], RBS_in = task["RBS"],
                                  plantATP_in = task["plantATP"],
                                  ComfirmedOrder_in = request.session["customerList"],
                                  #ComfirmedOrder_in=request.session["origin_CMAD_order"],
                                  bin_usefrom_stock_in = task["bin_use_from_stock"],
                                  ATP_NTA_in = int(task["ATP_NTA"]),
                                  scenarioList_in = task["scenarioList"],
                                  maxDelay_in = task["maxDelay"],
                                  date_list_in = request.session['date_list']
                              )
    except :
        scenarioList_objList = None;
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
                    'plantATP':json.dumps(task["plantATP"]),
                    'ATP_NTA':json.dumps(task["ATP_NTA"]), #a row rather than ATP_NTA vlaue,
                     #'origin_CMAD_order': request.session["origin_CMAD_order"],
                    'CMAD_order': request.session["CMAD_order"],
                    'scenarioList_objList': scenarioList_objList,
                     #'customerNameList':json.dumps(Scenario.customerNameList),
                    'customerNameList':Scenario.customerNameList,
                    'customerList':json.dumps(request.session["customerList"]),
                    'customerList_forTemplate':request.session["customerList"],
                    #'customerList':json.dumps(customerList),
                    'datalist': dl})

def adv(request):
    print(request.headers)
    #Host
    url_origin = request.headers['Host']
    #Referer
    #differ(Referer,Host)
    #url_origin = request.headers['Referer']
    if WebUtils.getRouter(url_origin) != "config":
        return render(request, 'config.html')
    return render(request, 'advOpt.html')


def modify(request):
    taskDict = WebUtils.getTaskAtSession(request);
    scenarioList_objList = request.session["scenarioList_objList"];
    scenario_no =int( request.GET.get('s',1).strip());
    scenario_index = scenario_no - 1;
    #the selected scenario is actually the list of dictionary for each customer for one scenario case
    selected_scenario = scenarioList_objList[scenario_index];
    selected_customerList = selected_scenario['customerList'];
    print(selected_scenario)
    return render(request, 'modify.html', {"CW_list" : request.session['CW_list'],
                    'plantATP':json.dumps(taskDict["plantATP"]),
                    'ATP_NTA':json.dumps(taskDict["ATP_NTA"]), #[0],
                    'customerNameList' : Scenario.customerNameList,
                    'customerList':json.dumps(selected_customerList) })

def export(request):
    selected_scenario_index__POST = request.POST.get("selected_scenario_index");
    if selected_scenario_index__POST == '' or selected_scenario_index__POST == None:
        return HttpResponse(back_previews_page_html_str_with_alert(
            "Please select a scenario before export!"));
        pass;
    else:
        selected_scenario_index = int(selected_scenario_index__POST)
        print("selected_scenario_index:"+str(selected_scenario_index))
        customer_list = request.session['scenarioList_objList'][selected_scenario_index]['customerList'];
        basedir = os.path.dirname(__file__)
        filename = 'Allocation_Template.xlsx'
        path = basedir ;
        path += "/static/excel/";
        #path += "/static/excel/";

        print('request.session["date_list"]='+str(request.session["date_list"]))

        targetFilePath = Parser.parse2_export_file(path=path, filename=filename,
                                                   customer_list = customer_list,
                                                   customername_list = Scenario.customerNameList,
                                                   len_cw = request.session['CW_len'],
                                                   cw_start = request.session['CW_start'],
                                                   product_SP = request.session['pid'],
                                                   date_list = request.session["date_list"],
                                                   #start_index = request.session['CW_start_index'],
                                                   #end_index = request.session['CW_end_index']
                                                   cw_list = request.session["CW_list"])

        # Test
        print(targetFilePath);

        file = open(targetFilePath, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="Allocation_Template.xls"'
        return response

def viewHistory(request):
    tasklist_all_list = []
    task_ongoing_list = []
    task_finished_list = []
    tasklist_all = Taskmodel.objects.all()
    # print(tasklist_all.__dict__) 不适用->因为.__dict__不是返回数据
    for eachtask in tasklist_all:
        #task = Task.copy(eachtask)
        #print(task.getDict())
        dict_task = eachtask.getDict();
        tasklist_all_list.append(dict_task)
        # if task not finished, TA_rid shall not be assigned as a number, ranther is None.
        if dict_task["TA_rid"] == None:
            task_ongoing_list.append(dict_task);
        #if task finished
        elif type(dict_task["TA_rid"]) is type(0):
            task_finished_list.append(dict_task);
    return render(request, 'histroy.html',{
        'tasklist':tasklist_all_list,
        'task_finished_list':task_finished_list,
        'task_ongoing_list':task_ongoing_list
    });


def details(request):
    targetTasks = [];
    tid = request.POST.get('tid');
    if tid != None :
        tid = tid.strip()
        # Query
        targetTasks = Taskmodel.objects.filter(tid=tid)
    else:
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
        hasspw = WebUtils.get_hashDigest_0x(password)
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
    user.hassPW = WebUtils.get_hashDigest_0x(request.POST.get("password"))
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
        taskDict = WebUtils.getTaskAtSession(request)
        # customerList = run_gurobi(abs_filename=request.session["filename_upload"],
        scenarioList_objList = Gurobi_Algo.run_gurobi(abs_filename=request.session["filename_upload"],
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

