import logging
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
import threading
from PyQt5.QtCore import QSharedMemory
import ast

def check_single_instance():
    # Nome único para o segmento de memória compartilhada
    shared_mem = QSharedMemory("XY-auto")

    # Tenta anexar à memória compartilhada existente
    if shared_mem.attach():
        # A memória compartilhada já existe, o que significa que outra instância está em execução
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Aviso")
        msg.setText("O programa já está em execução.")
        msg.exec_()

        sys.exit(0)  # Encerra a nova instância do programa
    else:
        # Cria a memória compartilhada, indicando que esta é a primeira instância
        shared_mem.create(1)
    return shared_mem

def excepthook(type, value, traceback):
    logging.error("Unhandled exception", exc_info=(type, value, traceback))
    print(traceback)
    QMessageBox.critical(None, "Erro", f"Ocorreu um erro não tratado: {value}")
    sys.__excepthook__(type, value, traceback)

# Função para carregar as dependências pesadas
def carregar_dependencias():
    global PRNui, NotasUI, PesquisaAPIThread, exportar_db, FaturamentoUI
    from funcoes.transformarPRN2 import PRNui
    from funcoes.NOTAS import NotasUI, PesquisaAPIThread, exportar_db
    from funcoes.FATURAMENTO import FaturamentoUI


class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface/mainW.ui", self)
        self.config = self.carregar_configuracoes()
        self.configurarUI()
        self.setFixedSize(self.size())
        self.setWindowTitle("XY-auto")
        self.setWindowIcon(QIcon("icon/XY.ico"))
        
    def configurarUI(self):
        self.textoPRNarq.setReadOnly(True)
        self.textoPRNlocal.setReadOnly(True)

        self.localNotasSalvar.setText(self.config.get('caminhoNotas', ''))
        self.textoPRNlocal.setText(self.config.get('caminhoPRN', ''))

        self.btnVoltar.clicked.connect(lambda: self.mostrar_pagina(0, cond=True))
        self.btnVoltar.setVisible(False)

        ### configurar FUNCOES DAS NOTAS

        self.localNotas.setReadOnly(True)
        self.localNotasSalvar.setReadOnly(True)

        self.btnNotas.clicked.connect(lambda: self.mostrar_pagina(1))
        self.btnNotaarq.clicked.connect(self.localizararqN)
        self.btnNotalocal.clicked.connect(self.localizarlocalN)
        self.btnNotatransformar.clicked.connect(self.transformarNotas)
        self.btnFATtransformar.clicked.connect(self.transformarFAT)
        self.btnCNPJ.clicked.connect(self.abrir_segunda_janela)
        self.btn_exportar.clicked.connect(self.exportarbanco)
        self.btnAbrPastaNota.clicked.connect(self.abrirpastaN)
        self.btnAbrPastaNota.setVisible(False)

        ######################
        self.btnPRN.clicked.connect(lambda: self.mostrar_pagina(2))
        self.btnPRNarq.clicked.connect(self.localizararq)
        self.btnPRNpasta.clicked.connect(self.localizarpasta)
        self.btnPRNlocal.clicked.connect(self.localizarlocal)
        
        self.btnAbrPasta.clicked.connect(self.abrirpasta)
        self.btnAbrPasta.setVisible(False)

        ##
        self.btnRazao.clicked.connect(lambda: self.mostrar_pagina(3))
        self.btnRateio.clicked.connect(lambda: self.mostrar_pagina(4))
        self.btnPRNtransformar.clicked.connect(self.transformarprn)

    def verificarCampos(self):
        localNotas = self.localNotas.text()
        localNotasSalvar = self.localNotasSalvar.text()
        mes = self.txtmes.currentText()
        ano = self.txtano.currentText()
        txtTomados = f'I56{mes}{ano}.txt'
        txtPrestados = f'I51{mes}{ano}.txt'
        txtEntrada = f'E{mes}{ano}.txt'

        if os.path.exists(localNotas):
            pass
        else:
            QMessageBox.critical(self, "Erro", f"Local dos arquivos nao existe {localNotas}")
            return False, localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados
        
        if os.path.exists(localNotasSalvar):
            pass
        else:
            QMessageBox.critical(self, "Erro", f"Local salvar arquivos nao existe {localNotasSalvar}")
            return False, localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados

        if mes.strip() != '' and ano.strip() != '':
            return True, localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados
        else:
            QMessageBox.critical(self, "Erro", f"Preencha mes e ano")
            return False, localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados

    def transformarNotas(self):
        try:
            verificacao ,localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados = self.verificarCampos()
            if verificacao:
                Cnotas = NotasUI(localNotas, localNotasSalvar, txtTomados, txtEntrada, self)
                Cnotas.gerarNotas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO {e}")
            print(e)

    def transformarFAT(self):
        try:
            verificacao ,localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados = self.verificarCampos()
            if verificacao:
                Cfat = FaturamentoUI(localNotas, localNotasSalvar, txtPrestados, self)
                Cfat.gerarFat()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO {e}")
            print(e)

    def printNotas(self, conteudo):
        if 'completou Notas' == conteudo:
            QMessageBox.information(self, "NOTAS", "Notas gerado")
            self.btnAbrPastaNota.setVisible(True)
        if 'completou Faturamento' == conteudo:
            QMessageBox.information(self, "FATURAMENTO", "Faturamento gerado")
            self.btnAbrPastaNota.setVisible(True)
        if 'LIMPAR' == conteudo:
            self.txtinfoNota.setText('')
        else:
            conteudoo = self.txtinfoNota.toPlainText()
            self.txtinfoNota.setText(f'{'#'*62}\n{conteudo}\n{conteudoo}')
        QApplication.processEvents()

    def printPRN(self, conteudo):
        if 'LIMPAR' == conteudo:
            self.txtinfoPRN.setText('#'*62)
        else:
            conteudoo = self.txtinfoPRN.toPlainText()
            self.txtinfoPRN.setText(f'{conteudo}\n{conteudoo}')
        QApplication.processEvents()

    def abrirpastaN(self):
        caminho_da_pasta = self.localNotasSalvar.text()
        os.startfile(caminho_da_pasta)

    def abrirpasta(self):
        caminho_da_pasta = self.textoPRNlocal.text()
        os.startfile(caminho_da_pasta)

    def sumirbtn(self, botao, cond=False):
        if cond:
            self.btnNotas.setVisible(True)
            self.btnPRN.setVisible(True)
            self.btnRazao.setVisible(True)
            self.btnRateio.setVisible(True)
            
            self.btnVoltar.setVisible(False)
            botao.setVisible(False)
        else:
            self.btnNotas.setVisible(False)
            self.btnPRN.setVisible(False)
            self.btnRazao.setVisible(False)
            self.btnRateio.setVisible(False)

            self.btnVoltar.setVisible(True)
            botao.setVisible(True)

    def mostrar_pagina(self,index, cond=False):
        sender_button = self.sender()
        self.sumirbtn(sender_button, cond)
        self.stackedWidget.setCurrentIndex(index)

    def localizarpasta(self):
        options = QFileDialog.Options()
        file_name = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        self.textoPRNarq.setText(file_name)

    def localizararq(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        self.textoPRNarq.setText(file_name)

    def localizarlocal(self): #local salvar prn
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        self.config['caminhoPRN'] = folder_path
        self.salvar_configuracoes(self.config)
        self.textoPRNlocal.setText(folder_path)
    
    def localizararqN(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        self.localNotas.setText(folder_path)

    def localizarlocalN(self): #funcao pra selecioar local onde ira salvar
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        self.config['caminhoNotas'] = folder_path
        self.salvar_configuracoes(self.config)
        self.localNotasSalvar.setText(folder_path)

    def carregar_configuracoes(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                return ast.literal_eval(f.read())
        return {}

    def salvar_configuracoes(self, config):
        """Salva as configurações no arquivo TXT."""
        with open("config.txt", "w") as f:
            f.write(str(config))

    def transformarprn(self):
        try:
            localarq = self.textoPRNarq.text()
            localsalvar = self.textoPRNlocal.text()

            if not os.path.exists(localarq):
                QMessageBox.critical(self, "Erro", f"Local arquivos nao existe {localarq}")
                return

            if not os.path.exists(localsalvar):
                QMessageBox.critical(self, "Erro", f"Local salvar arquivos nao existe {localsalvar}")
                return

            prn = PRNui(localarq, localsalvar, self)
            if prn.verificar():
                conteudoo = self.txtinfoPRN.toPlainText()
                self.txtinfoPRN.setText(f'{conteudoo} \n FINALIZADO, arquivo(s) salvo(s)')
                self.btnAbrPasta.setVisible(True)
            else:
                pass
        except Exception as e:
            self.txtinfoPRN.setText(f'{conteudoo} \n {e}\n OUVE UM ERRO ao transformar')

    def abrir_segunda_janela(self):
        verificacao ,localNotas,  localNotasSalvar, txtTomados, txtEntrada, txtPrestados = self.verificarCampos()
        if verificacao:
            Cnotas = NotasUI(localNotas, localNotasSalvar, txtTomados, txtEntrada, self)
            self.segunda_janela = SegundaJanela(Cnotas)
        else:
            QMessageBox.critical(self, "Erro", "O caminho do arquivo não é válido ou não existe.")

    def exportarbanco(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        if folder_path == '':
            pass
        else:
            exportar_db(folder_path)
            QMessageBox.information(self, "SALVO", f"Banco de dados salvo em: \n {folder_path}")

class SegundaJanela(QMainWindow):
    def __init__(self, Cnotas):
        super().__init__()
        uic.loadUi("interface/secW.ui", self)
        self.setWindowTitle("BUSCAR CNPJS")
        self.setWindowIcon(QIcon("icon/XY.ico"))

        self.setWindowModality(Qt.ApplicationModal)

        self.Cnotas = Cnotas
        self.df = self.verificarDF()
        self.salvo = True
        
        if self.df is None:
            self.close()
        else:
            self.preencher_tabela(self.df)
            self.btnPesqAPI.clicked.connect(self.iniciar_pesquisa)
            # Preencher a tabela com os dados iniciais
            self.thread = PesquisaAPIThread()
            self.thread.resultado_encontrado.connect(self.atualizar)
            self.btnSalvarCNPJS.clicked.connect(self.salvarCNPJS)
            self.tableWidget.setColumnWidth(1, 550)
            self.tableWidget.setColumnWidth(0, 150)
            self.btn_salvar_banco.clicked.connect(self.juntarCNPJSbanco)
            self.btnPARAR.clicked.connect(self.pararAPI)
            
            self.btn_salvar_banco.setVisible(False) 
            self.setFixedSize(self.size())
            self.show()

    def verificarDF(self):
        df = self.Cnotas.pegarCNPJS()
        if df.empty:
            QMessageBox.information(self, "SEM DADOS", "Nao tem CNPJS para pesquisar")
            return None
        else:
            QMessageBox.information(self, "", "Temos alguns CNPJS para pesquisar")
            return df
        
    def closeEvent(self, event):
        if self.df is None:
            event.accept()
        elif self.salvo:
            self.thread.terminate()  # Encerrando a thread ao fechar a janela
            event.accept()  
        else:
            resposta = QMessageBox.question(self, 'Fechar', 'Deseja fechar sem salvar? O progresso sera perdido', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if resposta == QMessageBox.Yes:
                self.thread.terminate()  # Encerrando a thread ao fechar a janela
                event.accept()  # Aceitando o evento de fechar a janela
            else:
                event.ignore()  # Ignorando o evento de fechar a janela # Aceitando o evento de fechar a janela

    def pararAPI(self):
        self.btn_salvar_banco.setVisible(True) 
        self.thread.terminate()
        self.labelP.setText(f"PARADO: {self.progress} de {len(self.df)} concluidos")
        self.labelP.setStyleSheet("background-color: red")

    def juntarCNPJSbanco(self):
        df = self.df[self.df['Nome'].notna()]
        caixa_dialogo = QMessageBox.question(self, 'JUNTAR CNPJS E BANCO', "Você quer salvar os CNPJS no banco de DADOS?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if caixa_dialogo == QMessageBox.Yes:
            self.salvo = True
            self.Cnotas.atualizarBANCOCNPJ(df)
            QMessageBox.information(self, "SALVO", "BANCO DE DADOS PREENCHIDO")
            self.df = self.df[self.df['Nome'].isna()].reset_index(drop=True)
            self.preencher_tabela(self.df)
        else:
            print("Usuário escolheu 'Não'")

    def salvarCNPJS(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        self.df.to_excel(f'{folder_path}/CNPJSnovos.xlsx', index=False)
        QMessageBox.information(self, "SALVO", "ARQUIVO EXCEL SALVO.")

    def iniciar_pesquisa(self):
        self.podesalvar = False
        if self.salvo:
            self.btn_salvar_banco.setVisible(False) 
            self.salvo = False
            self.thread.definirparametro(self.df)
            self.thread.start()
        else:
            QMessageBox.information(self, 'Iniciar', 'Se inicicar novamente antes de salvar o progresso ira recomeçar')

    def atualizar(self, i, nome, quant):

        df = self.df.copy()
        df.at[i, 'Nome'] = nome
        self.df = df.copy()

        # Configurar número de linhas e colunas
        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setColumnCount(len(df.columns))
        self.progress += 1
        if len(self.df) == self.progress:
            self.labelP.setText(f"FINALIZADO: {self.progress} de {len(self.df)} concluidos")
            self.labelP.setStyleSheet("background-color: green")
        else:
            self.labelP.setText(f"AGUARDE: {self.progress} de {len(self.df)} concluidos")
            self.labelP.setStyleSheet("background-color: yellow")
        total_minutos_necessarios = (len(self.df)-self.progress) * 1 / 3
        horas = int(total_minutos_necessarios // 60)
        minutos = int(total_minutos_necessarios % 60)
        segundos = int((total_minutos_necessarios % 1) * 60)
        self.labelP_2.setText(f"Tempo estimado: {horas}:{minutos}:{segundos}")
        QApplication.processEvents()
        # Preencher a tabela com os dados do DataFrame
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)

    def preencher_tabela(self,df):
        self.progress = 0
        self.labelP.setText(f"Parado: {self.progress} de {len(self.df)} concluidos")
        self.labelP.setStyleSheet("")

        # Configurar número de linhas e colunas
        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setColumnCount(len(df.columns))
        
        # Preencher a tabela com os dados do DataFrame
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(i, j, item)


if __name__ == "__main__":
    # Configura o manipulador global de exceções
    sys.excepthook = excepthook

    # Inicializa a aplicação Qt
    app = QApplication([])

    shared_mem = check_single_instance()
    # Cria e mostra a janela principal
    window = JanelaPrincipal()
    window.show()

    # Inicia o carregamento das dependências em segundo plano
    thread = threading.Thread(target=carregar_dependencias)
    thread.start()

    # Continua a execução da aplicação Qt
    app.exec_()

    # Espera a thread terminar antes de fechar o programa (opcional)
    thread.join()