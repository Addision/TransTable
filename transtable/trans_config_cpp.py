'''
@Author: jia.lai
@Date: 2020-05-18 09:52:27
@LastEditTime: 2020-05-18 14:04:01
@Description: 
@Version: 1.0
'''
'''
@Author: jia.lai
@Date: 2020-05-18 09:52:27
@LastEditTime: 2020-05-18 11:20:09
@Description: 转换配置类表
@Version: 1.0
'''

#######################################################
import sys
import os
import codecs
from trans import *
table_field = 'static constexpr %(field_type)s %(field_name)s = %(field_value)s;'
#######################################################


class TransConfigCpp(TransConfig):
    def __init__(self):
        super(TransConfigCpp, self).__init__(
            table_field, 'table_config_cpp.tmpl')
        pass
