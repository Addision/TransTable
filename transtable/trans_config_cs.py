'''
@Author: jia.lai
@Date: 2020-05-18 10:03:45
@LastEditTime: 2020-05-19 09:57:21
@Description: 转换配置表为cs
@Version: 1.0
'''

#######################################################
import sys
import os
import codecs
from trans import *
#######################################################


class TransConfigCs(Trans):
    def __init__(self):
        pass

    def get_row_fields(self, data_desc, field_desc):
        row_fields = ""
        tmp_field = ""
        for i in range(len(data_desc)):
            x = data_desc[i]
            tmp_field = '\t' + "public " + x[1]+" " + x[0] + ";"
            strlen = 50
            field_desc[i] = field_desc[i].replace("\n", " ")
            row_fields += (tmp_field + " " *
                           (strlen-len(tmp_field)) + "// "+field_desc[i])
            row_fields += "\r\n\t"
        return row_fields

    def gen_config(self, table_name, data_desc, field_desc, code_dir):
        if not self.is_config(table_name):
            return
        row_fields = self.get_row_fields(data_desc, field_desc)
        s = self.read_tmpl('table_config_cs.tmpl')
        if not s:
            return

        key_type = data_desc[0][1]
        conf_key_type = data_desc[1][1]
        conf_name = data_desc[1][0]

        s = s % {"class_name": table_name,
                 "row_fields": row_fields,
                 "key_type": key_type,
                 "conf_key_type": conf_key_type,
                 "conf_name": conf_name}

        self.write_code(table_name, s, code_dir, 'cs')
