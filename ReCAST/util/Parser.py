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
        CW_list = []
        customer = Customer()
        #To check if it is the line for recording date
        seller_count = 0;
        date_list = []
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
                #briefly check for the CW-cells which should be more strict rather than only check if a cell starting with 'CW'
                if str(cell_value).strip().startswith("CW"):
                    try:
                        CW_list.append(int(cell_value.strip()[2:]))
                    except:
                        print('>>>> Error come out <<<<')
                        print(cell_value.strip() + '.')
                        print(cell_value + '.')
                        print('row=' + str(row) + '. , ' + 'col=' + str(col) + '.')
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
                if cell_value == 'Seller': #to get date:
                    seller_count += 1;
                    if seller_count == 2:
                        date_list = sheet.row_values(row)[2:];
                    else:
                        pass;
                if cell_value == 'Confirmed Orders (CMAD)': #'Target Allocation':
                    # TA = TA_row[2:]
                    CMAD = sheet.row_values(row)
                    #customer.setName(CMAD[0])
                    #customer.setCMAD(CMAD[2:])
                    # 如果不提前吧Min RR写在前面就会影响这里的赋值：getMR的赋值
                    customerList.append(Customer(CMAD[0],CMAD[2:]))
                    print("!!!!!!!!! CMAD-"+str(CMAD[0])+": "+str(CMAD[2:]))
                    print("原CMAD整一行："+str(CMAD))
                    print("\n")
            excel_table.append(excel_list)

        #matching CW_list with value list to remove the excess.
        for customer in customerList:
            CMAD = customer.getCMAD();
            CMAD = Parser.trimList(CW_list,CMAD)
            customer.setCMAD(CMAD)

        excel_data = Excel_In(plant_ATP, ATP_NTA_row, customerList, CW_list, excel_table, productName, abs_filename,date_list)
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

    #NOTE: TODO: if this website are deployed on website, it must be multi-threaded as Excel I./O. Cannnot be executed concurrently..
    #here: the value: cw_start, cw_end and length of CW should be considered for selecting time horzion
    #note: date_list here is ready to used.
    @staticmethod
    def parse2_export_file(path, filename, customer_list, customername_list,len_cw, cw_start, product_SP, date_list ):
        #callback
        def __changedContent( ws, customer_list, customername_list,len_cw, cw_start, product_SP, date_list ):
            #TODO: may be need to changed here, the length of cw.
            #print CW list on the forth line
            range_max = 1+len_cw
            for i in range(range_max):
               ws.write(3, 3+i, 'CW' + str(cw_start+i))
               ws.write(4, 3+i, date_list[i])
            #initiate row\col for print out result.
            row = 5;
            # print each customer details at list after the fifth line
            for customer_dict in customer_list:
                #fill the CMAD value into Excel
                print(customer_dict)
                col = 0;
                for value in customer_dict['CMAD']:
                    ws.write(row, 3+col, value)
                    col += 1;
                # fill the product(SP) feild and Measure feild into Excel
                ws.write(row, 0, product_SP )
                ws.write(row, 2, 'TARGET_ALLOCATION' )
                # fill the customer name into Excel
                print(customername_list)
                ws.write(row, 1, customername_list[row-5])
                row += 1;
            #TODO:  extract the following code as a method:
            #compare cw length and each line at the to see if there is any garbage date, and clean it.
            customer_col_max = len(customername_list)
            introduction_col_max = 1;
            sheet = excel_file.sheet_by_index(0)
            max_row_num = sheet.nrows
            for row in range(0, max_row_num):
                #TODO:it shuold not sheet, rather the row!
                max_col_num = sheet.ncols
                if row < 3:
                    if max_col_num == 1:
                        pass;
                    else:
                        #modify the extra col, to remove it.
                        pass;
                else:
                    if max_col_num < len_cw:
                        #error!
                        pass;
                    elif max_col_num == len_cw:
                        pass;# correct
                    else:
                        #remove the extra cell or set as '' (empty)
                        pass;
            #finally input the introduction data into excel file
            ws.write(0, 0 , 'PRODUCT Field Values can be either SalesProduct (SP) or Finished Product (MA) ')
            ws.write(1, 0 , 'MEASURE Field values can be TARGET_ALLOCATION or MIN_RUNRATE ')
            ws.write(2, 0 , 'DF_SELLER should be Leaf Sellers at which Allocations has to be maintained.')

        abs_filename = path + filename;
        # abs_filename format e.g. -->  c/2020-05-28@15_27_06
        print(abs_filename)
        excel_file = xlrd.open_workbook(abs_filename)
        sheet = excel_file.sheet_by_index(0)
        max_row_num = sheet.nrows
        max_col_num = sheet.ncols
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
        __changedContent( ws, customer_list, customername_list,len_cw, cw_start, product_SP, date_list );

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

    # if two list length are not match, then remove the last few element at the value_list so to keep same length as the cw_list
    @staticmethod
    def trimList(cw_list, value_list):
        len_cw_list    = cw_list.__len__();
        len_value_list = value_list.__len__();
        if len_cw_list == len_value_list:
            pass;
        else :
            redundant = abs(len_value_list-len_cw_list)
            for i in range(redundant): #remove the cell at end of value list
                value_list.pop();
            #for i, item in enumerate(value_list):
            #    if item == '' or item == None:
            #        value_list[i].;
        return value_list;

    @staticmethod
    def trimCWList( cw_list ):
        #reverse
        cw_list.reverse();
        continue_to_pop = True;
        for cw in cw_list: #remove the cell at end of value list
            if continue_to_pop:
                if str(cw).strip() == '' or None == cw:
                    cw_list.pop();
                else:
                    continue_to_pop = False;
            else:
                print("triming list:"+str(cw_list))
                return cw_list.reverse();
