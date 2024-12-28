from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from resources.config.caminhos import Caminhos
from resources.layouts.configW import Ui_Dialog

class Configuracoes(QDialog, Ui_Dialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.setWindowTitle("Configurações")
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.btnescuro.clicked.connect(lambda: self.parent.apply_stylesheet('escuro'))
        self.btnclaro.clicked.connect(lambda: self.parent.apply_stylesheet('claro'))
        self.btn85.clicked.connect(lambda: (self.parent.load_and_resize_widget_geometry(scale_factor=0.85), self.moverJanelaConfiguracoes()))
        self.btn70.clicked.connect(lambda: (self.parent.load_and_resize_widget_geometry(scale_factor=0.7), self.moverJanelaConfiguracoes()))
        self.btn50.clicked.connect(lambda: (self.parent.load_and_resize_widget_geometry(scale_factor=0.5), self.moverJanelaConfiguracoes()))
        self.btn100.clicked.connect(lambda: (self.parent.load_and_resize_widget_geometry(scale_factor=1), self.moverJanelaConfiguracoes()))
        self.btnfonteP.clicked.connect(lambda: self.parent.ajustar_fonte(delta=2))
        self.btnfonteM.clicked.connect(lambda: self.parent.ajustar_fonte(delta=-2))
        self.label_fonte.setText(f'{self.parent.font().pointSize()}')


    def moverJanelaConfiguracoes(self):
        button_pos = self.parent.btnconfig.pos()
        button_width = self.parent.btnconfig.width()  # Largura do botão
        button_height = self.parent.btnconfig.height()

        # Posição do canto direito do botão
        x_pos = button_pos.x() + button_width - self.width()
        y_pos = button_pos.y()  + button_height  #Mantém a posição vertical no mesmo nível do botão
        
        # Mover a janela de configurações para a posição calculada
        self.move(x_pos, y_pos)

    def showEvent(self, event):
        # Pega a posição do botão
        button_pos = self.parent.btnconfig.pos()
        button_width = self.parent.btnconfig.width()  # Largura do botão
        button_height = self.parent.btnconfig.height()

        # Posição do canto direito do botão
        x_pos = button_pos.x() + button_width - self.width()
        y_pos = button_pos.y()  + button_height  #Mantém a posição vertical no mesmo nível do botão
        
        # Mover a janela de configurações para a posição calculada
        self.move(x_pos, y_pos)
        super().showEvent(event)