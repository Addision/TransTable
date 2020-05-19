'''
@Author: jia.lai
@Date: 2020-05-16 20:41:26
@LastEditTime: 2020-05-19 09:57:32
@Description: 
@Version: 1.0
'''
#######################################################
import os
import sys
from trans import *
#######################################################


class TransCs(Trans):
    def __init__(self):
        pass

    def get_row_fields(self, data_desc, field_desc):
        row_fields = ""
        tmp_field = ""
        for i in range(len(data_desc)):
            x = data_desc[i]
            tmp_field = '\t' + "public " + x[1]+" " + x[0] + " { get; set; };"
            strlen = 50
            field_desc[i] = field_desc[i].replace("\n", " ")
            row_fields += (tmp_field + " " *
                           (strlen-len(tmp_field)) + "// "+field_desc[i])
            row_fields += "\r\n\t"
        return row_fields

    def gen_cs(self, table_name, data_desc, field_desc, code_dir):
        if self.is_config(table_name):
            return
        row_fields = self.get_row_fields(data_desc, field_desc)
        s = self.read_tmpl('table_cs.tmpl')
        if not s:
            return
        key_type = None
        for i in range(len(data_desc)):
            if data_desc[i][0] == 'id':
                key_type = data_desc[i][1]
                break
        s = s % {"class_name": table_name,
                 "row_fields": row_fields, "key_type": key_type}

        self.write_code(table_name, s, code_dir, 'cs')
