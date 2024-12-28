# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\layouts\secW.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1078, 614)
        MainWindow.setStyleSheet("QPushButton[class=\"botoes1\"]{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"background-color: qlineargradient(\n"
"        spread:pad, \n"
"        x1:0, y1:1, \n"
"        x2:0, y2:0, \n"
"        stop:0 #648ed1,\n"
"        stop:0.35 #366096,   /* Azul escuro (rgb(7, 0, 235)) */\n"
"        stop:1 #366096  /* Azul claro (rgb(0, 255, 255)) */\n"
"    );\n"
"}\n"
"\n"
"QPushButton:hover[class=\"botoes1\"]{\n"
"color: rgb(9, 9, 9);\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"}\n"
"\n"
"")
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 771, 611))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tableWidget.setStyleSheet("")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setDefaultSectionSize(45)
        self.tableWidget.verticalHeader().setMinimumSectionSize(35)
        self.btn_salvar_banco = QtWidgets.QPushButton(self.widget)
        self.btn_salvar_banco.setEnabled(True)
        self.btn_salvar_banco.setGeometry(QtCore.QRect(780, 550, 291, 51))
        self.btn_salvar_banco.setStyleSheet("")
        self.btn_salvar_banco.setObjectName("btn_salvar_banco")
        self.btnPesqAPI = QtWidgets.QPushButton(self.widget)
        self.btnPesqAPI.setGeometry(QtCore.QRect(780, 70, 291, 51))
        self.btnPesqAPI.setStyleSheet("")
        self.btnPesqAPI.setObjectName("btnPesqAPI")
        self.labelP = QtWidgets.QLabel(self.widget)
        self.labelP.setGeometry(QtCore.QRect(780, 160, 291, 31))
        self.labelP.setStyleSheet("")
        self.labelP.setText("")
        self.labelP.setObjectName("labelP")
        self.labelP_2 = QtWidgets.QLabel(self.widget)
        self.labelP_2.setGeometry(QtCore.QRect(780, 190, 291, 31))
        self.labelP_2.setStyleSheet("")
        self.labelP_2.setText("")
        self.labelP_2.setObjectName("labelP_2")
        self.labelP_3 = QtWidgets.QLabel(self.widget)
        self.labelP_3.setGeometry(QtCore.QRect(780, 130, 291, 21))
        self.labelP_3.setStyleSheet("")
        self.labelP_3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelP_3.setObjectName("labelP_3")
        self.btnPARAR = QtWidgets.QPushButton(self.widget)
        self.btnPARAR.setGeometry(QtCore.QRect(780, 10, 291, 51))
        self.btnPARAR.setStyleSheet("")
        self.btnPARAR.setObjectName("btnPARAR")
        MainWindow.setCentralWidget(self.widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BUSCAR_CNPJS"))
        self.btn_salvar_banco.setText(_translate("MainWindow", "ATUALIZAR BANCO"))
        self.btn_salvar_banco.setProperty("class", _translate("MainWindow", "botoes1"))
        self.btnPesqAPI.setText(_translate("MainWindow", "PESQUISAR(API)"))
        self.btnPesqAPI.setProperty("class", _translate("MainWindow", "botoes1"))
        self.labelP_3.setText(_translate("MainWindow", "ATUALIZAÇÃO A CADA 60 SEGUNDOS"))
        self.btnPARAR.setText(_translate("MainWindow", "FINALIZAR/INTERROMPER"))
        self.btnPARAR.setProperty("class", _translate("MainWindow", "botoes1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
