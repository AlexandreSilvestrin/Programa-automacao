from PyQt5.QtWidgets import *
import os
from core.DIMOB import conversao_dimob

class ABA_DIMOB:
    def __init__(self, main):
        self.main = main
    
    def configurarDIMOB(self):

        self.main.textoDimobarq.setReadOnly(True)
        self.main.textoDimoblocal.setReadOnly(True)
        self.main.txtinfoDimob.setReadOnly(True)

        self.main.textoDimoblocal.setText(self.main.config.get('caminhoDimob', ''))

        self.main.btnDimobtransformar.clicked.connect(self.transformarDimob)
        
        self.main.btnDimobarq.clicked.connect(lambda : self.main.local_arq_salvar('dimob'))
        self.main.btnDimoblocal.clicked.connect(lambda : self.main.local_arq_salvar('dimob', tipo='salvar'))
        self.main.btnAbrPastaDimob.clicked.connect(lambda : self.main.local_arq_salvar('dimob', tipo='abrir'))
    
    def transformarDimob(self):
        try:
            localarq = self.main.textoDimobarq.text()
            localsalvar = self.main.textoDimoblocal.text()

            if not os.path.exists(localarq):
                QMessageBox.critical(self.main, "Erro", f"Local arquivos nao existe {localarq}")
                return

            if not os.path.exists(localsalvar):
                QMessageBox.critical(self.main, "Erro", f"Local salvar arquivos nao existe {localsalvar}")
                return

            dimob, e, nome = conversao_dimob(localarq, localsalvar)
            conteudoo = self.main.txtinfoDimob.toPlainText()
            if dimob:
                self.main.txtinfoDimob.setText(f'{conteudoo} \n FINALIZADO, arquivo(s) salvo(s) em: {nome}')
                self.main.btnAbrPastaDimob.setVisible(True)
            else:
                self.main.txtinfoDimob.setText(f'{conteudoo} \n {e}\n OUVE UM ERRO ao transformar')
                QMessageBox.critical(self.main, "Erro", f"Erro ao transformar o arquivo: {e}")

        except Exception as e:
            conteudoo = self.main.txtinfoDimob.toPlainText()
            self.main.txtinfoDimob.setText(f'{conteudoo} \n {e}\n OUVE UM ERRO ao transformar')