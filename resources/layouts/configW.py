# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources\layouts\configW.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(213, 187)
        Dialog.setStyleSheet("")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setEnabled(True)
        self.widget.setGeometry(QtCore.QRect(0, 0, 211, 181))
        self.widget.setObjectName("widget")
        self.btnfonteP = QtWidgets.QPushButton(self.widget)
        self.btnfonteP.setGeometry(QtCore.QRect(160, 60, 41, 41))
        self.btnfonteP.setStyleSheet("QPushButton{\n"
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
"font-size: 20px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 21px;\n"
"}")
        self.btnfonteP.setObjectName("btnfonteP")
        self.btnfonteM = QtWidgets.QPushButton(self.widget)
        self.btnfonteM.setGeometry(QtCore.QRect(110, 60, 41, 41))
        self.btnfonteM.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btnfonteM.setObjectName("btnfonteM")
        self.btnclaro = QtWidgets.QPushButton(self.widget)
        self.btnclaro.setGeometry(QtCore.QRect(110, 10, 91, 41))
        self.btnclaro.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btnclaro.setObjectName("btnclaro")
        self.btnescuro = QtWidgets.QPushButton(self.widget)
        self.btnescuro.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.btnescuro.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btnescuro.setObjectName("btnescuro")
        self.btn50 = QtWidgets.QPushButton(self.widget)
        self.btn50.setGeometry(QtCore.QRect(10, 130, 41, 41))
        self.btn50.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btn50.setObjectName("btn50")
        self.btn85 = QtWidgets.QPushButton(self.widget)
        self.btn85.setGeometry(QtCore.QRect(110, 130, 41, 41))
        self.btn85.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btn85.setObjectName("btn85")
        self.btn100 = QtWidgets.QPushButton(self.widget)
        self.btn100.setGeometry(QtCore.QRect(160, 130, 41, 41))
        self.btn100.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btn100.setObjectName("btn100")
        self.btn70 = QtWidgets.QPushButton(self.widget)
        self.btn70.setGeometry(QtCore.QRect(60, 130, 41, 41))
        self.btn70.setStyleSheet("QPushButton{\n"
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
"font-size: 15px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border-radius: 10px;\n"
"border-width:2px;\n"
"border-style:outset;\n"
"border-color:black;\n"
"background-color: #8cff57;\n"
"font-size: 15px;\n"
"}")
        self.btn70.setObjectName("btn70")
        self.label_14 = QtWidgets.QLabel(self.widget)
        self.label_14.setGeometry(QtCore.QRect(0, 100, 211, 31))
        self.label_14.setStyleSheet("QLabel{\n"
"font-size: 20px;\n"
"}\n"
"\n"
"")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_fonte = QtWidgets.QLabel(self.widget)
        self.label_fonte.setGeometry(QtCore.QRect(40, 60, 31, 41))
        self.label_fonte.setStyleSheet("QLabel{\n"
"font-size: 20px;\n"
"}\n"
"\n"
"")
        self.label_fonte.setAlignment(QtCore.Qt.AlignCenter)
        self.label_fonte.setObjectName("label_fonte")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.widget.setProperty("class", _translate("Dialog", "config"))
        self.btnfonteP.setText(_translate("Dialog", "+"))
        self.btnfonteP.setProperty("class", _translate("Dialog", "botoes1"))
        self.btnfonteM.setText(_translate("Dialog", "-"))
        self.btnfonteM.setProperty("class", _translate("Dialog", "botoes1"))
        self.btnclaro.setText(_translate("Dialog", "CLARO"))
        self.btnclaro.setProperty("class", _translate("Dialog", "botoes1"))
        self.btnescuro.setText(_translate("Dialog", "ESCURO"))
        self.btnescuro.setProperty("class", _translate("Dialog", "botoes1"))
        self.btn50.setText(_translate("Dialog", "50"))
        self.btn50.setProperty("class", _translate("Dialog", "botoes1"))
        self.btn85.setText(_translate("Dialog", "85"))
        self.btn85.setProperty("class", _translate("Dialog", "botoes1"))
        self.btn100.setText(_translate("Dialog", "100"))
        self.btn100.setProperty("class", _translate("Dialog", "botoes1"))
        self.btn70.setText(_translate("Dialog", "70"))
        self.btn70.setProperty("class", _translate("Dialog", "botoes1"))
        self.label_14.setText(_translate("Dialog", "TAMANHO"))
        self.label_fonte.setText(_translate("Dialog", "0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())