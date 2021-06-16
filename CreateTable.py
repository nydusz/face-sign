# -*-coding:utf-8-*-
"""
@author:taoshouzheng
@time:2018/7/18 9:24
@email:tsz1216@sina.com
"""

import pymysql

# 打开数据库连接
# conn = pymysql.connect('localhost', 'root', 'root', 'test_db')
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='&d0uisjfCxr!^AjOBk', db='mysql', charset='utf8')
# 使用cursor()方法创建一个游标对象cursor
cursor = conn.cursor()  # 游标对象用于执行查询和获取结果

# 使用execute()方法执行SQL，如果表存在则将其删除
cursor.execute('DROP TABLE IF EXISTS SIGNTABLE')


# 使用预处理语句创建表
sql = """CREATE TABLE `signtable` (
  `name` varchar(255) DEFAULT NULL COMMENT '姓名',
  `time` varchar(255) DEFAULT NULL COMMENT '时间',
  `issign` varchar(255) DEFAULT FALSE COMMENT '是否签到'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

# 执行SQL语句
cursor.execute(sql)

# 关闭数据库连接
conn.close()
