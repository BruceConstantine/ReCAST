import xlrd

from ReCAST.DO.Customer import Customer
from ReCAST.DO.Excel_In import Excel_In


class Parser():
    def __init__(self):
        pass

    @staticmethod
    def parse_upload_file(abs_filename):
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
        excel_list = []
        #plantATP or PlantATP(Adj)
        plantATP = []
        customerList = []
        customer = Customer()
        # 再遍历所有行
        for row in range(0, max_row_num):
            for col in range(max_col_num):
                # 获取单元格数据
                cell_value = sheet.cell(row, col).value
                # 把数据追加到excel_list中
                excel_list.append(cell_value)
                # 如果发现Plant ATP的cell，就检测所在行，获取这一行的所有值。
                if cell_value == 'Plant ATP (Adj)':
                    pass
                if cell_value == 'Plant ATP':
                    plant_ATP = sheet.row_values(row)
                    print(plant_ATP)
                elif cell_value == 'Min. Run Rate':
                    MR_row = sheet.row_values(row)
                    customer.setMR(MR_row[2:])
                # 这里要把Min.Run Rate写在前面，因为在表中就是Min Run Rate 就是在前面，
                elif cell_value == 'Target Allocation':
                    TA_row = sheet.row_values(row)
                    TA = TA_row[2:]
                    customer.setName(sheet.row_values(row)[0])
                    customer.setTA(TA_row[2:])
                    # 如果不提前吧Min RR写在前面就会影响这里的赋值：getMR的赋值
                    customerList.append(Customer(customer.getName(), customer.getTA(), customer.getMR()))

        excel = Excel_In(plant_ATP, customerList)
        print(excel.getJSON())
        # print(excel_list)
        # return  column
        print('done')
        return excel.getJSON()

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
