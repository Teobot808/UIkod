# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'host/driver_ui_form_widget.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1920, 1080)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(0, 0, 1911, 171))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.timelabel = QtWidgets.QLabel(self.frame_2)
        self.timelabel.setGeometry(QtCore.QRect(830, 0, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        self.timelabel.setFont(font)
        self.timelabel.setObjectName("timelabel")
        self.time_value = QtWidgets.QLabel(self.frame_2)
        self.time_value.setGeometry(QtCore.QRect(760, 40, 211, 111))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.time_value.setFont(font)
        self.time_value.setObjectName("time_value")
        self.PWM_bar = QtWidgets.QProgressBar(Form)
        self.PWM_bar.setGeometry(QtCore.QRect(0, 970, 1911, 101))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.PWM_bar.setFont(font)
        self.PWM_bar.setStyleSheet("QProgressBar {\n"
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
        self.PWM_bar.setProperty("value", 24)
        self.PWM_bar.setObjectName("PWM_bar")
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(0, 170, 471, 801))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.voltagelabel = QtWidgets.QLabel(self.frame_3)
        self.voltagelabel.setGeometry(QtCore.QRect(90, 90, 241, 61))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.voltagelabel.setFont(font)
        self.voltagelabel.setObjectName("voltagelabel")
        self.voltage_value = QtWidgets.QLabel(self.frame_3)
        self.voltage_value.setGeometry(QtCore.QRect(80, 320, 261, 151))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.voltage_value.setFont(font)
        self.voltage_value.setObjectName("voltage_value")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(470, 170, 971, 791))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.speedlabel = QtWidgets.QLabel(self.frame)
        self.speedlabel.setGeometry(QtCore.QRect(350, 80, 161, 91))
        font = QtGui.QFont()
        font.setPointSize(26)
        self.speedlabel.setFont(font)
        self.speedlabel.setObjectName("speedlabel")
        self.speed_value = QtWidgets.QLabel(self.frame)
        self.speed_value.setGeometry(QtCore.QRect(240, 240, 401, 291))
        font = QtGui.QFont()
        font.setPointSize(72)
        self.speed_value.setFont(font)
        self.speed_value.setObjectName("speed_value")
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setGeometry(QtCore.QRect(1440, 170, 471, 791))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.lapslabel = QtWidgets.QLabel(self.frame_4)
        self.lapslabel.setGeometry(QtCore.QRect(170, 90, 131, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.lapslabel.setFont(font)
        self.lapslabel.setObjectName("lapslabel")
        self.laps_value = QtWidgets.QLabel(self.frame_4)
        self.laps_value.setGeometry(QtCore.QRect(50, 320, 381, 141))
        font = QtGui.QFont()
        font.setPointSize(48)
        self.laps_value.setFont(font)
        self.laps_value.setObjectName("laps_value")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.timelabel.setText(_translate("Form", "Time"))
        self.time_value.setText(_translate("Form", "Time value"))
        self.voltagelabel.setText(_translate("Form", "Battery Voltage"))
        self.voltage_value.setText(_translate("Form", "both batt voltage"))
        self.speedlabel.setText(_translate("Form", "Speed"))
        self.speed_value.setText(_translate("Form", "speed value"))
        self.lapslabel.setText(_translate("Form", "Laps"))
        self.laps_value.setText(_translate("Form", "Laps value"))
