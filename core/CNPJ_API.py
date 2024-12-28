import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal


class PesquisaAPIThread(QThread):
    resultado_encontrado = pyqtSignal(int, str, int)

    def __init__(self):
        super().__init__()

    def definirparametro(self, df):
        self.df = df

    def run(self):
        def consultarAPI(cnpj):
            MAX_TENTATIVAS = 3
            tentativas = 0
            
            while tentativas < MAX_TENTATIVAS:
                teste = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj}')
                if teste.status_code == 200:
                    try:
                        dados_json = teste.json()
                        return dados_json['nome']
                    except:
                        return 'NaN'
                else:
                    teste2 = requests.get(f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}")
                    if teste2.status_code == 200:
                        try:
                            dados_json = teste2.json()
                            return dados_json['razao_social']
                        except:
                            return 'NaN'
                    else:
                        print('tentando novamente em 30 segundos')
                        time.sleep(30)
                        tentativas += 1

            print('execucao parada ou encerrada')
            return 'NaN'

        for i, cnpj in enumerate(self.df['CNPJ']):
            print(f'Faltam {len(self.df) - i} CNPJs para pesquisar')
            nome = consultarAPI(cnpj)
            self.resultado_encontrado.emit(i, nome, len(self.df))
        else:
            print('Completou!')