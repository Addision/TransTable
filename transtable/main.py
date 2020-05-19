'''
@Author: jia.lai
@Date: 2020-05-16 20:40:44
@LastEditTime: 2020-05-19 09:58:05
@Description: 导表工具
@Version: 1.0
'''
import os
import sys
from sys import argv
from read_excel import *
from trans_json import *
from trans_cpp import *
from trans_cs import *
from trans_md5 import *
from trans_config_cpp import *
from trans_config_cs import *
import traceback

count = 3
while count:
    try:
        import xlrd
        import hashlib
        from xlrd import xldate_as_tuple
        break
    except Exception as e:
        os.system('pip install xlrd')
        os.system('pip install hashlib')
        count -= 1
        continue


if __name__ == '__main__':
    print('导表开始.....')
    if len(argv) != 5:
        print('请正确设置导出路径')
        os.system('pause')

    output = argv[1]  # cpp 导出c++使用配置 cs 导出c#使用配置
    excel_dir = argv[2]
    json_dir = argv[3]
    code_dir = argv[4]

    # output = 'cs'
    # excel_dir = '../data/'
    # json_dir = '../data/'
    # code_dir = '../data/'
    try:
        trans_md5 = TransMd5(excel_dir)
        read_excel = ReadExcel(excel_dir)
        excel_list, table_names = read_excel.get_excel()
        for excel in excel_list:
            table_name = excel.split('_')[0]
            # 添加md5验证
            if not trans_md5.is_update(excel):
                continue
            else:
                trans_md5.update_md5_file()
            print('开始读表:'+table_name)
            ret, excel_sheet, field_desc, data_desc, table_field = read_excel.read_excel(
                excel, output)
            if not ret:
                print('ERROR: 读表错误:'+table_name)
                continue

            trans_json = TransJson()
            trans_json.gen_json(excel_sheet, table_field, table_name, json_dir)
            if output == 'cpp':
                trans_cpp = TransCpp()
                trans_cpp.gen_cpp(excel_sheet, table_name,
                                  data_desc, field_desc, code_dir)
                trans_conf = TransConfigCpp()
                trans_conf.gen_config(
                    excel_sheet, table_name, output, code_dir)
            if output == 'cs':
                trans_cs = TransCs()
                trans_cs.gen_cs(table_name, data_desc, field_desc, code_dir)
                trans_conf = TransConfigCs()
                trans_conf.gen_config(
                    table_name, data_desc, field_desc, code_dir)
            print('完成导表:'+table_name)
    except Exception as e:
        print('导表错误')
        traceback.print_exc()

    print('导表结束.....')
    os.system("pause")
    pass
