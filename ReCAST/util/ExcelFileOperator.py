import os
import time

import xlrd
from xlutils.copy import copy

from ReCAST.DO.Customer import Customer
from ReCAST.DO.Excel_In import Excel_In


from ReCAST.util.Parser import Parser

#static method for extracting method modularly
#其实可以直接不用写static method和类，直接一个函数怼上去行
# Parser模块也是。
class ExcelFileOpearator():
    def __init__(self):
        pass

    @staticmethod
    def handle_upload_file(file): #, CW_start):
        # 产生一个独一无二的文件名-这里用时间作为文件名->只是一个暂时处理用的，读入数据后立马删除了。
        current_time = time.strftime('%Y-%m-%d@%X', time.localtime())
        filename = current_time.replace(":", "_")
        # TODO: path 要重构出一个config文件来
        path = '/media/uploads/'  # 上传文件的保存路径，可以自己指定任意的路径
        abs_filename = path + filename
        if not os.path.exists(path):
            print(os.makedirs(path))
        #else:
            # file path already exist
        with open(abs_filename, 'wb+') as destination:  # open返回一个文件对象
            for chunk in file.chunks():
                destination.write(chunk)
        destination.close()
        return Parser.parse_upload_file(abs_filename )
    '''
        def upload_views(request):
            # 请求方法为POST时,进行处理;
            if request.method == "POST":
                # 获取上传的用户名称
                uname = request.POST['uname']
                #查询wenjian表中与用户为登陆用户的一直到文件数据
                L = wenjian.objects.filter(uname=uname,gxname='')
                L1 = wenjian.objects.filter(uname=uname,gxname='1')
                # 获取上传的文件,如果没有文件,则默认为None;
                File = request.FILES.get("myfile", None)
                if File is None:
                    a='请选择上传文件!'
                    return render(request,'sym.html',locals())
                else:
                    #判断该用户上传文件目录下是否有本次上传文件
                    lujing = "./index/templates/文件/"+"%s"%str(uname)+"/"+"%s"%File.name
                    #用户已上传本次上传文件
                    if File.name in os.listdir(r"./index/templates/文件/"+"%s"%str(uname)):
                        a='你已上传%s,上传失败!'%File.name
                        return render(request,'sym.html',locals())
                    else:
                        # 打开特定的文件进行二进制的写操作;
                        with open(lujing,'wb+') as f:
                            # 分块写入文件;
                            for chunk in File.chunks():
                                f.write(chunk)
                        #文件信息存储到数据库
                        dic={
                            'wenjian':File.name,
                            'lujing':lujing,
                            'uname':uname,
                        }
                        wenjian(**dic).save()
                        a='上传成功!!'
                        return render(request,'sym.html',locals())
    '''


    @staticmethod
    def export_result_excel(path, filename):  # , CW_start):
        # callback
        def __changedContent(ws):
            ws.write(5, 0, 'changed!')

        abs_filename = path + filename;
        # abs_filename format e.g. -->  c/2020-05-28@15_27_06
        print(abs_filename)
        excel_file = xlrd.open_workbook(abs_filename)
        sheet = excel_file.sheet_by_index(0)
        max_row_num = sheet.nrows
        max_col_num = sheet.ncols
        excel_table = []
        # plantATP or PlantATP(Adj)
        # customerList = []
        # customer = Customer()
        # xlrd和xlwt不能处理 Xlsx ，但可以学习下面的链接使用XlsxWrite，但是操作麻烦：
        # https://github.com/jmcnamara/XlsxWriter
        # https://blog.csdn.net/JasonTang1992/article/details/84074697?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-21.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-21.nonecase
        output_excel = copy(excel_file)
        ws = output_excel.get_sheet(0)

        # callback
        __changedContent(ws)

        # path = '/static/excel/temp/'
        # filename -> RLCusername + Timestamp
        filename = 'TargetAllocation_result.xls'
        output_excel.save(  # path +
            filename)
        return filename  # + path
