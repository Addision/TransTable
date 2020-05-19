'''
@Author: jia.lai
@Date: 2020-05-18 13:21:21
@LastEditTime: 2020-05-18 17:11:31
@Description: 转换基类
@Version: 1.0
'''

#######################################################
import os
import sys
import json
import codecs
from read_excel import *
#######################################################


class Trans(object):
    def __init__(self):
        pass

    def is_config(self, table_name):
        if 'Enum' in table_name:
            return True
        return False

    # 读取模板文件
    def read_tmpl(self, tmpl_name):
        s = ""
        tmpl_file = os.path.join(os.path.dirname(__file__), tmpl_name)
        with codecs.open(tmpl_file, "r", "utf-8") as f:
            s = f.read()
        if not s:
            return None
        return s

    # 保存生成代码文件
    def write_code(self, table_name, content, code_dir, output):
        encoding = 'utf-8'
        if output == 'cpp':
            file_name = 'Table'+table_name+'.hpp'
            encoding = 'GB2312'
        elif output == 'cs':
            file_name = 'Table'+table_name+'.cs'
        code_file = os.path.join(code_dir, file_name)
        with codecs.open(code_file, "w", encoding) as f:
            f.write(content)
            f.flush()

    # 生成json文件
    def write_json(self, table_name, json_rows, json_dir):
        json_file = os.path.join(json_dir, table_name+'.json')
        with codecs.open(json_file, 'w', "utf-8") as f:
            json_str = json.dumps(json_rows, indent=4,
                                  sort_keys=False, ensure_ascii=False)
            f.write(json_str + '\n')
            f.flush()


class TransConfig(Trans):
    def __init__(self, table_field, tmpl_name):
        self.table_field = table_field
        self.tmpl_name = tmpl_name
        pass

    def fix_row_field(self, excel_sheet, rows, type_dic):
        ncols = excel_sheet.ncols
        row_values = excel_sheet.row_values(rows)
        value_type = excel_sheet.row_values(0)[2]
        if not value_type in type_dic.keys():
            return None
        field_type = type_dic[value_type]
        field_name = str(row_values[1])
        field_value = None
        if value_type in ['INT32', 'INT64', 'UINT32', 'UINT64', 'INT']:
            field_value = int(row_values[2])
        if value_type in ['FLOAT', 'DOUBLE']:
            field_value = float(row_values[2])
        if value_type in ['STRING', 'CHAR']:
            field_value = str(row_values[2])

        row_field = ''
        row_field = self.table_field % {"field_type": field_type,
                                        "field_name": field_name,
                                        "field_value": field_value}
        return row_field

    def get_row_fields(self, excel_sheet, output):
        type_dic = None
        if output == 'cpp':
            type_dic = cpp_type_dic
        elif output == 'cs':
            type_dic = cs_type_dic
        row_fields = ''
        rows = 5
        rowe = excel_sheet.nrows
        while rows < rowe:
            row_field = self.fix_row_field(excel_sheet, rows, type_dic)
            if not row_field:
                continue
            row_fields += '\t'+row_field + '\n\t'
            rows = rows + 1
        return row_fields

    def gen_config(self, excel_sheet, table_name, output, code_dir):
        if not self.is_config(table_name):
            return
        row_fields = self.get_row_fields(excel_sheet, output)
        if not row_fields:
            return
        s = self.read_tmpl(self.tmpl_name)
        if output == 'cpp':
            s = s % {"class_upper": table_name.upper(),
                     "class_name": table_name,
                     "row_fields": row_fields}
        elif output == 'cs':
            s = s % {"class_name": table_name,
                     "row_fields": row_fields}

        self.write_code(table_name, s, code_dir, output)
