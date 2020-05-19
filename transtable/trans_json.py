'''
@Author: jia.lai
@Date: 2020-05-16 22:34:56
@LastEditTime: 2020-05-19 16:03:43
@Description: 将excel表转成json保存
@Version: 1.0
'''
#######################################################
import os
import sys
import codecs
import json
import traceback
#######################################################


class TransJson(object):
    def __init__(self):
        pass

    def fix_json_row(self, excel_sheet, nrow, table_field):
        ncols = excel_sheet.ncols
        row_values = excel_sheet.row_values(nrow)
        json_row_dict = {}
        for i in range(ncols):
            if excel_sheet.row_values(2)[i] not in table_field.keys():
                continue
            if not row_values[i]:
                row_values[i] = ''
            field_type = excel_sheet.row_values(0)[i]
            field_id = excel_sheet.row_values(2)[i]
            try:
                if field_type in ['INT32', 'INT64', 'UINT32', 'UINT64', 'INT']:
                    if row_values[i] == '':
                        json_row_dict[field_id] = 0
                    else:
                        json_row_dict[field_id] = int(row_values[i])
                if field_type in ['FLOAT', 'DOUBLE']:
                    if row_values[i] == '':
                        json_row_dict[field_id] = 0.0
                    else:
                        json_row_dict[field_id] = float(row_values[i])
                if field_type in ['STRING', 'CHAR']:
                    json_row_dict[field_id] = str(row_values[i])
                if "L" in field_type and row_values[i] == '':
                    json_row_dict[field_id] = []
                    continue
                if "LI" == field_type:
                    if '|' not in row_values[i]:
                        json_row_dict[field_id] = [int(row_values[i])]
                    else:
                        json_row_dict[field_id] = list(
                            map(int, row_values[i].split('|')))
                if field_type in ["LD", "LF"]:
                    if '|' not in row_values[i]:
                        json_row_dict[field_id] = [float(row_values[i])]
                    else:
                        json_row_dict[field_id] = list(
                            map(float, row_values[i].split('|')))
                if "LS" == field_type:
                    if '|' not in row_values[i]:
                        json_row_dict[field_id] = [str(row_values[i])]
                    else:
                        json_row_dict[field_id] = list(
                            map(str, row_values[i].split('|')))
            except Exception as e:
                print('请修改字段第'+str(i+1)+'列类型')
                traceback.print_exc()
                pass

        return json_row_dict

    def gen_json(self, excel_sheet, table_field, table_name, json_dir):
        nrow = 5
        rowe = excel_sheet.nrows
        if rowe <= nrow:
            return
        json_rows = {}
        while nrow < rowe:
            json_row_dict = self.fix_json_row(excel_sheet, nrow, table_field)
            if json_row_dict and not json_row_dict['id']:
                raise Exception('请设置第一列名称为id')
            json_rows[json_row_dict['id']] = json_row_dict
            nrow = nrow+1

        # 生成json文件
        json_file = os.path.join(json_dir, table_name+'.json')
        with codecs.open(json_file, 'w', "utf-8") as f:
            json_str = json.dumps(json_rows, indent=4,
                                  sort_keys=False, ensure_ascii=False)
            f.write(json_str + '\n')
