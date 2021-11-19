import binascii
import re
from importlib import import_module


def load_object(path):
    dot = path.rindex('.')
    module, name = path[:dot], path[dot + 1:]
    mod = import_module(module)
    obj = getattr(mod, name)
    return obj

def char2hex(data):
        oridata = data
        if data == None or data == '':
            return "''"
        data = bytes(data, encoding='utf-8')
        output = binascii.hexlify(data)
        output = str(output)
        output = re.match(r'^b\'(.*)\'$', output)[1]
        return '0x%s' % output


def generateInsertSql(table,fields,values):
    fieldsSql = ','.join([f"`{i}`" for i in fields])
    valuesSql = ','.join([f"{char2hex(i)}" for i in values])
    sql = f"insert into `{table}` ({fieldsSql}) values ({valuesSql});"
    return sql

def generateCreateSql(table,fields,keys=None,fieldDesc=None):
    fields_ = []
    for f in fields:
        if fieldDesc and f in fieldDesc.keys():
            desc = fieldDesc.get(f)
        else:
            desc = "varchar(255) default '' "
        s = f"`{f}` {desc}"
        fields_.append(s)

    fieldsSql = ','.join(fields_)
    if keys:
        keysSql = ','.join([f"`{i}`" for i in keys])
        keysSql = f',primary key ({keysSql})'
    else:
        keysSql = ''
    sql = f"create table  if not exists `{table}` ({fieldsSql}{keysSql});"
    return sql

if __name__ == '__main__':
    table = 'tb'
    fields = ['a','b','c']
    values = ['1','2','3']

    print(generateCreateSql(table,fields,keys=['a','b'],fieldDesc={'a':'int auto_increment'}))
    print(generateInsertSql(table,fields,values))