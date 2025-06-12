#estou separando em arquivos diferentes o tratamento de cada tipo de arquivo pra facilitar a manutencao
import re
import pandas as pd
import traceback
from io import StringIO

def organizerdf(df1, df2):
    for indice, linha in df2.iterrows():
        numero_correspondente = linha['Número']
        
        # Localizar a linha no DataFrame principal com o número correspondente
        indice_inserir = df1[df1['Número'] == numero_correspondente].index[0]
        
        # Inserir a linha do DataFrame secundário na linha seguinte ao DataFrame principal
        df1 = pd.concat([df1.loc[:indice_inserir], linha.to_frame().transpose(), df1.loc[indice_inserir+1:]]).reset_index(drop=True)
    return df1

def gerartomados(caminhoT):
    try:
        with open(caminhoT, 'r', encoding='latin-1') as txttomados:
            dados = txttomados.read().replace(',', '').replace('.', '')
        

        if "SEM MOVIMENTO" in dados:
            print('sem movimento')
            return {"df": 'SEM MOVIMENTO'}

        # r'-{13}.*?-{13}'  - oque sera removido  {13} quantidade . qualquer caracter * zero ou mais aparicoes ? pega sempre as primeiras aparicoes// re.DOTALL o . detecta a quebra de linha
        linhas_organizadas = re.sub(r'\n {30}', '', dados, flags=re.DOTALL).split('\n')
        linhas_selecionadas = []

        padrao_regex = re.compile(r'empresa(.*?)folha', re.DOTALL | re.IGNORECASE)
        empresa = padrao_regex.search(dados).group(0).replace('Folha', '').replace(':', '').replace('empresa', '').strip()

        padrao_regex = r"\|\s\d+\|\s\w\w\w"
        for linha in linhas_organizadas:
            if re.search(padrao_regex, linha):
                linhas_selecionadas.append(linha)

        if not linhas_selecionadas:
            dadosF = pd.DataFrame(columns=['Data', 'Número', 'Valor', 'CNPJ', 'Tipo'])
            return dadosF, empresa.replace(':', '').replace('empresa', '').strip()
        
        linhas_selecionadas =  '\n'.join(linhas_selecionadas)
        dados_io = StringIO(linhas_selecionadas)
        dadosF = pd.read_csv(dados_io, sep='|', header=None, dtype=str)
        dadosF.columns= ['zero', 'Data', 'dois', 'tres', 'Número', 'Valor' , 'seis', 'sete', 'oito', 'ISS Retido', 'CNPJ', 'onze', '12', '13']
        dadosF = dadosF[['Data', 'Número', 'Valor' , 'ISS Retido', 'CNPJ']]
        dadosF['ISS Retido'] = dadosF['ISS Retido'].astype(int)
        dfiss = dadosF[dadosF['ISS Retido'] > 0].copy()
        if not dfiss.empty:
            dfiss['Tipo'] = 'ISS'
            dfiss = dfiss[['Data', 'Número', 'ISS Retido', 'CNPJ', 'Tipo']].reset_index(drop=True)
            dfiss.rename(columns={'ISS Retido': 'Valor'}, inplace=True)

        dadosF['Tipo'] = 'Total'
        dadosF = dadosF[['Data', 'Número', 'Valor', 'CNPJ', 'Tipo']]
        dadosF = organizerdf(dadosF, dfiss)

        return {
            "df":dadosF
            }

    except Exception as e:
        erro = str(e)
        trace = traceback.format_exc()
        info = f'''INFO: HOUVE UM ERRO AO GERAR TOMADOS\nErro: {erro}'''
        print(trace)
        
        print('#'*30)

        return {
            "df": None,
            "info" : info,
            "erro": str(e),  # Mensagem da exceção
            "erroF": traceback.format_exc(),  # Detalhes completos do traceback
            "arquivo": "TOMADOS"
            }


if __name__ == "__main__": 
    print(gerartomados(r"C:\Users\Alexandre\Desktop\lbr\sehab-6\tomados\I56122024.txt"))