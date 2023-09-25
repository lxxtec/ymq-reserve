
# -*- encoding: utf-8 -*-
'''
@File    : app.py
@Time    : 2022/11/29 09:32:18
@Author  : lxxtec
@Contact : 631859877@qq.com
@Version : 0.1
@Desc    : HEU 体育馆场地预定dev v1.2.0
'''

from threading import Timer
import sys
import datetime
from multiprocessing import Pool, current_process
from os.path import abspath, join

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDate, QThread, QTimer, QTime
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
# from QCandyUi.CandyWindow import colorful
from qt_material import apply_stylesheet

from encrypt import Encryption
from mailserver import MailServe
from reserve import ReserveSystem
from Ui_mainui import Ui_Form


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS  # 系统临时目录
    else:
        base_path = abspath(".")
    return join(base_path, relative_path)


# @colorful('deepblue')
class QmyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        jpgName = resource_path(join("figs", "ymqq.png"))
        jpg = QPixmap(jpgName).scaled(self.width(), self.height())
        self.ui.lbFig0.setPixmap(jpg)

        jpgName = resource_path(join("figs", "bandi.png"))
        jpg = QPixmap(jpgName).scaled(self.width(), self.height())
        self.ui.lbFig1.setPixmap(jpg)

        # jpgName = resource_path(join("figs", "tanhao3.png"))
        # jpg = QPixmap(jpgName).scaled(self.width(), self.height())
        # self.ui.lbFigAlert.setPixmap(jpg)

        self.ui.stackedWidget.setCurrentIndex(2)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.on_timer_timeout)

        self.rer = ReserveSystem()

        self.enc = Encryption('ymq001')

        self.mailser = MailServe()

        self.count = 0
        # HEU羽毛球场馆预定 alpha0.1.1(lxxtec)
        self.setWindowTitle(
            "HEU羽毛球场馆预定 V1.2.1(lxxtec) expired date:{}".format(self.enc.lastDate))

        now = datetime.datetime.now()
        self.ui.dateEdit.setMinimumDate(QDate(now.year, now.month, now.day))
        self.ui.timeEdit.setTime(QTime(20, 59, 59))

    def select_field(self) -> list:
        selected = []
        if self.ui.cb1.isChecked():
            selected.append(1)
        if self.ui.cb2.isChecked():
            selected.append(2)
        if self.ui.cb3.isChecked():
            selected.append(3)
        if self.ui.cb4.isChecked():
            selected.append(4)
        if self.ui.cb5.isChecked():
            selected.append(5)
        if self.ui.cb6.isChecked():
            selected.append(6)
        if self.ui.cb7.isChecked():
            selected.append(7)
        if self.ui.cb8.isChecked():
            selected.append(8)
        if self.ui.cb9.isChecked():
            selected.append(9)
        if self.ui.cb10.isChecked():
            selected.append(10)
        if self.ui.cb11.isChecked():
            selected.append(11)
        if self.ui.cb12.isChecked():
            selected.append(12)
        if self.ui.cb13.isChecked():
            selected.append(13)
        if self.ui.cb14.isChecked():
            selected.append(14)
        if self.ui.cb15.isChecked():
            selected.append(15)
        if self.ui.cb16.isChecked():
            selected.append(16)
        if self.ui.cb17.isChecked():
            selected.append(17)
        if self.ui.cb18.isChecked():
            selected.append(18)
        if self.ui.cb19.isChecked():
            selected.append(19)
        if self.ui.cb20.isChecked():
            selected.append(20)
        return selected

    def select_time(self) -> list:
        res = []
        if self.ui.cbtime1.currentIndex() != 0:
            res.append(self.ui.cbtime1.currentIndex()+7)
        if self.ui.cbtime2.currentIndex() != 0:
            res.append(self.ui.cbtime2.currentIndex()+7)
        if len(res) == 2 and res[0] == res[1]:
            QMessageBox.warning(self, "警告", "两个时间段不能相同")
            return []
        return res

    def on_btStart_pressed(self):
        print("start task!!!")
        self.run_flag = False
        sel = self.select_field()
        if not sel:  # 用户没有选择场地
            QMessageBox.warning(self, "警告", "请选择场地")
            return
        tims = self.select_time()
        if not tims:
            QMessageBox.warning(self, "警告", "请选择合适的时间")
            return
        # 计算日期查
        seldate = self.ui.dateEdit.date()
        dateadd = QDate.currentDate().daysTo(seldate)
        print(dateadd)

        if not self.ui.textEdit.toPlainText():  # 用户没有输入cookie
            if not self.rer.cookie_flag:  # 也没有本地cookie
                QMessageBox.warning(self, "警告", "当前没有可用的cookie")
                return
        else:
            self.rer.generate_cookie(self.ui.textEdit.toPlainText())
        print("cookie: ", self.rer.cookie_flag)
        print(self.rer.cookie)
        # print(self.rer.cookie)
        self.timer.start()
        self.ui.btStart.setEnabled(False)
        self.rer.generate_urls(sel, tims, dateadd)
        if self.ui.cbTimeCheck.isChecked():
            self.ui.textBroswer.append(
                f"【已设置定时开抢】{self.ui.timeEdit.time().toString()}")

            now_t = datetime.datetime.now()
            # 解析日期，时间
            y, m, d = now_t.date().year, now_t.date().month, now_t.date().day

            next_t = datetime.datetime.strptime(
                f"{y}-{m}-{d} {self.ui.timeEdit.time().toString()}", "%Y-%m-%d %H:%M:%S")
            # print(next_t)
            # 计算总秒数
            delay_time = (next_t-now_t).total_seconds()
            print(delay_time)
            tim = Timer(delay_time, self.start_task)
            tim.start()
            return

        tim = Timer(0.1, self.start_task)
        tim.start()
        self.ui.textBroswer.append("正在尝试预定....")

        # self.rer.try_reserve()

    def start_task(self):
        self.run_flag = True
        if not self.timer.isActive():
            return
        self.rer.try_reserve()
        # self.rer.try_reserve_async()
        tim = Timer(2, self.start_task)
        tim.start()

    def on_timer_timeout(self):
        if self.run_flag == False:
            return

        if not self.rer.info.empty():
            res = self.rer.info.get()
            self.count += 1
            date = QDate.currentDate().addDays(res[2]).toString()
            msg = ">> 已预定:{}点 {}场 {}, 请前往HEU移动校园app进行查看付款 <<".format(
                res[1], res[0], date)

            self.ui.textBroswer.append(msg)
            email = self.ui.leMail.text()
            if email:  # 用户输入了邮箱
                self.mailser.send_mail(msg, "[HEU场地预定] 结果", email)
        else:
            self.ui.textBroswer.append(
                "已预定数量【{}】正在尝试预定....".format(self.count))
            # self.rer.try_reserve()

    def on_btQuit_pressed(self):
        print("cancel task!!!")
        if not self.timer.isActive():
            return
        button = QMessageBox.warning(self, "提示", "结束预定任务？",
                                     QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            print("cancel")
            self.timer.stop()
            self.ui.textBroswer.append("任务已取消！")
            self.ui.btStart.setEnabled(True)
        elif button == QMessageBox.No:
            print("continue")

    def on_btLogin_pressed(self):
        print('login')
        if self.enc.working:
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "警告", "已过期,请找管理员重新注册")

    def on_btAct_pressed(self):
        print('activate')
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.leMachinecode.setText(self.enc.localCode)

    def on_btBack_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_btActivate_pressed(self):
        print("activate code")
        codes = self.ui.teActivatecode.toPlainText()
        if self.enc.decrypt(codes):
            QMessageBox.about(self, "提示", "激活成功")
            self.setWindowTitle(
                "HEU羽毛球场馆预定 alpha0.1.1(lxxtec)  expired date:{}".format(self.enc.lastDate))

        else:
            QMessageBox.about(self, "提示", "激活失败！")

    def on_commandLinkButton_pressed(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def on_dial_valueChanged(self):
        QMessageBox.about(
            self, '提示', "免责声明：本软件仅适用于学习交流使用，请注意账户安全，因使用本软件造成的损失本软件概不负责，亦不承担任何法律责任")

    def on_cball_stateChanged(self):
        if self.ui.cball.isChecked():
            self.ui.cb1.setChecked(True)
            self.ui.cb2.setChecked(True)
            self.ui.cb3.setChecked(True)
            self.ui.cb4.setChecked(True)
            self.ui.cb5.setChecked(True)
            self.ui.cb6.setChecked(True)
            self.ui.cb7.setChecked(True)
            self.ui.cb8.setChecked(True)
            self.ui.cb9.setChecked(True)
            self.ui.cb10.setChecked(True)
            self.ui.cb11.setChecked(True)
            self.ui.cb12.setChecked(True)
            self.ui.cb13.setChecked(True)
            self.ui.cb14.setChecked(True)
            self.ui.cb15.setChecked(True)
            self.ui.cb16.setChecked(True)
            self.ui.cb17.setChecked(True)
            self.ui.cb18.setChecked(True)
            self.ui.cb19.setChecked(True)
            self.ui.cb20.setChecked(True)
        else:
            self.ui.cb1.setChecked(False)
            self.ui.cb2.setChecked(False)
            self.ui.cb3.setChecked(False)
            self.ui.cb4.setChecked(False)
            self.ui.cb5.setChecked(False)
            self.ui.cb6.setChecked(False)
            self.ui.cb7.setChecked(False)
            self.ui.cb8.setChecked(False)
            self.ui.cb9.setChecked(False)
            self.ui.cb10.setChecked(False)
            self.ui.cb11.setChecked(False)
            self.ui.cb12.setChecked(False)
            self.ui.cb13.setChecked(False)
            self.ui.cb14.setChecked(False)
            self.ui.cb15.setChecked(False)
            self.ui.cb16.setChecked(False)
            self.ui.cb17.setChecked(False)
            self.ui.cb18.setChecked(False)
            self.ui.cb19.setChecked(False)
            self.ui.cb20.setChecked(False)


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    myWidget = QmyWidget()
    myWidget.show()
    myWidget.setFixedSize(myWidget.width(), myWidget.height())
    extra = {

        # Font
        'font_family': 'SimHei',
        'font_size': '12px',
        'line_height': '12px',

        # Density Scale
        'density_scale': '0',

        # environ
        # 'pyside6': True,
        # 'linux': True,

    }
    apply_stylesheet(app, theme='dark_purple.xml',
                     invert_secondary=False, extra=extra)
    app.exec()
