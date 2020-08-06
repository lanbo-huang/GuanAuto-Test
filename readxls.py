import xlrd
class ReadExcel():
    def __init__(self,filename):
        self.data=xlrd.open_workbook(filename)
        self.table=self.data.sheet_by_index(0)
        self.nrows = self.table.nrows
        self.ncols= self.table.ncols

    def read_data(self):
        if self.nrows >1:
            keys = self.table.row_values(0)#d第一行表头信息
            list_api_data =[]
            for col in range(1,self.nrows):
                values =self.table.row_values(col)#取第二行开始的数据
                api_dict = dict(zip(keys,values))
                list_api_data.append(api_dict)
            return list_api_data
        else:
            print('表格是空数据')
            return None

#list_api=ReadExcel("yatong.xlsx").read_data()
#print(list_api)