from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from resources.config.caminhos import Caminhos
from resources.layouts.tercW import Ui_MainWindow
from models.banco_fat import FATModel
import json

class TerceiraJanela(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(Caminhos.CAMINHO_ICON))
        self.setWindowModality(Qt.ApplicationModal)
        
        self.show()
        self.configUI()
        
    def configUI(self):
        self.btn_pesq.clicked.connect(self.pesquisar)
        self.txt_cnpj.setInputMask("99.999.999/9999-99")
        self.btn_salvar.clicked.connect(self.salvar)
        self.btn_exportar.clicked.connect(self.exportarbanco)
        self.btn_importar.clicked.connect(self.importarbanco)

    def load_and_resize_widget_geometry(self, scale_factor=0.8):
        """Carrega a geometria dos widgets de um arquivo JSON e ajusta com base no fator de escala."""
        with open(Caminhos.CAMINHO_JANELA3, "r") as file:
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

        final_width = int(801 * scale_factor)
        final_height = int(255 * scale_factor)
        
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
        with open(Caminhos.CAMINHO_JANELA3, "w") as file:
            json.dump(widget_data, file, indent=4)
    
    def pesquisar(self):
        self.ret_ir.setChecked(False)
        self.ret_pis.setChecked(False)
        self.ret_cofins.setChecked(False)
        self.ret_csll.setChecked(False) 
        cnpj = self.txt_cnpj.text()
        print(cnpj)
        if cnpj == '':
            QMessageBox.information(self, "CNPJ", "Verifique se o campo do CNPJ esta digitado corretamente")
        else:
            lista = FATModel.pesquisar_cnpj(cnpj)
            if lista:
                codigo, razao, cnpj, porcent, ret= lista
                self.txt_contrato.setText(codigo)
                self.txt_porcent.setText(porcent)
                self.txt_razao.setText(razao)
                if "IR" in ret:
                    self.ret_ir.setChecked(True)
                if "PIS" in ret:
                    self.ret_pis.setChecked(True) 
                if "COFINS" in ret:
                    self.ret_cofins.setChecked(True) 
                if "CSLL" in ret:
                    self.ret_csll.setChecked(True) 

            else:
                QMessageBox.information(self, "CNPJ", "CNPJ nao existe")
    
    def salvar(self):
        cnpj = self.txt_cnpj.text()
        codigo= self.txt_contrato.text()
        razao= self.txt_razao.text()
        porcent= self.txt_porcent.text()
        ret=[]
        if self.ret_ir.isChecked():
            ret.append("IR")
        if self.ret_pis.isChecked():
            ret.append("PIS")
        if self.ret_cofins.isChecked():
            ret.append("COFINS")
        if self.ret_csll.isChecked():
            ret.append("CSLL")
        
        print(cnpj)
        if len(cnpj.strip()) < 18 or codigo.strip() == '' or razao.strip() =='' or porcent.strip() == '' or len(ret) == 0:
            QMessageBox.information(self, "CAMPOS", 'COMPLETE TODOS CAMPOS PARA SALVAR')
            return
        ret = ', '.join(ret)

        if FATModel.pesquisar_cnpj(cnpj):
            try:
                resposta = QMessageBox.question(self, 'ATUALIZAR', 'Esse CNPJ ja existe, deseja atualizar?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if resposta == QMessageBox.Yes:
                    FATModel.add_new_data([codigo, razao, cnpj, porcent, ret])
                    QMessageBox.information(self, "SALVO", f'{razao} Alterado com sucesso')
            except:
                QMessageBox.critical(self, "ERRO AO SALVAR", 'ERRO AO SALVAR')
        else:
            FATModel.add_new_data([codigo, razao, cnpj, porcent, ret])
            QMessageBox.information(self, "SALVO", f'{razao} Criado com sucesso')

    def importarbanco(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Selecionar Arquivo Excel", "", "Arquivos Excel (*.xlsx)", options=options)
        if file_name == '':
            pass
        else:
            FATModel.importar_db(file_name)
            QMessageBox.information(self, "IMPORTADO", f"Banco de dados importado com sucesso")
    
    def exportarbanco(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, "Selecionar Pasta", "", options=options)
        if folder_path == '':
            pass
        else:
            FATModel.exportar_db(folder_path)
            QMessageBox.information(self, "SALVO", f"Banco de dados salvo em: \n {folder_path}")