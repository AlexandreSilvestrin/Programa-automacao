from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
import os
import ast
import json
from PyQt5.QtCore import QThread
from resources.config.caminhos import Caminhos
from resources.layouts.mainW import Ui_MainWindow
from controllers.abas_main.aba_prn import ABA_PRN
from controllers.abas_main.aba_razao import ABA_RAZAO
from controllers.abas_main.aba_notas_fat import ABA_NOTAS_FAT

class Worker(QThread):
    def run(self):
        global PRNui, NotasUI, exportar_db, importar_db, FaturamentoUI, RAZAOui, RAZAO_DFCui, SegundaJanela, Configuracoes, TerceiraJanela
        from core.FATURAMENTO import FaturamentoUI
        from core.RAZAO_resumo import RAZAOui
        from core.RAZAO_DFC import RAZAO_DFCui
        from controllers.sec_controller import SegundaJanela
        from controllers.ter_controller import TerceiraJanela
        from controllers.config_controller import Configuracoes
        

# Dialog de carregamento
class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Carregando")
        self.setModal(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Carregando, aguarde..."))

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)  # Sem limite, indica carregamento indefinido
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        self.setFixedSize(250, 100)

    def closeEvent(self, event):
        event.ignore() 

class MainController(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Exibir diálogo de carregamento automaticamente
        self.loading_dialog = LoadingDialog(self)
        self.loading_dialog.show()

        # Iniciar tarefa em segundo plano
        self.worker = Worker()
        self.worker.finished.connect(self.task_finished)
        self.worker.start()

        self.config = self.carregar_configuracoes()
        self.show()
        self.setWindowTitle("XY-auto")
        self.setWindowIcon(QIcon(Caminhos.CAMINHO_ICON))
        self.max_width = 1030
        self.max_height = 901
        self.setFixedSize(self.max_width, self.max_height)
        self.config_window = None
        self.configurarUI()

    def task_finished(self):
        # Fechar o diálogo quando a tarefa terminar
        self.loading_dialog.close()
        self.loading_dialog.deleteLater()
        print("Tarefa concluída!")
        # Você pode iniciar qualquer lógica adicional aqui

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
            file_path = Caminhos.CAMINHO_TEMA_ESCURO

        if botao == 'claro':
            file_path = Caminhos.CAMINHO_TEMA_CLARO

        """Carrega e aplica um arquivo de estilo QSS."""
        with open(file_path, 'r') as style_file:
            self.original_style = style_file.read()
            self.setStyleSheet(self.original_style)
        self.config['tema']= botao
        self.salvar_configuracoes(self.config)
    
    def configurarUI(self):
        self.btnVoltar.clicked.connect(lambda: self.mostrar_pagina(0, cond=True))
        self.btnVoltar.setVisible(False)
        self.btnNotas.clicked.connect(lambda: self.mostrar_pagina(1))
        self.btnPRN.clicked.connect(lambda: self.mostrar_pagina(2))
        self.btnRazao.clicked.connect(lambda: self.mostrar_pagina(3))
        self.btnRateio.clicked.connect(lambda: self.mostrar_pagina(4))
        self.btncss.clicked.connect(self.export_style)
        self.btnconfig.clicked.connect(self.abrirConfig)
        self.aba_notas_fat = ABA_NOTAS_FAT(self)
        self.aba_notas_fat.configurarNOTAS()
        self.abaPRN = ABA_PRN(self)
        self.abaPRN.configurarPRN()
        self.abaRAZAO = ABA_RAZAO(self)
        self.abaRAZAO.configurarRAZAO()
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
        with open(Caminhos.CAMINHO_JANELA1, "w") as file:
            json.dump(widget_data, file, indent=4)

        print("Geometria exportada para 'janela1.json'")

    def load_and_resize_widget_geometry(self, scale_factor=0.8):
        try:
            self.scale = scale_factor
            self.config['scale'] = scale_factor
            self.salvar_configuracoes(self.config)
            """Carrega a geometria dos widgets de um arquivo JSON e ajusta com base no fator de escala."""
            with open(Caminhos.CAMINHO_JANELA1, "r") as file:
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
            
        QApplication.instance().setFont(self.font())

    def carregar_configuracoes(self):
        try:
            if os.path.exists(Caminhos.CAMINHO_CONFIG):
                with open(Caminhos.CAMINHO_CONFIG, "r") as f:
                    return ast.literal_eval(f.read())
            return {}
        except:
            return {}

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

    def printRAZAO(self, conteudo):
        if 'LIMPAR' == conteudo:
            self.txtinfoRAZAO.setText('#'*62)
        else:
            conteudoo = self.txtinfoRAZAO.toPlainText()
            self.txtinfoRAZAO.setText(f'{conteudo}\n{conteudoo}')
        QApplication.processEvents()

    def sumirbtn(self, botao, cond=False):
        if cond:
            self.btnNotas.setVisible(True)
            self.btnPRN.setVisible(True)
            self.btnRazao.setVisible(True)
            #self.btnRateio.setVisible(True)
            
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

    def salvar_configuracoes(self, config):
        """Salva as configurações no arquivo TXT."""
        with open(Caminhos.CAMINHO_CONFIG, "w") as f:
            f.write(str(config))

    def local_arq_salvar(self, botao, tipo='arq'):
        if tipo == 'arq':
            if botao == 'prn':
                options = QFileDialog.Options()
                path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
                self.textoPRNarq.setText(path)
            elif botao == 'razao':
                options = QFileDialog.Options()
                path, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo TXT", "", "Arquivos TXT (*.txt)", options=options)
                self.razao_arq.setText(path)
        elif tipo == 'pasta':
            options = QFileDialog.Options()
            path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
            if botao == 'prn':
                self.textoPRNarq.setText(path)
            elif botao == 'razao':
                self.razao_arq.setText(path)
            elif botao == 'notas':
                self.localNotas.setText(path)
        elif tipo == 'salvar':
            options = QFileDialog.Options()
            path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
            if botao == 'prn':
                self.textoPRNlocal.setText(path)
                self.config['caminhoPRN'] = path
            elif botao == 'razao':
                self.razao_local.setText(path)
                self.config['caminhoRazao'] = path
            elif botao == 'notas':
                self.localNotasSalvar.setText(path)
                self.config['caminhoNotas'] = path
            self.salvar_configuracoes(self.config)
        elif tipo == 'abrir':
            if botao == 'prn':
                caminho_da_pasta = self.textoPRNlocal.text()
            elif botao == 'razao':
                caminho_da_pasta = self.razao_local.text()
            elif botao == 'notas':
                caminho_da_pasta = self.localNotasSalvar.text()
            os.startfile(caminho_da_pasta)




if __name__ == '__main__':
    app = QApplication([])

    window = MainController()
    window.show()

    app.exec_()