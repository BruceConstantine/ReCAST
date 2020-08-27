import xlrd
from xlutils.copy import copy

from ReCAST.DO.Customer import Customer
from ReCAST.DO.Excel_In import Excel_In


'''python操作excel的三个工具包如下，注意，只能操作.xls，不能操作.xlsx。
        xlrd: 对excel进行读相关操作
        xlwt: 对excel进行写相关操作
        xlutils: 对excel读写操作的整合
'''

class Parser():
    def __init__(self):
        pass
    '''
    Algorithm for reading all required data at excel file.
    Step 1. Load excel from frontend and post it to server.
    Step 2. Open file and read it line by line.
    Step 3. If there is a row called ‘PlantATP(Adj)’ at the file, then read the line.
            Else if there is row of ‘PlantATP’, then read it. 
    Step 4. Get the first CW value of ‘ATP vs Net Target Alloc (Cum)’ 
    Step 5. Read the line of ‘Confirmed Orders (CDMA)’ within the specific CW period for each customer/seller
    '''
    @staticmethod
    def parse_upload_file(abs_filename):
        # abs_filename format e.g. -->  /media/uploads/2020-05-28@15_27_06
        excel_file = xlrd.open_workbook(abs_filename)
        sheet = excel_file.sheet_by_index(0)
        max_row_num = sheet.nrows
        max_col_num = sheet.ncols
        '''
        customer_name_list = []
        #遍历第一列，在唯一的WF00 Seller之后找出所有Customer.
        #读取第一列的Seller，来计算是否已经读取到第二个seller之后了，是的话就可以开始录取Customer了
        afterSeller_count = 0
        seller_col = sheet.col_values(0)
        for row in range(max_row_num):
            cell_value = seller_col[row]
            if afterSeller_count <= 1:
                this_customer = '' #当前Customer初始化
                if cell_value == 'Seller':
                    afterSeller_count += 1
            else: # afterSeller_count >= 2:  # 只有当过去第二个Seller后才能算作开始计算Customer
                last_customer = this_customer
                this_customer = cell_value
                if this_customer == last_customer:
                    # 连着值一样的都是一个Customer，不予考虑
                    pass
                else:
                    #值发生了变化就是新的customer
                    customer_name_list.append(this_customer)
        print(customer_name_list)
        '''
        excel_table = []
        #plantATP or PlantATP(Adj)
        customerList = []
        productName=''
        ATP_NTA_row=[]
        customer = Customer()
        # 再遍历所有行
        for row in range(0, max_row_num):
            excel_list = []
            productName_found = False
            ATP_NTA_row_found = False
            plant_ATP_found = False
            for col in range(max_col_num):
                # 获取单元格数据
                cell_value = sheet.cell(row, col).value
                # 把数据追加到excel_list中
                excel_list.append(cell_value)
                # 如果发现Plant ATP的cell，就检测所在行，获取这一行的所有值。
                if cell_value ==  'Plant ATP (Adj)':
                    plant_ATP = sheet.row_values(row)[2:]
                    plant_ATP_found = True
                if not plant_ATP_found and cell_value ==  'Plant ATP':
                    plant_ATP = sheet.row_values(row)[2:]
                if not productName_found :
                    if type(cell_value) == str: # must be 'str' type
                        if cell_value.startswith("Product") and cell_value.__contains__('SP') :
                            productName = list(filter(lambda str: str.startswith('SP'), cell_value.split(' ')))[0]
                            productName_found = True
                if not ATP_NTA_row_found and  cell_value == 'ATP vs Net Target Alloc (Cum)': #'Min. Run Rate':
                    ATP_NTA_row = sheet.row_values(row)[2:]
                    ATP_NTA_row_found = True
                    # customer.setMR(MR_row[2:])
                # 这里要把Min.Run Rate写在前面，因为在表中就是Min Run Rate 就是在前面，
                if cell_value == 'Confirmed Orders (CMAD)': #'Target Allocation':
                    # TA = TA_row[2:]
                    CMAD = sheet.row_values(row)
                    customer.setName(CMAD[0])
                    customer.setCMAD(CMAD[2:])
                    # 如果不提前吧Min RR写在前面就会影响这里的赋值：getMR的赋值
                    customerList.append(Customer(customer.getName(),customer.getCMAD()))
            excel_table.append(excel_list)
        excel_data = Excel_In(plant_ATP, ATP_NTA_row, customerList, excel_table, productName)
        # print(excel_data.getJSON())
        # print(excel_table)
        # return  column
        # print('done')
        return excel_data.getJSON()

        '''
    import pandas as pd
    def parse_upload_file(abs_filename):
        df = pd.read_excel(abs_filename, sheet_name=[0]) #使用pandas读取第一个sheet
        #print(df)
        print(df.keys())
       # sheet = df["Sheet1"] #打开sheet1->Excel的第一张表
        #column = sheet[0]
       # return  column
    '''
    @staticmethod
    def parse2_export_file(path, filename):
        #callback
        def __changedContent( ws ):
            ws.write(5, 0, 'changed!')

        abs_filename = path + filename;
        # abs_filename format e.g. -->  c/2020-05-28@15_27_06
        print(abs_filename)
        excel_file = xlrd.open_workbook(abs_filename)
        sheet = excel_file.sheet_by_index(0)
        max_row_num = sheet.nrows
        max_col_num = sheet.ncols
        excel_table = []
        excel_table = []
        # plantATP or PlantATP(Adj)
        #customerList = []
        #customer = Customer()
        # xlrd和xlwt不能处理 Xlsx ，但可以学习下面的链接使用XlsxWrite，但是操作麻烦：
        # https://github.com/jmcnamara/XlsxWriter
        # https://blog.csdn.net/JasonTang1992/article/details/84074697?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-21.nonecase&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-21.nonecase
        output_excel = copy(excel_file)
        ws = output_excel.get_sheet(0)

        #callback
        __changedContent(ws)

        #path = '/static/excel/temp/'
        #filename -> RLCusername + Timestamp
        filename = 'TargetAllocation_result.xls'
        output_excel.save( #path +
                           filename )
        return filename # + path

        # for row in range(0, max_row_num):
        #     excel_list = []
        #     for col in range(max_col_num):
        #         # 获取单元格数据
        #         cell_value = sheet.cell(row, col).value
        #         # 把数据追加到excel_list中
        #         excel_list.append(cell_value)
        #         # 如果发现Plant ATP的cell，就检测所在行，获取这一行的所有值。
        #         if cell_value == 'Plant ATP':
        #             plant_ATP = sheet.row_values(row)[2:]
        #         if cell_value == 'Plant ATP (Adj)':
        #             plant_ATP = sheet.row_values(row)[2:]
        #         elif cell_value == 'ATP vs Net Target Alloc (Cum)':  # 'Min. Run Rate':
        #             ATP_NTA_row = sheet.row_values(row)[2:]
        #             # customer.setMR(MR_row[2:])
        #         # 这里要把Min.Run Rate写在前面，因为在表中就是Min Run Rate 就是在前面，
        #         elif cell_value == 'Confirmed Orders (CMAD)':  # 'Target Allocation':
        #             # TA = TA_row[2:]
        #             CMAD = sheet.row_values(row)
        #             customer.setName(CMAD[0])
        #             customer.setCMAD(CMAD[2:])
        #             # 如果不提前吧Min RR写在前面就会影响这里的赋值：getMR的赋值
        #             customerList.append(Customer(customer.getName(), customer.getCMAD()))
        #     excel_table.append(excel_list)
        #
        # excel_data = Excel_In(plant_ATP, ATP_NTA_row, customerList, excel_table)
        # print(excel_data.getJSON())
        # # print(excel_table)
        # # return  column
        # # print('done')
        # return excel_data.getJSON()



