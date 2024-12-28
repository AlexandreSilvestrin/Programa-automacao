from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import json
from resources.config.caminhos import Caminhos
from core.CNPJ_API import PesquisaAPIThread
from models.banco_cnpj import CNPJModel
from resources.layouts.secW import Ui_MainWindow

class SegundaJanela(QMainWindow, Ui_MainWindow):
    def __init__(self, Cnotas):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("BUSCAR CNPJS")
        self.setWindowIcon(QIcon(Caminhos.CAMINHO_ICON))

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
        with open(Caminhos.CAMINHO_JANELA2, "r") as file:
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
        with open(Caminhos.CAMINHO_JANELA2, "w") as file:
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
            CNPJModel.add_new_data(df)
            QMessageBox.information(self, "SALVO", "BANCO DE DADOS PREENCHIDO")
            self.df = self.df[self.df['Nome'].isna()].reset_index(drop=True)
            if self.df.empty:
                self.close()
            else:
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