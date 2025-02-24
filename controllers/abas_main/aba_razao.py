from PyQt5.QtWidgets import *
import os
from core.RAZAO_DFC import RAZAO_DFCui
from core.RAZAO_resumo import RAZAOui

class ABA_RAZAO:
    def __init__(self, main):
        self.main = main


    def configurarRAZAO(self):
        self.main.razao_txt_contras.setVisible(False)
        self.main.label_razao2_2.setVisible(False)
        self.main.razao_arq.setReadOnly(True)
        self.main.razao_local.setReadOnly(True)
        self.main.txtinfoRAZAO.setReadOnly(True)
        self.main.razao_local.setText(self.main.config.get('caminhoRazao', ''))

        self.main.rb_razao_dfc.toggled.connect(self.alternar_campo)
        self.main.btnRAZAOtransformar.clicked.connect(self.transformarRAZAO)

        self.main.btnRAZAOarq.clicked.connect(lambda : self.main.local_arq_salvar('razao'))
        self.main.btnRAZAOpasta.clicked.connect(lambda : self.main.local_arq_salvar('razao', tipo='pasta'))
        self.main.btnRAZAOlocal.clicked.connect(lambda : self.main.local_arq_salvar('razao', tipo='salvar'))
        self.main.btnAbrPastaRazao.clicked.connect(lambda : self.main.local_arq_salvar('razao', tipo='abrir'))
        self.main.btnAbrPastaRazao.setVisible(False)
    
    def alternar_campo(self):
        self.main.razao_txt_contras.setVisible(self.main.rb_razao_dfc.isChecked())
        self.main.label_razao2_2.setVisible(self.main.rb_razao_dfc.isChecked())
    
    def transformarRAZAO(self):
        try:
            localarq = self.main.razao_arq.text()
            localsalvar = self.main.razao_local.text()

            if not os.path.exists(localarq):
                QMessageBox.critical(self.main, "Erro", f"Local arquivos nao existe {localarq}")
                return

            if not os.path.exists(localsalvar):
                QMessageBox.critical(self.main, "Erro", f"Local salvar arquivos nao existe {localsalvar}")
                return

            if self.main.rb_razao_dfc.isChecked():
                lista_contras = [int(item.strip()) for item in self.main.razao_txt_contras.text().split(',')]
                razao = RAZAO_DFCui(localarq, localsalvar, lista_contras, self.main)

            elif self.main.rb_razao.isChecked():
                razao = RAZAOui(localarq, localsalvar, self.main)

            else:
                QMessageBox.critical(self.main, "Nao selecionado", f"Selecione uns dos check")
                return

            if razao.resumir():
                conteudoo = self.main.txtinfoRAZAO.toPlainText()
                self.main.txtinfoRAZAO.setText(f'{conteudoo} \n FINALIZADO, arquivo(s) salvo(s)')
                self.main.btnAbrPastaRazao.setVisible(True)
            
        except Exception as e:
            self.main.txtinfoRAZAO.setText(f'{localarq} \n {e}\n OUVE UM ERRO ao transformar')