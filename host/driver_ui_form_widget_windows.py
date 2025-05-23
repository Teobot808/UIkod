# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'driver_ui_form_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QProgressBar,
    QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1920, 1080)
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(0, 0, 1911, 171))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.timelabel = QLabel(self.frame_2)
        self.timelabel.setObjectName(u"timelabel")
        self.timelabel.setGeometry(QRect(830, 0, 121, 51))
        font = QFont()
        font.setPointSize(22)
        self.timelabel.setFont(font)
        self.time_value = QLabel(self.frame_2)
        self.time_value.setObjectName(u"time_value")
        self.time_value.setGeometry(QRect(760, 40, 211, 111))
        font1 = QFont()
        font1.setPointSize(48)
        self.time_value.setFont(font1)
        self.PWM_bar = QProgressBar(Form)
        self.PWM_bar.setObjectName(u"PWM_bar")
        self.PWM_bar.setGeometry(QRect(0, 970, 1911, 101))
        self.PWM_bar.setFont(font1)
        self.PWM_bar.setStyleSheet(u"QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    background-color: #222;\n"
"    height: 30px;  /* This controls the thickness */\n"
"    text-align: center;\n"
"    color: white;\n"
"}\n"
"\n"
"QProgressBar::chunk {\n"
"    background-color: #05B8CC;\n"
"    width: 20px;\n"
"}\n"
"")
        self.PWM_bar.setValue(24)
        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setGeometry(QRect(0, 170, 471, 801))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.voltagelabel = QLabel(self.frame_3)
        self.voltagelabel.setObjectName(u"voltagelabel")
        self.voltagelabel.setGeometry(QRect(90, 90, 241, 61))
        font2 = QFont()
        font2.setPointSize(24)
        self.voltagelabel.setFont(font2)
        self.voltage_value = QLabel(self.frame_3)
        self.voltage_value.setObjectName(u"voltage_value")
        self.voltage_value.setGeometry(QRect(80, 320, 261, 151))
        self.voltage_value.setFont(font1)
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(470, 170, 971, 791))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.speedlabel = QLabel(self.frame)
        self.speedlabel.setObjectName(u"speedlabel")
        self.speedlabel.setGeometry(QRect(350, 80, 161, 91))
        font3 = QFont()
        font3.setPointSize(26)
        self.speedlabel.setFont(font3)
        self.speed_value = QLabel(self.frame)
        self.speed_value.setObjectName(u"speed_value")
        self.speed_value.setGeometry(QRect(240, 240, 401, 291))
        font4 = QFont()
        font4.setPointSize(72)
        self.speed_value.setFont(font4)
        self.frame_4 = QFrame(Form)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setGeometry(QRect(1440, 170, 471, 791))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.lapslabel = QLabel(self.frame_4)
        self.lapslabel.setObjectName(u"lapslabel")
        self.lapslabel.setGeometry(QRect(170, 90, 131, 51))
        self.lapslabel.setFont(font2)
        self.laps_value = QLabel(self.frame_4)
        self.laps_value.setObjectName(u"laps_value")
        self.laps_value.setGeometry(QRect(50, 320, 381, 141))
        self.laps_value.setFont(font1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.timelabel.setText(QCoreApplication.translate("Form", u"Time", None))
        self.time_value.setText(QCoreApplication.translate("Form", u"Time value", None))
        self.voltagelabel.setText(QCoreApplication.translate("Form", u"Battery Voltage", None))
        self.voltage_value.setText(QCoreApplication.translate("Form", u"both batt voltage", None))
        self.speedlabel.setText(QCoreApplication.translate("Form", u"Speed", None))
        self.speed_value.setText(QCoreApplication.translate("Form", u"speed value", None))
        self.lapslabel.setText(QCoreApplication.translate("Form", u"Laps", None))
        self.laps_value.setText(QCoreApplication.translate("Form", u"Laps value", None))
    # retranslateUi

