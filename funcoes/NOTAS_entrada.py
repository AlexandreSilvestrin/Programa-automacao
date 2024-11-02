#estou separando em arquivos diferentes o tratamento de cada tipo de arquivo pra facilitar a manutencao
import re
import pandas as pd
import traceback
from io import StringIO

def gerarentrada(caminhoE):
    try:
        with open(caminhoE, 'r', encoding='latin1') as entrada:
            dados = entrada.read().split('\n')

        dadosF = []
        padrao_regex = re.compile(r"\|\d{2}/\d{2}/\d{4}\|")
        for e, linha in enumerate(dados):
            if re.search(padrao_regex, linha):
                dadosF.append(linha)
                dadosF.append(dados[e+1])

        dadosF =  '\n'.join(dadosF)
        dadosF = dadosF.replace('.', '')
        dadosF = dadosF.replace(',', '')
        dadosF = dadosF.replace('  |            |  |    |    | |           |   |          |          |', '')
        dadosF = dadosF.replace('''   |          |          |\n|''', '')
        dados_io = StringIO(dadosF)
        dadosF = pd.read_csv(dados_io, sep='|', header=None, dtype=str)
        dadosF = dadosF[[1,4,6,8,14]]
        dadosF.columns= ['Data', 'Número', 'CNPJ', 'Valor', 'Nome']
        dadosF['Data'] = pd.to_datetime(dadosF['Data'], format='%d/%m/%Y')
        dadosF['Data'] = dadosF['Data'].dt.day
        dadosF['CNPJ'] = dadosF['CNPJ'].astype(str).replace('/', '', regex=True)
        dadosF['Nome'] = dadosF['Nome'].apply(lambda x: re.sub(r'\d{5,}', '', x))
        return {
            "df":dadosF
            }
    except Exception as e:
        erro = str(e)
        trace = traceback.format_exc()
        info = f'''INFO: HOUVE UM ERRO AO GERAR ENTRADA\nErro: {erro}'''
        return {
            "df": None,
            "info" : info,
            "erro": str(e),  # Mensagem da exceção
            "erroF": traceback.format_exc(),  # Detalhes completos do traceback
            "arquivo": "ENTRADA"
            }
    


if __name__ == "__main__": 
    print(gerarentrada(r"C:\Users\Alexandre\Downloads\drive-download-20241010T171031Z-001\LBR\ARTESP8- Consorcio LBR Modera\Entradas\E092024.txt"))