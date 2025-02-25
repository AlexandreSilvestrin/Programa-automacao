# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tercW.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 255)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: rgb(52, 53, 65);\n"
"}\n"
"\n"
"QStackedWidget {\n"
"    background-color: rgb(52, 53, 65);\n"
"    gridline-color: black;\n"
"    border-style: solid;\n"
"    border-width: 3px;\n"
"    border-radius:12px;\n"
"}\n"
"\n"
"QPushButton[class=\"botoes1\"] {\n"
"    border-radius: 10px;\n"
"    border-width: 2px;\n"
"    background-color: qlineargradient(\n"
"        spread: pad, \n"
"        x1: 0, y1: 1, \n"
"        x2: 0, y2: 0, \n"
"        stop: 0 #648ed1,\n"
"        stop: 0.35 #366096,   /* Azul escuro */\n"
"        stop: 1 #366096  /* Azul claro */\n"
"    );\n"
"}\n"
"\n"
"QPushButton:hover[class=\"botoes1\"] {\n"
"    color: rgb(9, 9, 9);\n"
"    border-radius: 10px;\n"
"    border-width: 2px;\n"
"    border-style: outset;\n"
"    border-color: black;\n"
"    background-color: #8cff57;\n"
"}\n"
"\n"
"QPushButton[class=\"botoes2\"] {\n"
"    background-color: rgb(37, 38, 47);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover[class=\"botoes2\"] {\n"
"    background-color: rgb(82, 84, 103);\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: rgb(92, 94, 115);\n"
"    color: white;\n"
"}\n"
"\n"
"QLabel {\n"
"    border-radius: 15px;\n"
"    border-style: outset;\n"
"    color: rgb(209, 209, 209);\n"
"}\n"
"\n"
"QTextEdit{\n"
"background-color: rgb(74, 76, 93);\n"
"color: white;\n"
"border-radius:12px;\n"
"}\n"
"QLineEdit{\n"
"background-color: rgb(74, 76, 93);\n"
"color: white;\n"
"border-radius:12px;\n"
"}\n"
"\n"
"QComboBox{\n"
"    color: white;\n"
"background-color: rgb(92, 94, 115);\n"
"border-radius:5px;\n"
"}\n"
"\n"
"[class=\"config\"]{\n"
"    background-color: rgb(92, 94, 115);\n"
"     border-width: 2px;\n"
"    border-style: outset;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_pesq = QtWidgets.QPushButton(self.centralwidget)
        self.btn_pesq.setGeometry(QtCore.QRect(630, 200, 161, 41))
        self.btn_pesq.setObjectName("btn_pesq")
        self.btn_salvar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_salvar.setGeometry(QtCore.QRect(460, 200, 161, 41))
        self.btn_salvar.setStyleSheet("")
        self.btn_salvar.setObjectName("btn_salvar")
        self.txt_cnpj = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_cnpj.setGeometry(QtCore.QRect(130, 10, 281, 41))
        self.txt_cnpj.setText("")
        self.txt_cnpj.setObjectName("txt_cnpj")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.label_10.setStyleSheet("")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.txt_contrato = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_contrato.setGeometry(QtCore.QRect(500, 10, 291, 41))
        self.txt_contrato.setText("")
        self.txt_contrato.setObjectName("txt_contrato")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(400, 10, 111, 41))
        self.label_11.setStyleSheet("")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.txt_razao = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_razao.setGeometry(QtCore.QRect(160, 60, 631, 41))
        self.txt_razao.setText("")
        self.txt_razao.setObjectName("txt_razao")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 60, 141, 41))
        self.label_12.setStyleSheet("")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 110, 241, 41))
        self.label_13.setStyleSheet("")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.txt_porcent = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_porcent.setGeometry(QtCore.QRect(260, 110, 531, 41))
        self.txt_porcent.setText("")
        self.txt_porcent.setObjectName("txt_porcent")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 160, 101, 41))
        self.label_14.setStyleSheet("")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.ret_ir = QtWidgets.QCheckBox(self.centralwidget)
        self.ret_ir.setGeometry(QtCore.QRect(120, 160, 51, 41))
        self.ret_ir.setObjectName("ret_ir")
        self.ret_pis = QtWidgets.QCheckBox(self.centralwidget)
        self.ret_pis.setGeometry(QtCore.QRect(180, 160, 51, 41))
        self.ret_pis.setObjectName("ret_pis")
        self.ret_cofins = QtWidgets.QCheckBox(self.centralwidget)
        self.ret_cofins.setGeometry(QtCore.QRect(240, 160, 71, 41))
        self.ret_cofins.setObjectName("ret_cofins")
        self.ret_csll = QtWidgets.QCheckBox(self.centralwidget)
        self.ret_csll.setGeometry(QtCore.QRect(320, 160, 71, 41))
        self.ret_csll.setObjectName("ret_csll")
        self.btn_importar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_importar.setGeometry(QtCore.QRect(10, 200, 101, 41))
        self.btn_importar.setObjectName("btn_importar")
        self.btn_exportar = QtWidgets.QPushButton(self.centralwidget)
        self.btn_exportar.setGeometry(QtCore.QRect(120, 200, 101, 41))
        self.btn_exportar.setObjectName("btn_exportar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Porcentagem Consórcios"))
        self.btn_pesq.setText(_translate("MainWindow", "PESQUISAR"))
        self.btn_pesq.setProperty("class", _translate("MainWindow", "botoes1"))
        self.btn_salvar.setText(_translate("MainWindow", "SALVAR"))
        self.btn_salvar.setProperty("class", _translate("MainWindow", "botoes1"))
        self.label_10.setText(_translate("MainWindow", "CNPJ"))
        self.label_11.setText(_translate("MainWindow", "CONTRATO"))
        self.label_12.setText(_translate("MainWindow", "RAZAO SOCIAL"))
        self.label_13.setText(_translate("MainWindow", "PORCENTAGEM POR CONSORCIADA"))
        self.label_14.setText(_translate("MainWindow", "RETENÇÕES"))
        self.ret_ir.setText(_translate("MainWindow", "IR"))
        self.ret_pis.setText(_translate("MainWindow", "PIS"))
        self.ret_cofins.setText(_translate("MainWindow", "COFINS"))
        self.ret_csll.setText(_translate("MainWindow", "CSLL"))
        self.btn_importar.setText(_translate("MainWindow", "IMPORTAR"))
        self.btn_importar.setProperty("class", _translate("MainWindow", "botoes1"))
        self.btn_exportar.setText(_translate("MainWindow", "EXPORTAR"))
        self.btn_exportar.setProperty("class", _translate("MainWindow", "botoes1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
