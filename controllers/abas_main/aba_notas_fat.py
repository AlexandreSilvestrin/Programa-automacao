from PyQt5.QtWidgets import *
import os
from core.FATURAMENTO import FaturamentoUI
from controllers.sec_controller import SegundaJanela
from controllers.ter_controller import TerceiraJanela
from core.NOTAS import NotasUI
from models.banco_cnpj import CNPJModel

class ABA_NOTAS_FAT:
    def __init__(self, main):
        self.main = main

    def configurarNOTAS(self):
        self.main.localNotasSalvar.setText(self.main.config.get('caminhoNotas', ''))
        self.main.btnNotatransformar.setEnabled(False)
        self.main.btnNotatransformar.setToolTip("PESQUISAR CNPJ antes de continuar.")
        self.main.localNotas.setReadOnly(True)
        self.main.localNotas.setToolTip("Pasta dos arquivos (LBR, SONDOTECNICA, PLANSERV)")
        self.main.localNotasSalvar.setReadOnly(True)
        self.main.localNotasSalvar.setToolTip("Selecione uma pasta de saida geral apenas (o codigo ira criar a pasta da empresa e salvar os arquivos)")
        self.main.txtinfoNota.setReadOnly(True)
        self.main.btn_porcent.clicked.connect(self.abrir_terceira_janela)
        self.main.btnNotatransformar.clicked.connect(self.transformarNotas)
        self.main.btnFATtransformar.clicked.connect(self.transformarFAT)

        self.main.btnNotaarq.clicked.connect(lambda : self.main.local_arq_salvar('notas', tipo='pasta'))
        self.main.btnNotalocal.clicked.connect(lambda : self.main.local_arq_salvar('notas', tipo='salvar'))
        self.main.btnAbrPastaNota.clicked.connect(lambda : self.main.local_arq_salvar('notas', tipo='abrir'))
        self.main.btnCNPJ.clicked.connect(self.abrir_segunda_janela)
        self.main.btn_exportar.clicked.connect(self.exportarbanco)
        self.main.btn_exportar.setToolTip("Salva uma copia do banco CNPJ")
        self.main.btn_importar.clicked.connect(self.importarbanco)
        self.main.btn_importar.setToolTip("Adiciona novos dados no banco CNPJ")
        self.main.btnAbrPastaNota.setVisible(False)

    def transformarNotas(self):
        self.main.btnNotatransformar.setEnabled(False)
        try:
            verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
            if verificacao:
                Cnotas = NotasUI(localNotas, localNotasSalvar, mes, ano, self.main)
                Cnotas.gerarNotas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO 1{e}")
            print(e)
        
    def transformarFAT(self):
        try:
            verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
            if verificacao:
                Cfat = FaturamentoUI(localNotas, localNotasSalvar, mes, ano, self.main)
                Cfat.gerarFat()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO 2{e}")
            print(e)

    def verificarCampos(self):
        localNotas = self.main.localNotas.text()
        localNotasSalvar = self.main.localNotasSalvar.text()
        mes = self.main.txtmes.currentText()
        ano = self.main.txtano.currentText()
        
        if os.path.exists(localNotas):
            pass
        else:
            QMessageBox.critical(self.main, "Erro", f"Local dos arquivos nao existe {localNotas}")
            return False, localNotas,  localNotasSalvar, mes, ano
        
        if os.path.exists(localNotasSalvar):
            pass
        else:
            QMessageBox.critical(self.main, "Erro", f"Local salvar arquivos nao existe {localNotasSalvar}")
            return False, localNotas,  localNotasSalvar, mes, ano

        if mes.strip() != '' and ano.strip() != '':
            return True, localNotas,  localNotasSalvar, mes, ano
        else:
            QMessageBox.critical(self.main, "Erro", f"Preencha mes e ano")
            return False, localNotas,  localNotasSalvar, mes, ano
    
    def abrir_segunda_janela(self):
        verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
        if verificacao:
            Cnotas = NotasUI(localNotas, localNotasSalvar, mes, ano, self.main)
            self.main.segunda_janela = SegundaJanela(Cnotas)
            self.main.segunda_janela.setStyleSheet(self.main.styleSheet())
            self.main.segunda_janela.setFont(self.main.font())
            self.main.segunda_janela.load_and_resize_widget_geometry(self.main.scale)
            self.main.btnNotatransformar.setEnabled(True)
        else:
            QMessageBox.critical(self.main, "Erro", "O caminho do arquivo não é válido ou não existe.")
    
    def abrir_terceira_janela(self):
        self.tercJ = TerceiraJanela()
        self.tercJ.setStyleSheet(self.main.styleSheet())
        self.tercJ.load_and_resize_widget_geometry(self.main.scale)

    def importarbanco(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.main, "Selecionar Arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        if file_name == '':
            pass
        else:
            CNPJModel.importar_db(file_name)
            QMessageBox.information(self.main, "IMPORTADO", f"Banco de dados importado com sucesso")
    
    def exportarbanco(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self.main, "Selecionar Pasta", "", options=options)
        if folder_path == '':
            pass
        else:
            CNPJModel.exportar_db(folder_path)
            QMessageBox.information(self.main, "SALVO", f"Banco de dados salvo em: \n {folder_path}")