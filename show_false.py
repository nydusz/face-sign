# -*-coding:utf-8-*-


import pymysql
from datetime import datetime

# 打开数据库连接
# conn = pymysql.connect('localhost', 'root', 'root', 'test_db')
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='&d0uisjfCxr!^AjOBk', db='mysql', charset='utf8')

# 使用cursor()方法获取操作游标
cursor = conn.cursor()

# SQL语句：向数据表中插入数据
sql = "select distinct init_table.name from init_table where init_table.name not in (select name from signtable)"

# 异常处理
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有的记录列表
    results = cursor.fetchall()
    # 遍历列表
    for row in results:
        # 打印列表元素
        print(row[0]+"没签到")

except:
    print('Uable to fetch data!')

# 关闭数据库连接
conn.close()