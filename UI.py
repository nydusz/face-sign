# coding:utf-8
import csv
import glob
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

import qtawesome
from random import randint
from time import sleep, ctime
import cv2
import os
import numpy as np
from net.mtcnn import mtcnn
import utils.utils as utils
from net.inception import InceptionResNetV1
from face_recognize import face_rec


import pymysql
from datetime import datetime

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


import face_recognize

im = None
result = None
temp = "Unknown"
name = "yym"
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='&d0uisjfCxr!^AjOBk', db='mysql',
                               charset='utf8')
class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)  # 定义一个发送str的信号

    def write(self, text):
        self.textWritten.emit(str(text))


class Initor_for_btn(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

    def init_right(self):

        # 原始视频
        self.raw_video = QtWidgets.QLabel(self)
        self.raw_video.setAlignment(Qt.AlignCenter)
        self.raw_video.setText('欢迎进入签到系统')
        self.raw_video.setFixedSize(
            self.video_size[0], self.video_size[1])  # width height
        # self.raw_video.move(290, 20)
        self.raw_video.setStyleSheet('QLabel{background:white;}'
                                     'QLabel{color:rgb(100,100,100);'
                                     'font-size:15px;'
                                     'font-weight:bold;font-family:宋体;}'
                                     'border-radius: 25px;border: 1px solid black;')


        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.right_bar_layout.addWidget(self.raw_video, 0, 0)

        self.right_label_1 = QtWidgets.QPushButton(temp)
        self.right_label_1.setObjectName('right_label')
        self.right_bar_layout.addWidget(self.right_label_1, 1, 0, 1, 2)
        self.right_label_1.setVisible(False)

        self.right_button_1 = QtWidgets.QPushButton('确定')
        self.right_button_1.setObjectName('right_button')
        self.right_bar_layout.addWidget(self.right_button_1, 2, 0, 1, 3)
        # self.right_button_1.setFixedSize(200, 50)

        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

        #########
        self.right_button_1.clicked.connect(lambda: self.showName())
        #########

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QWidget#right_label{
                border:none;
                font-size:0px;
                font-weight:0;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
            QWidget#right_button{
                text-align:center;
                background:grey;border-radius:5px;
                border:none;
                font-size:16px;
                margin-left:150px;
                margin-right:250px;
                padding:3px;
            }
            QWidget#right_button:hover
            {
                background-color:rgb(44 , 137 , 255);
            }
            
            QWidget#right_button:pressed
            {
                background-color:rgb(14 , 135 , 228);
                padding-left:3px;
                padding-top:3px;
            }

        ''')

    def init_left(self):

        self.left_close = QtWidgets.QPushButton(
            qtawesome.icon('fa.remove', color='white'), '')  # 关闭按钮
        self.left_reset = QtWidgets.QPushButton(
            qtawesome.icon('fa.undo', color='white'), '')  # 刷新
        self.left_mini = QtWidgets.QPushButton(
            qtawesome.icon('fa.minus', color='white'), '')  # 最小化按钮

        self.left_label_1 = QtWidgets.QPushButton('录入')
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton('签到')
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton('报表')
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(
            qtawesome.icon('fa.picture-o', color='white'), '选择图片')
        self.left_button_1.setObjectName('left_button')

        self.btn = QtWidgets.QPushButton(qtawesome.icon('fa.floppy-o', color='white'), '保存图片')
        self.btn.setObjectName('left_button')

        self.left_button_2 = QtWidgets.QPushButton(
            qtawesome.icon('fa.video-camera', color='white'), '开始签到')
        self.left_button_2.setObjectName('left_button')

        self.left_button_3 = QtWidgets.QPushButton(
            qtawesome.icon('fa.sign-in', color='white'), '签到完成')
        self.left_button_3.setObjectName('left_button')

        self.left_button_rec = QtWidgets.QPushButton(
            qtawesome.icon('fa.table', color='white'), '查看签到情况')
        self.left_button_rec.setObjectName('left_button')

        self.left_button_init = QtWidgets.QPushButton(
            qtawesome.icon('fa.address-book', color='white'), '报表初始化')
        self.left_button_init.setObjectName('left_button')

        self.left_button_show = QtWidgets.QPushButton(
            qtawesome.icon('fa.book', color='white'), '显示未签到')
        self.left_button_show.setObjectName('left_button')

        #三个按钮
        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_reset, 0, 1, 1, 1)
        #
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.btn, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 6, 0, 1, 3)


        self.left_layout.addWidget(self.left_label_3, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_init, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_rec, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_show, 10, 0, 1, 3)


        self.left_widget.setStyleSheet('''
                QPushButton{border:none;color:white;}
                QPushButton#left_label{
                    border:none;
                    border-bottom:1px solid white;
                    font-size:18px;
                    font-weight:700;
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                }
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
            ''')

        self.left_close.setFixedSize(32, 32)  # 设置关闭按钮的大小
        self.left_reset.setFixedSize(32, 32)  # 设置按钮大小
        self.left_mini.setFixedSize(32, 32)  # 设置最小化按钮大小

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:2px;}QPushButton:hover{background:red;}''')
        self.left_reset.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:2px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:2px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet(
            '''QWidget#left_widget{
                    background:black;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }'''
        )

    def init_ui(self):
        # self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(
            self.left_widget, 0, 0, 12, 2)
        self.main_layout.addWidget(
            self.right_widget, 0, 2, 12, 10)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件


class Initor_for_event(Initor_for_btn):

    def __init__(self):
        super().__init__()
        self.timer_camera = QTimer()  # 定义定时器

    def init_btn_event(self):

        self.left_mini.clicked.connect(self.showMinimized)


        self.left_button_1.clicked.connect(
            self.load_local_video_file)  # 点击选择文件
        self.left_button_2.clicked.connect(self.load_camera_video)  # 加载摄像头
        self.left_button_init.clicked.connect(self.init_baobiao) #初始化报表
        self.left_button_show.clicked.connect(self.showIsNotSign)
        self.left_button_3.clicked.connect(self.end_sign)
###############
    def showName(self):
        global temp
        self.right_label_1.setText(temp)
        QMessageBox.about(self, '消息', '{} 欢迎'.format(temp))
        csvf = open("wf.csv", 'r')
        rea = csv.reader(csvf)
        a = list(rea)
        for item in a:
            print(item)
        with open('wf.csv', 'w', newline='') as f:
            headers = ['name', 'time', 'issign']
            wt = csv.DictWriter(f, fieldnames=headers)
            # wt.writeheader()
            #NAME = "ssr"
            SIGNFLAG = "true"
            TIME = datetime.now()
            itemDic = {'name': temp, 'time': TIME, 'issign': SIGNFLAG}
            wt.writerow(itemDic)
            for item in a:
                wt.writerow({'name': item[0], 'time': item[1], 'issign': item[2]})

        # 插入


        # 使用cursor()方法获取操作游标
        cursor = conn.cursor()

        # SQL语句：向数据表中插入数据
        NAME = temp
        TI = datetime.now()
        TIME = TI.strftime("%Y-%m-%d %H:%M:%S")  # Out[55]: '2020-09-09 22:42:12'

        ISSIGN = "true"

        insert_sql = ("insert into signtable (name, time, issign) values('%s', '%s', '%s') "
                      % (NAME, TIME, ISSIGN))

        # sql = """INSERT INTO signtable(name, time, issign)
        #          VALUES ( NAME, TIME, ISSIGN)"""
        # VALUES ('赵', '丽颖', 38, '女', 15000)
        # 异常处理
        try:
            # 执行SQL语句
            cursor.execute(insert_sql)
            print("成功")
            # 提交事务到数据库执行
            conn.commit()  # 事务是访问和更新数据库的一个程序执行单元
        except:
            # 如果发生错误则执行回滚操作
            conn.rollback()
            print("失败")
        cursor.close()
        # 关闭数据库连接
        #conn.close()
            # self.video_capture.release()
   # def showData(self):
    #    with open('wf.csv', 'r')



class MainUi(Initor_for_event):

    def __init__(self):
        super().__init__()
        self.base_pt = './faces'
        self.init_ui()
        self.setWindowTitle('人脸识别系统')
        self.timer_detector = QTimer()  # 定义定时器
        self.resize(1200, 910)
        self.video_size = (800, 576)
        self.setFixedSize(self.width(), self.height())
        self.init_layout()
        self.init_clik()

    def init_clik(self):

        self.left_button_rec.clicked.connect(self.getText)
        self.left_close.clicked.connect(self.close_all)
        self.btn.clicked.connect(self.test)

    def close_all(self):
        self.close()

    def getText(self):
        cmd = 'D:/Project/face-recognition/wf.csv'
        os.popen(cmd)
        # try:
        #     f = open('D:/Project/face-recognition/wf.csv', 'r')
        #     print(f.read())
        # finally:
        #     if f:
        #         f.close()

            

    def init_layout(self):

        self.init_left()
        self.init_right()

        self.init_btn_event()
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.main_layout.setSpacing(0)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    def load_camera_video(self, index=0):
        # self.cap = cv2.VideoCapture(0)  # 调用摄像头（一般电脑自带摄像头index为0）
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if not self.cap.isOpened():
           raise EOFError('未检测到可用摄像头')
        dududu = face_rec()
        while True:
            ret, draw = self.cap.read()
            if not self.cap.isOpened():
                raise EOFError('cuowu')
            dududu.recognize(draw)
            #temp = "欢迎"
            self.timer_camera.start(fps)
            self.timer_camera.timeout.connect(self.openFrame)
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    def init_baobiao(self):
        #print("1")

        #游标
        cursor = conn.cursor()
        ###

        file_infos_list = []
        #os.chdir(r"D:\Project\face-recognition\face_dataset")
        #for file_name in glob.glob("*.jpg"):
        #    file_name = file_name.split('.')[0]
       #     file_infos_list.append(file_name)
        #print(file_infos_list)
        os.chdir(r"D:\Project\face-recognition\face_dataset")
        delete_sql = 'DELETE FROM init_table'
        # 异常处理
        try:
            # 执行SQL语句
            cursor.execute(delete_sql)
            # 提交到数据库执行
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()

        for f in glob.glob("*.jpg"):
            file_name = f.split('.')[0]

            ######

            insert_sql = ("insert into init_table (name, time, issign) values('%s', '%s', '%s') "
                          % (file_name, "dd", "false"))
            # sql = """INSERT INTO signtable(name, time, issign)
            #          VALUES ( NAME, TIME, ISSIGN)"""
            # VALUES ('赵', '丽颖', 38, '女', 15000)
            # 异常处理
            try:
                # 执行SQL语句
                cursor.execute(insert_sql)
                print("成功")
                # 提交事务到数据库执行
                conn.commit()  # 事务是访问和更新数据库的一个程序执行单元
            except:
                # 如果发生错误则执行回滚操作
                conn.rollback()
                print("失败")


            ######
            file_infos_list.append(file_name)

        cursor.close()
        # with open('D:/Project/face-recognition/wf.csv', "w", newline='', encoding='utf-8-sig') as csv_file:
        #     headers = ['name']
        #     wt = csv.DictWriter(csv_file, fieldnames=headers)
        #     wt.writeheader()
        #     writer = csv.writer(csv_file)
        #     for row in file_infos_list:
        #         if row != '':
        #             writer.writerow([row])
        QMessageBox.about(self, '消息', '报表初始化成功')

    def test2(self):
        result = QMessageBox.question(self, '提示', '是否将图片进行存储', QMessageBox.Yes | QMessageBox.No,
                                      QMessageBox.No)  # 默认关闭界面选择No

        # fps = face_rec()
        # while True:
        #     ret, draw = self.cap.read()
        #     fps.recognize(draw)
        #     cv2.imshow('Video', draw)
        #     if cv2.waitKey(20) & 0xFF == ord('q'):
        #         break
        # self.timer_camera.start(fps)
        # self.timer_camera.timeout.connect(self.openFrame)


#########################
    def showIsNotSign(self):
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
            lang=""
            curT = datetime.now()
            PcurT = curT.strftime("%Y-%m-%d %H:%M:%S              ")
            # lang+=str(curT) +"\n"
            idxx=1
            for row in results:
                # 打印列表元素
                lang += str(idxx) + ": " + row[0] + "没签到" + "\n"
                idxx+=1
            #for i in lang:

            QMessageBox.about(self, PcurT, lang)
            QMessageBox.resize(self, 1800, 1800)
        except:
            print('Uable to fetch data!')
#########################
    def end_sign(self):
        self.cap.release()
        self.raw_video.setText('欢迎进入签到系统')
#########################


    def load_local_video_file(self):
        global AD,NAME
        videoName, _ = QFileDialog.getOpenFileName(
            self, 'Open','', '*.jpg;;All Files(*)')
        AD = videoName
        temp=videoName.split('/')
        NAME=temp[len(temp) - 1]
        print(AD,NAME)
        if videoName != '':  # 为用户取消
            self.cap = cv2.VideoCapture(videoName)
            fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.timer_camera.start(fps)
            self.timer_camera.timeout.connect(self.openFrame)
            self.uploadf = 1
        else:
            self.uploadf = 0
        print(self.uploadf)

    def test(self):
        if(self.uploadf==1):
            result = QMessageBox.question(self, '提示', '是否将图片进行存储', QMessageBox.Yes | QMessageBox.No,
                                                  QMessageBox.No)  # 默认关闭界面选择No
            if result == QMessageBox.Yes:
                self.picupload()
                print('OK')
                self.uploadf = 0
            else:
                print('No')



    def openFrame(self):
        global im
        if self.cap.isOpened():
            ret, im = self.cap.read()
            if ret:
                frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                height, width, bytesPerComponent = frame.shape
                bytesPerLine = bytesPerComponent * width
                q_image = QImage(frame.data,  width, height, bytesPerLine,
                                 QImage.Format_RGB888).scaled(self.raw_video.width(), self.raw_video.height())
                self.raw_video.setPixmap(QPixmap.fromImage(q_image))

            else:
                im = None
                self.cap.release()
                self.timer_camera.stop()   # 停止计时器

    def picupload(self):
        path = './face_dataset'
        img = cv2.imread(AD)
        cv2.imwrite(path+'/'+NAME,img)
        print("存储成功")


class MonitorWindows(MainUi):

    def __init__(self):
        super().__init__()

class face_rec():
    def __init__(self):
        # 创建mtcnn对象
        # 检测图片中的人脸`
        self.mtcnn_model = mtcnn()
        # 门限函数
        self.threshold = [0.5, 0.8, 0.9]
        # 载入facenet
        # 将检测到的人脸转化为128维的向量
        self.facenet_model = InceptionResNetV1()
        # model.summary()
        model_path = './model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)
        # -----------------------------------------------#
        #   对数据库中的人脸进行编码
        #   known_face_encodings中存储的是编码后的人脸
        #   known_face_names为人脸的名字
        # -----------------------------------------------#
        face_list = os.listdir("face_dataset")
        self.known_face_encodings = []
        self.known_face_names = []
        for face in face_list:
            name = face.split(".")[0]
            data_path = os.path.join("./face_dataset/" , face)
            img = cv2.imread(data_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 检测人脸
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)
            # 转化成正方形
            rectangles = utils.rect2square(np.array(rectangles))
            # facenet要传入一个160x160的图片
            rectangle = rectangles[0]
            # 记下他pip install keras==2.0.9们的landmark
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
                    rectangle[3] - rectangle[1]) * 160
            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))
            new_img, _ = utils.Alignment_1(crop_img, landmark)
            new_img = np.expand_dims(new_img, 0)
            # 将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)
    def recognize(self, draw):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)
        # 检测人脸
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)
        if len(rectangles) == 0:
            return
        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, 0] = np.clip(rectangles[:, 0], 0, width)
        rectangles[:, 1] = np.clip(rectangles[:, 1], 0, height)
        rectangles[:, 2] = np.clip(rectangles[:, 2], 0, width)
        rectangles[:, 3] = np.clip(rectangles[:, 3], 0, height)
        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
                    rectangle[3] - rectangle[1]) * 160
            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))
            new_img, _ = utils.Alignment_1(crop_img, landmark)
            new_img = np.expand_dims(new_img, 0)
            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            face_encodings.append(face_encoding)
        face_names = []
        for face_encoding in face_encodings:
            # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
            matches = utils.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.9)
            name = "Unknown"
            # 找出距离最近的人脸
            face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
            # 取出这个最近人脸的评分
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)
            global temp  #全局temp = name 去286行test2
            temp = name
            if name != "Unknown":
                print('------------------------------')
                print('识别成功！欢迎'+name+'！')
                print('------------------------------')

            else:
                print('------------------------------')
                print('抱歉无法验证您的身份！')
                print('------------------------------')
        rectangles = rectangles[:, 0:4]
        # -----------------------------------------------#
        #   画框~!~
        # -----------------------------------------------#
        for (left, top, right, bottom), name in zip(rectangles, face_names):
            cv2.rectangle(draw, (left, top), (right, bottom), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(draw, name, (left, bottom - 15), font, 0.75, (255, 255, 255), 2)
        return draw


if __name__ == '__main__':

    try:
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        App = QApplication(sys.argv)
        monitor_box = MonitorWindows()
        monitor_box.show()
        sys.exit(App.exec_())
    except Exception as e:
        print(e)

    input('输入任意键退出')



