import logging
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSharedMemory
from controllers.main_controller import MainController
import traceback

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


def excepthook(type, value, tb):
    # Salva o erro no log
    logging.error("Unhandled exception", exc_info=(type, value, tb))

    traceback.print_exception(type, value, tb)
    # Salva o traceback em um arquivo
    with open("erro_log.txt", "a") as f:
        f.write("Erro ocorrido:\n")
        traceback.print_exception(type, value, tb, file=f)
        f.write("\n" + "="*40 + "\n")
    
    # Exibe o erro em uma caixa de mensagem
    QMessageBox.critical(None, "Erro", f"Ocorreu um erro não tratado: {value}")
    
    # Chama o excepthook original
    sys.__excepthook__(type, value, tb)


if __name__ == "__main__":
    # Configura o manipulador global de exceções
    sys.excepthook = excepthook

    # Inicializa a aplicação Qt
    app = QApplication([])

    shared_mem = check_single_instance()
    # Cria e mostra a janela principal
    window = MainController()

    app.exec_()
