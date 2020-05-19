'''
@Author: jia.lai
@Date: 2020-05-16 20:40:58
@LastEditTime: 2020-05-18 15:04:48
@Description: 读取excel文件
@Version: 1.0
'''

#######################################################
import os
import sys

count = 3
while count:
    try:
        import xlrd
        from xlrd import xldate_as_tuple
        break
    except Exception as e:
        os.system('pip install xlrd')
        count -= 1
        continue

# 数据类型字典
cpp_type_dic = {
    "INT32": "sint32",
    "INT64": "sint64",
    "UINT32": "uint32",
    "UINT64": "uint64",
    "INT": "int",
    "FLOAT": "float",
    "DOUBLE": "double",
    "STRING": "std::string",
    "CHAR": "const char*",
    "BOOL": "bool",
    "LI": "std::vector<int>",
    "LD": "std::vector<double>",
    "LF": "std::vector<float>",
    "LS": "std::vector<std::string>"
}

cs_type_dic = {
    "INT32": "int",
    "INT64": "long",
    "UINT32": "uint",
    "UINT64": "ulong",
    "INT": "int",
    "FLOAT": "float",
    "DOUBLE": "double",
    "STRING": "string",
    "CHAR": "string",
    "BOOL": "bool",
    "LI": "List<int>",
    "LD": "List<double>",
    "LF": "List<float>",
    "LS": "List<string>"
}
#######################################################


class ReadExcel(object):
    def __init__(self, excel_dir):
        self.excel_dir = excel_dir
        self.table_names = []
        self.filter_cols = []

    def get_excel(self):
        files = os.listdir(self.excel_dir)
        excel_list = [file for file in files if os.path.splitext(file)[
            1] == ".xlsx" and '~' not in file]
        for excel in excel_list:
            name = os.path.splitext(excel)[0]
            self.table_names.append(name.split('_')[0])
        return excel_list, self.table_names

    def check_table_key(self, excel_sheet):
        rows = 5
        rowe = excel_sheet.nrows
        if rowe < rows:
            raise Exception('表头部分配置错误')
        keys = []
        for i in range(5, rowe):
            key = excel_sheet.cell_value(i, 0)
            if key in keys:
                raise Exception('第一列id配置重复：id='+key + ' 第'+str(i+1)+'行')
            else:
                keys.append(key)

    def read_excel(self, excel, output):
        excel_file = xlrd.open_workbook(
            os.path.join(self.excel_dir, excel))
        excel_sheet = excel_file.sheet_by_name(excel_file.sheet_names()[0])
        if not excel_sheet:
            return False, None, None, None, None
        self.check_table_key(excel_sheet)
        row0 = excel_sheet.row_values(0)  # 字段类型
        row1 = excel_sheet.row_values(1)  # 标识是否需要此列数据
        row2 = excel_sheet.row_values(2)  # 字段名称
        row3 = excel_sheet.row_values(3)  # 字段说明
        row4 = excel_sheet.row_values(4)  # 字段说明

        desc1 = []
        desc2 = []
        names = []
        types = []
        table_field = {}
        for i in range(len(row0)):
            if not row0[i]:
                break
            if output == 'cpp' and row1[i] and row1[i] == '1':
                continue
            if output == 'cs' and row1[i] and row1[i] == '2':
                continue
            if row0[i] not in cpp_type_dic.keys():
                raise Exception('ERROR: 表字段类型配置错误')
            if output == 'cpp':
                types.append(cpp_type_dic[row0[i]])
            elif output == 'cs':
                types.append(cs_type_dic[row0[i]])
            if row2[i] not in names:
                names.append(row2[i])
                table_field[row2[i]] = row0[i]
            else:
                raise Exception('ERROR: 表字段名称重复')

            desc1.append(row3[i])
            desc2.append(row4[i])

        field_desc = [a+" "+b for a, b in zip(desc1, desc2)]
        data_desc = list(zip(names, types))

        return True, excel_sheet, field_desc, data_desc, table_field
