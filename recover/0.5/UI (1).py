# coding:utf-8

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


im = None
result = None
AD,NAME='',''

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

        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

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
            QLabel#right_lable{
                border:none;
                font-size:16px;
                font-weight:700;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
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
            qtawesome.icon('fa.film', color='white'), '上传')
        self.left_button_1.setObjectName('left_button')

        self.left_button_2 = QtWidgets.QPushButton(
            qtawesome.icon('fa.video-camera', color='white'), '打开摄像头签到')
        self.left_button_2.setObjectName('left_button')

        self.left_button_rec = QtWidgets.QPushButton(
            qtawesome.icon('fa.play', color='white'), '保存报表')
        self.left_button_rec.setObjectName('left_button')
        self.btn = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'),'存储')


        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_reset, 0, 1, 1, 1)
        #
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.btn, 2, 0, 1, 1)
        #
        self.left_layout.addWidget(self.left_label_2, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 5, 0, 1, 3)
        # self.left_layout.addWidget(self.left_button_3, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_rec, 8, 0, 1, 3)


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

    # def load_url(self):
    #     QtGui.QDesktopServices.openUrl(QtCore.QUrl(
    #         'https://blog.csdn.net/weixin_44936889'))



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
        self.uploadf = 0

    def init_clik(self):

        self.left_button_rec.clicked.connect(self.getText)
        self.left_close.clicked.connect(self.close_all)
        self.btn.clicked.connect(self.test)

    def close_all(self):
        self.close()


    def getText(self):
        global im
        if not im is None:
            img2save = im.copy()
        else:
            img2save = None
        a = QInputDialog()
        a.setOkButtonText('确定')
        text, ok = a.getText(u'添加', '输入姓名')
        # text, ok = QInputDialog.getText(self, u'添加', '输入姓名')
        save_pt = os.path.join(self.base_pt, text)
        if not os.path.join(save_pt):
            os.mkdir(save_pt)
        if img2save is None:
            QMessageBox.about(self, '消息', '{} 添加失败。'.format(text))
        else:
            cv2.imwrite(os.path.join(
                save_pt, '{}.jpg'.format(randint(0, 1000))), img2save)
            QMessageBox.about(self, '消息', '{} 添加成功！'.format(text))
            

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

        self.cap = cv2.VideoCapture(index)  # 调用摄像头（一般电脑自带摄像头index为0）
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if not self.cap.isOpened():
            raise EOFError('未检测到可用摄像头')
        self.timer_camera.start(fps)
        self.timer_camera.timeout.connect(self.openFrame)

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
        path = '../../face_dataset'
        img = cv2.imread(AD)
        cv2.imwrite(path+'/'+NAME,img)
        print("存储成功")

class MonitorWindows(MainUi):

    def __init__(self):
        super().__init__()


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
