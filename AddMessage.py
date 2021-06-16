# # -*-coding:utf-8-*-
#
#
# import pymysql
# from datetime import datetime
#
# # 打开数据库连接
# # conn = pymysql.connect('localhost', 'root', 'root', 'test_db')
# conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='&d0uisjfCxr!^AjOBk', db='mysql', charset='utf8')
#
# # 使用cursor()方法获取操作游标
# cursor = conn.cursor()
#
# # SQL语句：向数据表中插入数据
# NAME = "dd"
# TI = datetime.now()
# TIME = TI.strftime("%Y-%m-%d %H:%M:%S") #Out[55]: '2020-09-09 22:42:12'
#
# ISSIGN = "true"
#
# insert_sql = ("insert into signtable (name, time, issign) values('%s', '%s', '%s') "
#               % (NAME, TIME, ISSIGN))
#
# # sql = """INSERT INTO signtable(name, time, issign)
# #          VALUES ( NAME, TIME, ISSIGN)"""
# # VALUES ('赵', '丽颖', 38, '女', 15000)
# # 异常处理
# try:
#     # 执行SQL语句
#     cursor.execute(insert_sql)
#     print("成功")
#     # 提交事务到数据库执行
#     conn.commit()  # 事务是访问和更新数据库的一个程序执行单元
# except:
#     # 如果发生错误则执行回滚操作
#     conn.rollback()
#     print("失败")
#
# # 关闭数据库连接
# conn.close()