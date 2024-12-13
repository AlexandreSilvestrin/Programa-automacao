import logging
import sys
from PyQt5 import uic , QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt ,QTimer
import os
import threading
from PyQt5.QtCore import QSharedMemory
import ast
import json

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
    global PRNui, NotasUI, PesquisaAPIThread, exportar_db, importar_db ,FaturamentoUI
    from funcoes.transformarPRN2 import PRNui
    from funcoes.NOTAS import NotasUI, PesquisaAPIThread, exportar_db, importar_db
    from funcoes.FATURAMENTO import FaturamentoUI


class Configuracoes(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi("interface/config.ui", self)
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

class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface/mainW.ui", self)
        self.config = self.carregar_configuracoes()
        self.show()
        self.setWindowTitle("XY-auto")
        self.setWindowIcon(QIcon("icon/XY.ico"))
        self.max_width = 1030
        self.max_height = 901
        self.setFixedSize(self.max_width, self.max_height)
        self.config_window = None
        self.configurarUI()

    def config_tema(self):
        fonte = self.config.get('fonte')
        tema = self.config.get('tema')
        self.scale = self.config.get('scale')
        if fonte:
            self.ajustar_fonte(fonte, carregar=True)
        if tema:
            self.apply_stylesheet(tema)
        if self.scale:
            self.load_and_resize_widget_geometry(self.scale)

    def apply_stylesheet(self, botao):
        if botao == "escuro":
            file_path = 'static/dark.css'

        if botao == 'claro':
            file_path = 'static/light.css'

        """Carrega e aplica um arquivo de estilo QSS."""
        with open(file_path, 'r') as style_file:
            self.original_style = style_file.read()
            self.setStyleSheet(self.original_style)
        self.config['tema']= botao
        self.salvar_configuracoes(self.config)
    
    def configurarUI(self):
        
        #####

        self.textoPRNarq.setReadOnly(True)
        self.textoPRNlocal.setReadOnly(True)

        self.localNotasSalvar.setText(self.config.get('caminhoNotas', ''))
        self.textoPRNlocal.setText(self.config.get('caminhoPRN', ''))

        self.btnVoltar.clicked.connect(lambda: self.mostrar_pagina(0, cond=True))
        self.btnVoltar.setVisible(False)

        ### configurar FUNCOES DAS NOTAS
        self.btnFATtransformar.setVisible(False)
        self.btnNotatransformar.setVisible(False)

        self.localNotas.setReadOnly(True)
        self.localNotasSalvar.setReadOnly(True)

        self.btnNotas.clicked.connect(lambda: self.mostrar_pagina(1))
        self.btnNotaarq.clicked.connect(self.localizararqN)
        self.btnNotalocal.clicked.connect(self.localizarlocalN)
        self.btnNotatransformar.clicked.connect(self.transformarNotas)
        self.btnFATtransformar.clicked.connect(self.transformarFAT)
        self.btnCNPJ.clicked.connect(self.abrir_segunda_janela)
        self.btn_exportar.clicked.connect(self.exportarbanco)
        self.btn_importar.clicked.connect(self.importarbanco)
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
        self.btncss.clicked.connect(self.export_style)

        self.btnconfig.clicked.connect(self.abrirConfig)
        self.config_tema()

    def abrirConfig(self):
        # Verifica se a janela de configurações já está aberta
        if self.config_window and self.config_window.isVisible():
            self.config_window.close()  # Se estiver visível, fecha
        else:
            self.config_window = Configuracoes(self)  # Caso contrário, abre
            self.config_window.exec_()

    def export_style(self):
        """Exporta a geometria de todos os widgets para um arquivo JSON."""
        widget_data = {}
        
        # Itera sobre todos os widgets da janela
        for widget in self.findChildren(QWidget):  # Encontra todos os widgets filhos
            widget_name = widget.objectName()  # Obtém o nome do widget
            if widget_name:  # Apenas widgets nomeados
                geometry = widget.geometry().getRect()  # Obtém a geometria (x, y, width, height)
                widget_data[widget_name] = geometry  # Salva no dicionário

        # Salva no arquivo JSON
        with open("janela1.json", "w") as file:
            json.dump(widget_data, file, indent=4)

        print("Geometria exportada para 'janela1.json'")
    
    def load_and_resize_widget_geometry(self, scale_factor=0.8):
        try:
            self.scale = scale_factor
            self.config['scale'] = scale_factor
            self.salvar_configuracoes(self.config)
            """Carrega a geometria dos widgets de um arquivo JSON e ajusta com base no fator de escala."""
            with open("janela1.json", "r") as file:
                widget_data = json.load(file)

            # Itera sobre todos os widgets e aplica a geometria com o fator de escala
            for widget_name, geometry in widget_data.items():
                widget = getattr(self, widget_name, None)  # Obtém o widget pelo nome
                if widget:
                    # Calcula o novo tamanho e posição baseado no fator de escala
                    new_geometry = [
                        int(geometry[0] * scale_factor),  # x
                        int(geometry[1] * scale_factor),  # y
                        int(geometry[2] * scale_factor),  # width
                        int(geometry[3] * scale_factor)   # height
                    ]
                    widget.setGeometry(*new_geometry)  # Aplica a nova geometria

            final_width = int(self.max_width * scale_factor)
            final_height = int(self.max_height * scale_factor)
            
            self.setFixedSize(final_width, final_height)
            print(f"Widgets redimensionados para {scale_factor*100}% do tamanho original.")
        except:
            pass

    def ajustar_fonte(self, delta, carregar=False):
        if carregar:
            tamanho = 0
        else:
            tamanho = self.font().pointSize()
        self.config['fonte'] = tamanho+delta
        self.salvar_configuracoes(self.config)
        font = QFont("Calibri", tamanho+delta)  # Tamanho 14
        """Aplicar a fonte para todos os widgets filhos de forma recursiva"""
        self.setFont(font)  # Altera a fonte do widget atual
        if self.config_window and self.config_window.isVisible():
            self.config_window.label_fonte.setText(f'{tamanho+delta}')

        # Aplicar recursivamente aos filhos
        for child in self.findChildren(QWidget):
            child.setFont(font)
        
    def carregar_configuracoes(self):
        try:
            if os.path.exists("config.txt"):
                with open("config.txt", "r") as f:
                    return ast.literal_eval(f.read())
            return {}
        except:
            return {}

    def verificarCampos(self):
        localNotas = self.localNotas.text()
        localNotasSalvar = self.localNotasSalvar.text()
        mes = self.txtmes.currentText()
        ano = self.txtano.currentText()
        
        if os.path.exists(localNotas):
            pass
        else:
            QMessageBox.critical(self, "Erro", f"Local dos arquivos nao existe {localNotas}")
            return False, localNotas,  localNotasSalvar, mes, ano
        
        if os.path.exists(localNotasSalvar):
            pass
        else:
            QMessageBox.critical(self, "Erro", f"Local salvar arquivos nao existe {localNotasSalvar}")
            return False, localNotas,  localNotasSalvar, mes, ano

        if mes.strip() != '' and ano.strip() != '':
            return True, localNotas,  localNotasSalvar, mes, ano
        else:
            QMessageBox.critical(self, "Erro", f"Preencha mes e ano")
            return False, localNotas,  localNotasSalvar, mes, ano

    def transformarNotas(self):
        self.btnNotatransformar.setVisible(False)
        try:
            verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
            if verificacao:
                Cnotas = NotasUI(localNotas, localNotasSalvar, mes, ano, self)
                Cnotas.gerarNotas()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO 1{e}")
            print(e)

    def transformarFAT(self):
        self.btnFATtransformar.setVisible(False)
        try:
            verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
            if verificacao:
                Cfat = FaturamentoUI(localNotas, localNotasSalvar, mes, ano, self)
                Cfat.gerarFat()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"ERRO 2{e}")
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
        verificacao ,localNotas,  localNotasSalvar, mes, ano = self.verificarCampos()
        if verificacao:
            Cnotas = NotasUI(localNotas, localNotasSalvar, mes, ano, self)
            self.segunda_janela = SegundaJanela(Cnotas)
            self.segunda_janela.setStyleSheet(self.styleSheet())
            self.segunda_janela.setFont(self.font())
            self.segunda_janela.load_and_resize_widget_geometry(self.scale)
            self.btnFATtransformar.setVisible(True)
            self.btnNotatransformar.setVisible(True)
        else:
            QMessageBox.critical(self, "Erro", "O caminho do arquivo não é válido ou não existe.")

    def importarbanco(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        if file_name == '':
            pass
        else:
            importar_db(file_name)
            QMessageBox.information(self, "IMPORTADO", f"Banco de dados importado com sucesso")
    
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
            self.tableWidget.setColumnWidth(1, 550)
            self.tableWidget.setColumnWidth(0, 150)
            self.btn_salvar_banco.clicked.connect(self.juntarCNPJSbanco)
            self.btnPARAR.clicked.connect(self.pararAPI)
            
            self.btn_salvar_banco.setVisible(False) 
            self.setFixedSize(self.size())
            self.show()

    def load_and_resize_widget_geometry(self, scale_factor=0.8):
        """Carrega a geometria dos widgets de um arquivo JSON e ajusta com base no fator de escala."""
        with open("janela2.json", "r") as file:
            widget_data = json.load(file)

        # Itera sobre todos os widgets e aplica a geometria com o fator de escala
        for widget_name, geometry in widget_data.items():
            widget = getattr(self, widget_name, None)  # Obtém o widget pelo nome
            if widget:
                # Calcula o novo tamanho e posição baseado no fator de escala
                new_geometry = [
                    int(geometry[0] * scale_factor),  # x
                    int(geometry[1] * scale_factor),  # y
                    int(geometry[2] * scale_factor),  # width
                    int(geometry[3] * scale_factor)   # height
                ]
                widget.setGeometry(*new_geometry)  # Aplica a nova geometria

        final_width = int(1078 * scale_factor)
        final_height = int(614 * scale_factor)
        
        self.setFixedSize(final_width, final_height)
        print(f"Widgets redimensionados para {scale_factor*100}% do tamanho original.")

    def export_style(self):
        """Exporta a geometria de todos os widgets para um arquivo JSON."""
        widget_data = {}
        
        # Itera sobre todos os widgets da janela
        for widget in self.findChildren(QWidget):  # Encontra todos os widgets filhos
            widget_name = widget.objectName()  # Obtém o nome do widget
            if widget_name:  # Apenas widgets nomeados
                geometry = widget.geometry().getRect()  # Obtém a geometria (x, y, width, height)
                widget_data[widget_name] = geometry  # Salva no dicionário

        # Salva no arquivo JSON
        with open("janela2.json", "w") as file:
            json.dump(widget_data, file, indent=4)

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

    # Inicia o carregamento das dependências em segundo plano
    thread = threading.Thread(target=carregar_dependencias)
    thread.start()

    # Continua a execução da aplicação Qt
    app.exec_()

    # Espera a thread terminar antes de fechar o programa (opcional)
    thread.join()