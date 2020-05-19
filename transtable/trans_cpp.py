'''
@Author: jia.lai
@Date: 2020-05-16 20:41:15
@LastEditTime: 2020-05-18 17:12:45
@Description: 
@Version: 1.0
'''


################################################################################
import os
import sys
from trans import *

data_type_trans = {
    "sint32": "asInt()",
    "sint64": "asInt64()",
    "uint32": "asUInt()",
    "uint64": "asUInt64()",
    "int": "asInt()",
    "float": "asFloat()",
    "double": "asFloat()",
    "const char*": "asCString()",
    "bool": "asBool()",
    "std::string": "asString()",
    "std::vector<int>": "asInt()",
    "std::vector<float>": "asFloat()",
    "std::vector<double>": "asFloat()",
    "std::vector<std::string>": "asString()"
}

single_tmpl = '                row.%(fields)s = r["%(fields)s"].%(asType)s;\n'

vector_tmpl = '''
                auto end_%(fields)s = r["%(fields)s"].end();
				auto begin_%(fields)s = r["%(fields)s"].end();
				for (auto it = begin_%(fields)s; it != end_%(fields)s; ++it)
				{
					row.%(fields)s.emplace_back(it->%(asType)s);
				}
            '''
#########################################################################################


class TransCpp(Trans):
    def __init__(self):
        pass

    def get_row_fields(self, data_desc, field_desc):
        row_fields = ""
        tmp_field = ""
        for i in range(len(data_desc)):
            x = data_desc[i]
            tmp_field = '\t'+x[1]+" " + x[0] + ";"
            strlen = 50
            field_desc[i] = field_desc[i].replace("\n", " ")
            row_fields += (tmp_field + " " *
                           (strlen-len(tmp_field)) + "// "+field_desc[i])
            row_fields += "\n\t"
        return row_fields

    def get_json_logic(self, data_desc):
        json_logic = ''
        for i in range(len(data_desc)):
            x = data_desc[i]
            if "vector" in x[1]:
                json_logic += (vector_tmpl) % {
                    "fields": x[0], "asType": data_type_trans[x[1]]}
            else:
                json_logic += (single_tmpl) % {
                    "fields": x[0], "asType": data_type_trans[x[1]]}
        return json_logic

    def gen_cpp(self, excel_sheet, table_name, data_desc, field_desc, code_dir):
        if self.is_config(table_name):
            return
        row_fields = self.get_row_fields(data_desc, field_desc)
        json_logic = self.get_json_logic(data_desc)
        s = self.read_tmpl('table_cpp.tmpl')
        if not s:
            return
        key_type = None
        for i in range(len(data_desc)):
            if data_desc[i][0] == 'id':
                key_type = data_desc[i][1]
                break
        s = s % {"class_upper": table_name.upper(),
                 "class_name": table_name,
                 "row_fields": row_fields,
                 "json_logic": json_logic,
                 "key_type": key_type}

        self.write_code(table_name, s, code_dir, 'cpp')
