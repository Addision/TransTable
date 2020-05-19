1、表第一列名称为id，代表表主键，默认
2、填表的数据类型有以下几种:
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

左边为表配置类型，右边为c++对照数据类型    
L开头数据类型配置按照1|2|3填写

3、表第二行默认可以不填写，1 代表生成cpp、json代码会被过滤掉<服务器不会使用>,2 代表生成c#、json代码会被过滤掉<客户端不会使用>
4、直接执行bat脚本 , 生成c++代码 参数第一个cpp 生成csharp代码第一个参数为cs
5、表配置名称如果包含Enum则生成枚举类型的代码，策划一般不需要配置这样的表
6、data 写excel_md5 是保存excel文件md5的值，倒完表需要上传一下

