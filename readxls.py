import xlrd
class ReadExcel():
    def __init__(self,filename):
        self.data=xlrd.open_workbook(filename)
        self.table=self.data.sheet_by_index(0)
        self.nrows = self.table.nrows
        self.ncols= self.table.ncols

    def read_data(self):
        #返回每一行的数据
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

    def get_row_num(self,caseid):
        """
        根据所给的caseid找到对应的行号，caseid所在列为第1列(从第0列开始算)
        :param caseid:
        :return:caseid所在的行号
        """
        row_num = 0
        for values in self.table.col_values(1):
            if caseid in values:
                return row_num
            else:
                row_num +=1

    def get_row_data(self,caseid):
        """
        根据所有的caisid获取所在行所有的值
        :param caseid:
        :return:caseid所在行的值
        """
        list_row_api = []
        row_num = self.get_row_num(caseid)
        row_data = self.table.row_values(row_num)
        keys = self.table.row_values(0)
        list_row_api.append(dict(zip(keys,row_data)))

        return list_row_api



#list_api=ReadExcel("D:\Guanauto-test\GuanAuto-Test\testapis\yatong_h5_out.xlsx")

#print(list_api.get_row_data("test_out_2"))