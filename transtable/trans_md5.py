'''
@Author: jia.lai
@Date: 2020-05-17 17:12:01
@LastEditTime: 2020-05-18 14:45:38
@Description: 使用md5验证excel是否被修改
@Version: 1.0
'''
#######################################################
import codecs
import os
import json
import hashlib
#######################################################


class TransMd5(object):
    def __init__(self, excel_dir):
        self.file_info = {}
        self.md5_file = "excel_md5"
        self.excel_dir = excel_dir
        self.update_md5 = False
        self.load_md5_file()

    def load_md5_file(self):
        md5_file = os.path.join(self.excel_dir, self.md5_file)
        if not os.path.exists(md5_file):
            return
        with codecs.open(md5_file, "r") as f:
            s = f.read()
            if not s:
                return
            self.file_info = json.loads(s)
        pass

    def update_md5_file(self):
        if self.update_md5:
            md5_file = os.path.join(self.excel_dir, self.md5_file)
            with codecs.open(md5_file, "w") as f:
                json_str = json.dumps(self.file_info, indent=4,
                                      sort_keys=False, ensure_ascii=False)
                f.write(json_str + '\n')
            self.update_md5 = False

    def is_update(self, excel):
        excel_file = os.path.join(self.excel_dir, excel)
        if not os.path.exists(excel_file):
            return False
        md5_str = None
        with codecs.open(excel_file, "rb") as f:
            md5 = hashlib.md5()
            md5.update(f.read())
            md5_str = md5.hexdigest()
        if excel in self.file_info.keys() and str(md5_str) == str(self.file_info[excel]):
            return False
        self.file_info[excel] = md5_str
        self.update_md5 = True
        return True
