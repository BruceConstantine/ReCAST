import json
import time

from django.http import FileResponse
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from ReCAST.DTO.Task import Task
from ReCAST.util.ExcelFileOperator import ExcelFileOpearator


def login(request):
    if request.method == 'POST':
        form = request.POST
        # if form.is_valid():
        uname = form.get('username')
        pw = form.get('password')

        #Write user accouhnt infor into session
        request.session['username'] = uname;
        return render(request, 'index.html')
    elif request.method == 'GET':
        return render(request, 'index.html')

def logout(request):
    # return redirect('http://www.baidu.com')
    return HttpResponse('Login.html')


# Create your views here.
def display(request):
    now_time = time.strftime('%Y-%m-%d %X', time.localtime())
    return render(request, 'modify.html', {'now_time': now_time})


def createTask(request):
    #create task

    return render(request, 'createTask.html')


def config(request):
    task = request.session.get("task") #
    if task == None:
        task = {}
    else :
        task =  json.loads(task)
    if request.method == "POST":
        se = request.session
        taskName = request.POST.get('taskName')
        taskDescription = request.POST.get('taskDescription')
        CW_start = int(request.POST.get('CW_start'))
        CW_end   = int(request.POST.get('CW_end'))
        pid = se.get("pid")
        username = se.get('username')
        #get Scenario list

        task = Task(taskName,taskDescription,'create',username,pid,CW_start,CW_end)
        #Cache task dto into session
        request.session["task"] = task.getJSON()
        task = task.getDict()
        # print(json.loads(request.session.get("task")).get("taskName"))
        # print(json.loads(request.session.get("task"))["tid"])

    return render(request, 'config.html',task)
   # if request.method == "GET":
   #     return render(request, '403.html')

def upload(request):
    if request.method == "POST":
        file = request.FILES['excel_in']
        if file:  # len(request.FILES.keys()) != 0
            # Load Excel data to session
            excel_data_json = ExcelFileOpearator.handle_upload_file(file)  # str(request.FILES['file']) --> None
            # a = request.session.get('username')
            return render(request, 'config.html', {"data":excel_data_json})
            # return HttpResponse(excel_data_json)
    else:
        return render(request, 'createTask.html')
    # return render('course/upload.html')

def downloadManual (request):
        file = open('static/manual/ReCAST_Use_Manual.pdf', 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="ReCAST Use Manual.pdf"'
        return response


def run(request):
    return render(request, 'result.html')


def adv(request):
    return render(request, 'advOpt.html')


def modify(request):
    return None


def export(request):
    return None


def viewHistory(request):
    return render(request, 'createTask.html')


def search(request):
    return None


def save(request):
    return None


def discard(request):
    return None


def quit(request):
    return None


def default(request):
   # return render(request, 'login.html')
    return render(request, 'child.html')


def advOpt(request):
    return render(request, 'advOpt.html')


def register(request):
    return render(request, 'register.html')


def reset(request):
    return render(request, 'reset.html')


def getActiveCode(request):
    return None