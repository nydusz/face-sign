import csv
from datetime import datetime
# 读取文件
# csvf = open("tes.csv",'r')
# rea = csv.reader(csvf)
# a = list(rea)
# for item in a:
#     print(item)
# 写文件
NAME = "scar"
SIGNFLAG = "true"
TIME = datetime.now()
# 写文件
with open('wf.csv', 'w') as f:
    headers = ['name','time','issign']
    wt = csv.DictWriter(f, fieldnames=headers)
    wt.writeheader()
    # itemDic = {'name':NAME,'time':TIME,'issign':SIGNFLAG}
    # wt.writerow(itemDic)
