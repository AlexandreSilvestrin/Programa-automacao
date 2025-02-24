from PyQt5.QtWidgets import *
import os
from core.PRN_T import PRNui

class ABA_PRN:
    def __init__(self, main):
        self.main = main
    
    def configurarPRN(self):

        self.main.textoPRNarq.setReadOnly(True)
        self.main.textoPRNarq.setToolTip("Pode ser um arquivo unico ou uma pasta contendo varias arquivos pra serem transformados")
        self.main.textoPRNlocal.setReadOnly(True)
        self.main.txtinfoPRN.setReadOnly(True)

        self.main.textoPRNlocal.setText(self.main.config.get('caminhoPRN', ''))

        self.main.btnPRNtransformar.clicked.connect(self.transformarprn)
        
        self.main.btnPRNarq.clicked.connect(lambda : self.main.local_arq_salvar('prn'))
        self.main.btnPRNpasta.clicked.connect(lambda : self.main.local_arq_salvar('prn', tipo='pasta'))
        self.main.btnPRNlocal.clicked.connect(lambda : self.main.local_arq_salvar('prn', tipo='salvar'))
        self.main.btnAbrPasta.clicked.connect(lambda : self.main.local_arq_salvar('prn', tipo='abrir'))
        self.main.btnAbrPasta.setVisible(False)
    
    def transformarprn(self):
        try:
            localarq = self.main.textoPRNarq.text()
            localsalvar = self.main.textoPRNlocal.text()

            if not os.path.exists(localarq):
                QMessageBox.critical(self.main, "Erro", f"Local arquivos nao existe {localarq}")
                return

            if not os.path.exists(localsalvar):
                QMessageBox.critical(self.main, "Erro", f"Local salvar arquivos nao existe {localsalvar}")
                return

            prn = PRNui(localarq, localsalvar, self.main)
            if prn.verificar():
                conteudoo = self.main.txtinfoPRN.toPlainText()
                self.main.txtinfoPRN.setText(f'{conteudoo} \n FINALIZADO, arquivo(s) salvo(s)')
                self.main.btnAbrPasta.setVisible(True)

        except Exception as e:
            self.main.txtinfoPRN.setText(f'{conteudoo} \n {e}\n OUVE UM ERRO ao transformar')