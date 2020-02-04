# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sndg.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(958, 867)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setMinimumSize(QSize(800, 800))
        self.graphicsView.setMaximumSize(QSize(800, 800))

        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")

        self.verticalLayout_2.addLayout(self.verticalLayout_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label2 = QLabel(self.centralwidget)
        self.label2.setObjectName(u"label2")
        self.label2.setEnabled(True)
        self.label2.setStyleSheet(u"color: rgba(0, 0, 0, 0.);")

        self.verticalLayout_3.addWidget(self.label2)

        self.label1 = QLabel(self.centralwidget)
        self.label1.setObjectName(u"label1")
        self.label1.setEnabled(True)
        self.label1.setStyleSheet(u"color: rgba(0, 0, 0, 0.);")

        self.verticalLayout_3.addWidget(self.label1)

        self.label0 = QLabel(self.centralwidget)
        self.label0.setObjectName(u"label0")
        self.label0.setStyleSheet(u"color: rgba(0, 0, 0, 0.);")

        self.verticalLayout_3.addWidget(self.label0)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.slider = QSlider(self.centralwidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMaximum(100)
        self.slider.setOrientation(Qt.Vertical)

        self.horizontalLayout_3.addWidget(self.slider)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.sendButton = QPushButton(self.centralwidget)
        self.sendButton.setObjectName(u"sendButton")

        self.verticalLayout_2.addWidget(self.sendButton)

        self.getButton = QPushButton(self.centralwidget)
        self.getButton.setObjectName(u"getButton")

        self.verticalLayout_2.addWidget(self.getButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.estimateBox = QCheckBox(self.centralwidget)
        self.estimateBox.setObjectName(u"estimateBox")

        self.verticalLayout_2.addWidget(self.estimateBox)

        self.estimateButton = QPushButton(self.centralwidget)
        self.estimateButton.setObjectName(u"estimateButton")

        self.verticalLayout_2.addWidget(self.estimateButton)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 958, 25))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"font: 75 11pt \"Ubuntu\";")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Social Navigation Dataset Generator", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Interaction level", None))
        self.label2.setText(QCoreApplication.translate("MainWindow", u"High", None))
        self.label1.setText(QCoreApplication.translate("MainWindow", u"Media", None))
        self.label0.setText(QCoreApplication.translate("MainWindow", u"None", None))
        self.sendButton.setText(QCoreApplication.translate("MainWindow", u"send\n"
"context\n"
"assessment", None))
        self.getButton.setText(QCoreApplication.translate("MainWindow", u"get new\n"
"sample", None))
        self.estimateBox.setText(QCoreApplication.translate("MainWindow", u"automatically\n"
"estimate", None))
        self.estimateButton.setText(QCoreApplication.translate("MainWindow", u"estimate", None))
    # retranslateUi

