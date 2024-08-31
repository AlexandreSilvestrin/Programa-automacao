import re
import tabula
import os
import pandas as pd
from io import StringIO
import openpyxl
from unidecode import unidecode
import PyPDF2
import warnings
import requests
import json
import time
from PyQt5.QtCore import QThread, pyqtSignal

warnings.filterwarnings("ignore", category=FutureWarning, message="errors='ignore' is deprecated")

def exportar_db(folder_path):
    dfbanco = pd.read_excel('BANCOCNPJ.xlsx')
    dfbanco.columns = ('CNPJ/CPF', 'Nome')
    dfbanco['CNPJ/CPF'] = dfbanco['CNPJ/CPF'].apply(lambda x: str(x).zfill(14))
    dfbanco.to_excel(f'{folder_path}/BANCOCNPJ.xlsx', index=False)


class Notas:
    def __init__(self, local, local_salvar, txt_tomados, txt_entrada):
        self.local = local
        self.local_salvar = local_salvar
        self.txt_tomados = txt_tomados
        self.txt_entrada = txt_entrada
        self.caminhos = self.listarcaminhos(local, txt_entrada, txt_tomados)
        self.data = self.pegardata()
        self.banco = self.lerbanco()

    def printarInformacoes(self, conteudo):
        print(conteudo)

    def pegardata(self):
        nome = self.txt_tomados.replace('.txt', '')
        return nome[-6:-4], nome[-4:]

    def criar_pasta(self):
        ultimo_diretorio = os.path.basename(self.local)
        os.makedirs(f'{self.local_salvar}/{ultimo_diretorio}', exist_ok=True)
        if not os.path.exists(f'{self.local_salvar}/{ultimo_diretorio}/TUDO.xlsx'):
            teste = pd.DataFrame(columns=['Data', 'Número', 'CNPJ/CPF' , 'Vazia1', 'Vazia2','Valor', 'NF Nome', 'Tipo'])
            teste.to_excel(f'{self.local_salvar}/{ultimo_diretorio}/TUDO.xlsx', index=False)
        self.local_salvar = f'{self.local_salvar}/{ultimo_diretorio}'

    def listarcaminhos(self, base_directory, txtentrada, txttomados):
        substrings = ['retencoes', 'retencao', 'Retençao', 'Retenção']
        lista_caminhos = []
        for pasta in os.listdir(base_directory):
            file_path_entrada, file_path_tomados, file_path_pdf = False, False, False

            for root, dirs, files in os.walk(f'{base_directory}/{pasta}'):
                for file in files:
                    if file in txtentrada:
                        file_path_entrada = os.path.join(root, file)
                    if file in txttomados:
                        file_path_tomados = os.path.join(root, file)
                    if any(substring in unidecode(file).lower() for substring in substrings):
                        file_path_pdf = os.path.join(root, file)
            caminhos = [pasta, file_path_tomados, file_path_entrada, file_path_pdf]

            lista_caminhos.append(caminhos)
        print('lista caminhos', lista_caminhos)
        return lista_caminhos

    def lertomadostxt(self, caminhoT):
        print(f'tomados {caminhoT}')
        def organizerdf(df1, df2):
            for indice, linha in df2.iterrows():
                numero_correspondente = linha['Número']
                
                # Localizar a linha no DataFrame principal com o número correspondente
                indice_inserir = df1[df1['Número'] == numero_correspondente].index[0]
                
                # Inserir a linha do DataFrame secundário na linha seguinte ao DataFrame principal
                df1 = pd.concat([df1.loc[:indice_inserir], linha.to_frame().transpose(), df1.loc[indice_inserir+1:]]).reset_index(drop=True)
            return df1
        
        with open(caminhoT, 'r') as txttomados:
            dados = txttomados.read().replace(',', '').replace('.', '')
        
        # r'-{13}.*?-{13}'  - oque sera removido  {13} quantidade . qualquer caracter * zero ou mais aparicoes ? pega sempre as primeiras aparicoes// re.DOTALL o . detecta a quebra de linha
        linhas_organizadas = re.sub(r'\n {30}', '', dados, flags=re.DOTALL).split('\n')
        linhas_selecionadas = []

        padrao_regex = re.compile(r'empresa(.*?)folha', re.DOTALL | re.IGNORECASE)
        empresa = padrao_regex.search(dados).group(0).replace('Folha', '').strip()
        #linhas_selecionadas.append(empresa)

        padrao_regex = r"\|\s\d+\|\s\w\w\w"
        for linha in linhas_organizadas:
            if re.search(padrao_regex, linha):
                linhas_selecionadas.append(linha)

        if not linhas_selecionadas:
            dadosF = pd.DataFrame(columns=['Data', 'Número', 'Valor', 'CNPJ/CPF', 'Tipo'])
            return dadosF, empresa.replace(':', '').replace('empresa', '').strip()
        
        linhas_selecionadas =  '\n'.join(linhas_selecionadas)
        dados_io = StringIO(linhas_selecionadas)
        dadosF = pd.read_csv(dados_io, sep='|', header=None, dtype=str)
        dadosF.columns= ['zero', 'Data', 'dois', 'tres', 'Número', 'Valor' , 'seis', 'sete', 'oito', 'ISS Retido', 'CNPJ/CPF', 'onze', '12', '13']
        dadosF = dadosF[['Data', 'Número', 'Valor' , 'ISS Retido', 'CNPJ/CPF']]
        dadosF['ISS Retido'] = dadosF['ISS Retido'].astype(int)
        dfiss = dadosF[dadosF['ISS Retido'] > 0].copy()
        if not dfiss.empty:
            dfiss['Tipo'] = 'ISS'
            dfiss = dfiss[['Data', 'Número', 'ISS Retido', 'CNPJ/CPF', 'Tipo']].reset_index(drop=True)
            dfiss.rename(columns={'ISS Retido': 'Valor'}, inplace=True)

        dadosF['Tipo'] = 'Total'
        dadosF = dadosF[['Data', 'Número', 'Valor', 'CNPJ/CPF', 'Tipo']]
        dadosF = organizerdf(dadosF, dfiss)

        linha_cabecalho = pd.DataFrame({'Data': [empresa], 'Número': ['00'], 'Valor': ['00'], 'CNPJ/CPF': ['00'], 'Tipo': ['00']})
        dadosF = pd.concat([linha_cabecalho, dadosF], ignore_index=True)

        return dadosF, empresa.replace(':', '').replace('empresa', '').strip()

    def lerentradatxt(self, caminhoE):
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
        dadosF.columns= ['Data', 'Número', 'CNPJ/CPF', 'Valor', 'Nome']
        dadosF['Data'] = pd.to_datetime(dadosF['Data'], format='%d/%m/%Y')
        dadosF['Data'] = dadosF['Data'].dt.day
        dadosF['CNPJ/CPF'] = dadosF['CNPJ/CPF'].astype(str).replace('/', '', regex=True)
        dadosF['Nome'] = dadosF['Nome'].apply(lambda x: re.sub(r'\d{5,}', '', x))
        return dadosF

    def lerpdf(self, caminho):
        print('pdf', caminho)
        def verifica_tipo_pdf():
            with open(caminho, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
            if 'S E M     M O V I M E N T O' in text:
                return 'Tipo 3'
            elif 'Notas Fiscais de Serviços' in text:
                return 'Tipo 2'
            elif 'Notas de Entradas de Serviços' in text:
                return 'Tipo 1'
            else:
                return 'Tipo não identificado'
            
        tipo = verifica_tipo_pdf()
        
        if 'Tipo 3' == tipo:
            dfFINAL = pd.DataFrame(columns=['Data',	'Número',	'CNPJ/CPF',	'Tipo',	'Valor'])
            return dfFINAL
        elif tipo == 'Tipo 1':
            # Specify the area coordinates (left, top, right, bottom) for extraction
            area = [120.285,12.375,573.705,765.765]

            df_list = tabula.read_pdf(caminho, pages=1, area=area,lattice=True)

            tabela = pd.concat(df_list, ignore_index=True)
            # Print the extracted data
            
            tabela.rename(columns={'Seg\rSocial': 'ValorSS'}, inplace=True)
            tabela.rename(columns={'Unnamed: 0': 'Data'}, inplace=True)
            tabelaF = tabela[['Data', 'Número', 'CNPJ/CPF', 'PIS Retido',  'COFINS Retida', 'CSLL retida', 'IRRF', 'ValorSS']]
            tabelaF = tabelaF.replace(r'\r', ' ', regex=True)
            tabelaF = tabelaF.replace(r',', '', regex=True)
            tabelaF = tabelaF.replace(r'.', '')
            tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']] = tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].apply(lambda x: x.str.split())
            tabelaF['PIS Retido'] =tabelaF['PIS Retido'].apply(lambda x: x[0])
            tabelaF['COFINS Retida'] =tabelaF['COFINS Retida'].apply(lambda x: x[0])
            tabelaF['CSLL retida'] =tabelaF['CSLL retida'].apply(lambda x: x[0])
            tabelaF['CNPJ/CPF'] = tabelaF['CNPJ/CPF'].str.replace(r'[^\d]', '', regex=True)
            tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']] =tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].apply(lambda x: pd.to_numeric(x))
            tabelaF['Valor'] = tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].sum(axis=1)
            tabelaF['IRRF'] = tabelaF['IRRF'].astype(int)
            tabelaF['ValorSS'] = tabelaF['ValorSS'].astype(int)
            tabelaF['Data'] = pd.to_datetime(tabelaF['Data'], format='%d/%m/%Y')
            tabelaF['Data'] = tabelaF['Data'].dt.day.astype(str)
            dadosIRRF = tabelaF[tabelaF['IRRF']>0].copy()
            dadosIRRF['Tipo'] = 'IRRF'
            dadosIRRF = dadosIRRF[['Data', 'Número', 'CNPJ/CPF', 'Tipo', 'IRRF',]].reset_index(drop=True)
            dadosIRRF.rename(columns={'IRRF': 'Valor'}, inplace=True)
            dadosRS = tabelaF.copy()
            dadosRS['Tipo'] = 'Retencao Social'
            dadosRS = dadosRS[['Data', 'Número', 'CNPJ/CPF', 'Tipo', 'Valor',]].reset_index(drop=True)
            dadosINSS = tabelaF[tabelaF['ValorSS']>0].copy()
            dadosINSS['Tipo'] = 'INSS'
            dadosINSS = dadosINSS[['Data', 'Número', 'CNPJ/CPF', 'Tipo', 'ValorSS']].reset_index(drop=True)
            dadosINSS.rename(columns={'ValorSS': 'Valor'}, inplace=True)
            dfFINAL = pd.concat([dadosRS, dadosIRRF, dadosINSS], ignore_index=True)
            dfFINAL['Número'] = dfFINAL['Número'].astype(str).str.zfill(10)
        elif tipo == 'Tipo 2':
            area = [123.672,31.476,562.523,779.733]

            df_list = tabula.read_pdf(caminho, pages=1, area=area,lattice=True)

            tabela = pd.concat(df_list, ignore_index=True)
            
            print(tabela)
            tabela.columns = ['Data', 'nada', 'Número', 'CNPJ/CPF', 'nada', 'nadaa', 'asdf', 'PIS', 'COFINS', 'CSLL' ,'IRRF', 'INSS']
            tabela = tabela[['Data', 'Número', 'CNPJ/CPF', 'PIS', 'COFINS', 'CSLL' ,'IRRF', 'INSS']]
            tabela = tabela.replace(r'\r', ' ', regex=True)
            tabela = tabela.replace(r',', '', regex=True)
            tabela = tabela.replace(r'.', '')

            tabela[['PIS', 'COFINS', 'CSLL', 'IRRF', 'INSS']] = tabela[['PIS', 'COFINS', 'CSLL', 'IRRF', 'INSS']].apply(lambda x: x.str.split())
            tabela['PIS'] = tabela['PIS'].apply(lambda x: x[0])
            tabela['COFINS'] = tabela['COFINS'].apply(lambda x: x[0])
            tabela['CSLL'] = tabela['CSLL'].apply(lambda x: x[0])
            tabela['IRRF'] = tabela['IRRF'].apply(lambda x: x[0])
            tabela['INSS'] = tabela['INSS'].apply(lambda x: x[0])
            tabela[['PIS', 'COFINS', 'CSLL', 'IRRF', 'INSS']] = tabela[['PIS', 'COFINS', 'CSLL', 'IRRF', 'INSS']].apply(lambda x: pd.to_numeric(x))
            tabela['SOCIAL'] = tabela[['PIS', 'COFINS', 'CSLL']].sum(axis=1)
            tabela.drop(columns=['PIS', 'COFINS', 'CSLL'], inplace=True)
            tabelaINSS = tabela[tabela['INSS']> 0 ].copy()
            tabelaINSS.rename(columns={'INSS': 'Valor'}, inplace=True)
            if not tabelaINSS.empty:
                tabelaINSS['Tipo'] = 'INSS'
            tabelaIRRF = tabela[tabela['IRRF']> 0 ].copy()
            tabelaIRRF.rename(columns={'IRRF': 'Valor'}, inplace=True)
            if not tabelaIRRF.empty:
                tabelaIRRF['Tipo'] = 'IRRF'
            tabelaSOCIAL = tabela[tabela['SOCIAL'] > 0 ].copy()
            tabelaSOCIAL.rename(columns={'SOCIAL': 'Valor'}, inplace=True)
            if not tabelaSOCIAL.empty:
                tabelaSOCIAL['Tipo'] = 'Retencao Social'
            dfFINAL = pd.concat([tabelaIRRF, tabelaSOCIAL, tabelaINSS])
            dfFINAL.drop(columns=['IRRF', 'INSS', 'SOCIAL'], inplace=True)
            dfFINAL['CNPJ/CPF'] = dfFINAL['CNPJ/CPF'].str.replace(r'[-./]', '', regex=True)
            dfFINAL['Número'] = dfFINAL['Número'].astype(str).str.zfill(10)
        else:
            return 'faill'
        
        return dfFINAL

    def juntartomadospdf(self, df1, dfpdf):
        for index, row in dfpdf.iterrows():
            numero_atual = row['Número']
            cnpj_atual = row['CNPJ/CPF']
            # Encontrar o índice da linha correspondente no df1
            idx_df1 = df1[(df1['Número'] == numero_atual)  & (df1['CNPJ/CPF'] == cnpj_atual)].index
            # Inserir a linha do dfpdf abaixo da linha correspondente no df1
            if not idx_df1.empty:
                idx_df1 = idx_df1[0]  # Usar o primeiro índice se houver mais de um
                df1 = pd.concat([df1.iloc[:idx_df1 + 1], pd.DataFrame(row).T, df1.iloc[idx_df1 + 1:]]).reset_index(drop=True)
            else:
                df1 = pd.concat([df1, pd.DataFrame(row).T]).reset_index(drop=True)
        return df1

    def pradronizarxl(self, localsalvar):
        for arq in os.listdir(localsalvar):
            # Carregar o arquivo Excel
            workbook = openpyxl.load_workbook(f'{localsalvar}/{arq}')

            # Selecionar a planilha desejada (substitua 'Sheet1' pelo nome da sua planilha)
            sheet = workbook['Sheet1']

            # Definir o tamanho da coluna A para 20 (substitua 'A' pelo identificador da sua coluna)
            sheet.column_dimensions['A'].width = 5
            sheet.column_dimensions['B'].width = 18
            sheet.column_dimensions['C'].width = 18
            sheet.column_dimensions['D'].width = 5
            sheet.column_dimensions['E'].width = 12
            sheet.column_dimensions['F'].width = 11.14
            sheet.column_dimensions['G'].width = 6
            sheet.column_dimensions['H'].width = 85

            #Salvar as alterações no arquivo
            workbook.save(f'{localsalvar}/{arq}')

    def lerbanco(self):
        dfbanco = pd.read_excel('BANCOCNPJ.xlsx')
        dfbanco.columns = ('CNPJ/CPF', 'Nome')
        dfbanco['CNPJ/CPF'] = dfbanco['CNPJ/CPF'].apply(lambda x: str(x).zfill(14))
        mapa_cnpj_nome = dict(zip(dfbanco['CNPJ/CPF'], dfbanco['Nome']))
        return mapa_cnpj_nome


    def alterarnome(self, df1):
        df1['NF Nome'] = 'NF '+ df1['Número'].fillna('').astype(str) + ' ' + df1['Nome'].fillna('')
        
        def adicionar_texto(row):
            if row['Tipo'] == 'IRRF':
                return 'IRRF RETIDO CF. ' + row['NF Nome']
            elif row['Tipo'] == 'Retencao Social':
                return 'RETENÇÃO SOCIAL CF. ' + row['NF Nome']
            elif row['Tipo'] == 'INSS':
                return 'INSS RETIDO CF. ' + row['NF Nome']
            elif row['Tipo'] == 'ISS':
                return 'ISS RETIDO CF. ' + row['NF Nome']
            else:
                return row['NF Nome']

        df1['NF Nome'] = df1.apply(adicionar_texto, axis=1)
        df1['NF Nome'] = df1['NF Nome'].replace('NF 00 ', '')
        df1 = df1.drop(columns=['Nome'])
        return df1
    
    def salvar_junto(self, df, localsalvar):
        tudo = pd.read_excel(f'{localsalvar}/TUDO.xlsx')
        linha_vazia = pd.DataFrame({'Data': [''], 'Número': [''], 'Valor': [''], 'CNPJ/CPF': ['']})
        fim = pd.concat([tudo, linha_vazia,linha_vazia, df]).reset_index(drop=True)
        fim.to_excel(f'{localsalvar}/TUDO.xlsx', index=False)

    def salvar_em_excel(self, df, nome_arquivo, localsalvar):
        df = df.drop(0)
        # Obtendo o mês e o ano
        mes, ano = self.pegardata()
        df['Ano'] = ano
        df['Mês'] = mes
        df['Dia'] = df['Data']
        df['Data'] = df['Dia'].astype(str) + '/' + df['Mês'].astype(str) + '/' + df['Ano'].astype(str)
        df['Data'] = df['Data'].str.strip()
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y', errors='coerce').dt.strftime('%d/%m/%Y')
        # Removendo as colunas de ano, mês e dia após criar a coluna de data
        df = df.drop(['Dia', 'Mês', 'Ano'], axis=1)
        # Salva o DataFrame em um arquivo Excel
        df['Vazia1'] = ''
        df['Vazia2'] = ''
        df['Vazia3'] = ''
        df['Vazia4'] = ''
        df['Vazia5'] = ''
        df['Valor'] = df['Valor'].astype(float).astype(int)
        df = df[['Vazia1','Vazia2','Vazia3', 'Vazia4', 'Valor', 'Data', 'Vazia5', 'NF Nome']]
        df.to_excel(f'{localsalvar}/{nome_arquivo}', index=False, header=False)
        self.printarInformacoes(f'DataFrame salvo em "{nome_arquivo}".')

    def lerarquivos(self, pasta,Ctomados, Centrada, Cpdf):
        dftomados, dfentrada, dfpdf = pd.DataFrame(columns=['Data', 'Número', 'CNPJ/CPF', 'Valor', 'Nome']), pd.DataFrame(columns=['Data', 'Número', 'CNPJ/CPF', 'Valor', 'Nome']), pd.DataFrame(columns=['Data', 'Número', 'CNPJ/CPF', 'Valor', 'Nome'])
        empresa = pasta
        if Ctomados:
            dftomados, empresa = self.lertomadostxt(Ctomados)
        if Centrada:
            dfentrada = self.lerentradatxt(Centrada)
        if Cpdf:
            dfpdf = self.lerpdf(Cpdf)

        if not dfpdf.empty:
            dftomados = self.juntartomadospdf(dftomados, dfpdf)

        if dftomados.empty:
            print(f'sem movimento empresa: {empresa}')
            return empresa, dftomados, dfpdf, dfentrada, False
        
        dftomados['Nome'] = dftomados['CNPJ/CPF'].map(self.banco)
        #terminiar leitura do banco e o resto embaixo (resolver juntar df tomados e dfentrada com linha vazia)

        if not dfentrada.empty:
            linha_vazia = pd.DataFrame({'Data': ['00'], 'Número': ['00'], 'Valor': ['00'], 'CNPJ/CPF': ['']})
            dftomados = pd.concat([dftomados, linha_vazia, dfentrada]).reset_index(drop=True)
            
        dftomados['Número'] = dftomados['Número'].astype(float).astype(int).apply(lambda x: f'{x:02}')
        dftomados = self.alterarnome(dftomados)
        dftomados['Vazia1'] = ''
        dftomados['Vazia2'] = ''        
        return empresa, dftomados, dfpdf, dfentrada, True

    def pegarCNPJS(self):
        def attbanco(df, banco):
            for index, row in df.iterrows():
                cnpj = row['CNPJ/CPF']
                nome = row['Nome']
        # Verifica se o CNPJ já está no dicionário
                if cnpj not in banco:
                    banco[cnpj] = nome
                    df_resultado = pd.DataFrame(list(banco.items()), columns=['CNPJ', 'Nome'])
                    df_resultado['CNPJ'] = df_resultado['CNPJ'].astype(float)
                    df_resultado.to_excel('BANCOCNPJ.xlsx', index=False)

        dfentradaCNPJ = pd.DataFrame()
        dftomadosCNPJ = pd.DataFrame()
        for pasta, Ctomados, Centrada, Cpdf in self.caminhos:
            empresa, dftomados, dfpdf, dfentrada, cond = self.lerarquivos(pasta, Ctomados, Centrada, Cpdf)
            dfentradaCNPJ = pd.concat([dfentradaCNPJ, dfentrada[['CNPJ/CPF', 'Nome']]]).reset_index(drop=True)
            dftomadosCNPJ =  pd.concat([dftomadosCNPJ, dftomados[['CNPJ/CPF']]])

        attbanco(dfentradaCNPJ, self.banco)
        self.banco = self.lerbanco()
        dftomadosCNPJ = dftomadosCNPJ[(dftomadosCNPJ['CNPJ/CPF'] != '00') & (dftomadosCNPJ['CNPJ/CPF'] != '')]
        dftomadosCNPJ = dftomadosCNPJ.drop_duplicates('CNPJ/CPF')
        dftomadosCNPJ['Nome'] = dftomadosCNPJ['CNPJ/CPF'].map(self.banco)
        dftomadosCNPJ.columns = ['CNPJ', 'Nome']
        dftomadosCNPJ = dftomadosCNPJ[dftomadosCNPJ['Nome'].isna()][['CNPJ', 'Nome']].reset_index(drop=True)
        return dftomadosCNPJ

    def atualizarBANCOCNPJ(self, dfCNPJS):
        dfbanco = pd.read_excel('BANCOCNPJ.xlsx')
        dfbanco = pd.concat([dfbanco, dfCNPJS], ignore_index=True)
        dfbanco.to_excel('BANCOCNPJ.xlsx', index=False)

    def gerarNotas(self):
        self.printarInformacoes('LIMPAR')
        self.criar_pasta()
        for i in self.caminhos:
            pasta, Ctomados, Centrada, Cpdf = i
            empresa, dftomados, dfpdf, dfentrada, cond = self.lerarquivos(pasta, Ctomados, Centrada, Cpdf)
            if cond:
                self.salvar_junto(dftomados[['Data', 'Número', 'CNPJ/CPF' , 'Vazia1', 'Vazia2','Valor', 'NF Nome', 'Tipo']], self.local_salvar)
                self.salvar_em_excel(dftomados[[ 'Valor', 'Data', 'NF Nome', 'CNPJ/CPF']], f'{empresa}.xlsx', self.local_salvar)
                self.pradronizarxl(self.local_salvar)
                self.printarInformacoes('################################################')
            else:
                continue
        self.printarInformacoes('############### COMPLETOU NOTAS ###################')

class NotasUI(Notas):
    def __init__(self, local, local_salvar, txt_tomados, txt_entrada, ui):
        super().__init__(local, local_salvar, txt_tomados, txt_entrada)
        self.ui = ui

    def printarInformacoes(self, conteudo):
        self.ui.printNotas(conteudo)

    def tabelaCNPJ(self, df):
        self.ui.preencher_tabela(df)

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

if __name__ == "__main__": 
    base_directory = r'C:/Users/Alexandre/Desktop/drive-download-20240611T173809Z-001/LBR'
    saida = "C:/Users/Alexandre/Desktop/Nova pasta (2)"
    txtentrada = 'E052024.txt'
    txttomados = 'I56052024.txt'

    notas = Notas(base_directory,  saida,txttomados, txtentrada)
    #preciso terminas de colocar no UI agora , ele precisa das mesma coisa o local de salvar o local dos arquivos e os dois nomes dos arquivos