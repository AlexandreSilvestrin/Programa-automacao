import os
import pandas as pd
import openpyxl
from unidecode import unidecode
import warnings
from core.NOTAS_tomados import gerartomados
from core.NOTAS_entrada import gerarentrada
from core.NOTAS_pdf import gerarpdf
from models.banco_cnpj import CNPJModel


warnings.filterwarnings("ignore", category=FutureWarning, message="errors='ignore' is deprecated")

class Notas:
    def __init__(self, local, local_salvar, mes, ano):
        self.local = local
        self.local_salvar = local_salvar
        self.txtTomados = f'I56{mes}{ano}.txt'
        self.txtEntrada = f'E{mes}{ano}.txt'
        self.caminhos = self.listarcaminhos()
        self.data = mes, ano
        self.banco = CNPJModel.banco_to_dict()

    def printarInformacoes(self, conteudo):
        print(conteudo)

    def criar_pasta(self):
        ultimo_diretorio = os.path.basename(self.local)
        os.makedirs(f'{self.local_salvar}/{ultimo_diretorio}/NOTAS', exist_ok=True)
        self.local_salvar = f'{self.local_salvar}/{ultimo_diretorio}/NOTAS'

    def pradronizarxl(self, localsalvar):
        for arq in os.listdir(localsalvar):
            # Carregar o arquivo Excel
            if arq.endswith('.xlsx'):
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

    def alterarnome(self, df1):
        df1['NF Nome'] = 'NF '+ df1['Número'].fillna('').astype(str) + ' ' + df1['Nome'].fillna('')
        
        def adicionar_texto(row):
            if row['Tipo'] == 'IRRF':
                return 'IR RETIDO CF. ' + row['NF Nome']
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

    def listarcaminhos(self):
        substrings = ['retencoes', 'retencao', 'Retençao', 'Retenção']
        lista_caminhos = []
        for pasta in os.listdir(self.local):
            file_path_entrada, file_path_tomados, file_path_pdf = False, False, False

            for root, dirs, files in os.walk(f'{self.local}/{pasta}'):
                for file in files:
                    if file in self.txtEntrada:
                        file_path_entrada = os.path.join(root, file)
                    if file in self.txtTomados:
                        file_path_tomados = os.path.join(root, file)
            
                for root, dirs, files in os.walk(os.path.join(self.local, pasta)):
                    if 'tomados' in root.lower():
                        for file in files:
                            if any(substring in unidecode(file).lower() for substring in substrings):
                                file_path_pdf = os.path.join(root, file)

        
            caminhos = [pasta, file_path_tomados, file_path_entrada, file_path_pdf]
            lista_caminhos.append(caminhos)
            print(caminhos, '\n')

        return lista_caminhos
    
    def juntartomadospdf(self, df1, dfpdf):
        for index, row in dfpdf.iterrows():
            numero_atual = row['Número']
            cnpj_atual = row['CNPJ']
            # Encontrar o índice da linha correspondente no df1
            idx_df1 = df1[(df1['Número'] == numero_atual)  & (df1['CNPJ'] == cnpj_atual)].index
            # Inserir a linha do dfpdf abaixo da linha correspondente no df1
            if not idx_df1.empty:
                idx_df1 = idx_df1[0]  # Usar o primeiro índice se houver mais de um
                df1 = pd.concat([df1.iloc[:idx_df1 + 1], pd.DataFrame(row).T, df1.iloc[idx_df1 + 1:]]).reset_index(drop=True)
            else:
                df1 = pd.concat([df1, pd.DataFrame(row).T]).reset_index(drop=True)
        return df1

    def salvar_em_excel(self, df, nome_arquivo, localsalvar):
        # Obtendo o mês e o ano
        mes, ano = self.data
        df = df.copy()
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

    def salvarerro(self, dferro, empresa):
        erro = dferro['erro']
        erroF = dferro['erroF']
        info = dferro['info']
        arq = dferro['arquivo']
        with open(f"{self.local_salvar}/ERRO_{empresa}_{arq}.txt", "w") as arq:
            arq.write(f'{info}\n Arquivo: {arq}\n\n TRACEBACK:\n{erroF}')
        self.printarInformacoes(info)

    def pegarCNPJS(self):
        self.printarInformacoes('LIMPAR')

        dfentradaCNPJ = pd.DataFrame()
        dftomadosCNPJ = pd.DataFrame()
        for pasta, Ctomados, Centrada, Cpdf in self.caminhos:
            empresa, dftomados, dfpdf, dfentrada, cond = self.lerarquivos(pasta, Ctomados, Centrada, Cpdf)
            if cond:
                dfentradaCNPJ = pd.concat([dfentradaCNPJ, dfentrada[['CNPJ', 'Nome']]]).reset_index(drop=True)
                dftomadosCNPJ =  pd.concat([dftomadosCNPJ, dftomados[['CNPJ']]])

        CNPJModel.add_new_data(dfentradaCNPJ)
        self.banco = CNPJModel.banco_to_dict()

        dftomadosCNPJ = dftomadosCNPJ[(dftomadosCNPJ['CNPJ'] != '00') & (dftomadosCNPJ['CNPJ'] != '')]
        dftomadosCNPJ = dftomadosCNPJ.drop_duplicates('CNPJ')
        dftomadosCNPJ['Nome'] = dftomadosCNPJ['CNPJ'].map(self.banco)
        dftomadosCNPJ.columns = ['CNPJ', 'Nome']
        dftomadosCNPJ = dftomadosCNPJ[dftomadosCNPJ['Nome'].isna()][['CNPJ', 'Nome']].reset_index(drop=True)
        return dftomadosCNPJ

    def lerarquivos(self, pasta,Ctomados, Centrada, Cpdf):
        print(pasta)
        dftomados, dfentrada, dfpdf = pd.DataFrame(columns=['Data', 'Número', 'CNPJ', 'Valor', 'Nome']), pd.DataFrame(columns=['Data', 'Número', 'CNPJ', 'Valor', 'Nome']), pd.DataFrame(columns=['Data', 'Número', 'CNPJ', 'Valor', 'Nome'])
        empresa = pasta
        if Ctomados:
            dftomados = gerartomados(Ctomados)
            if dftomados['df'] is None:
                self.salvarerro(dftomados, empresa)
                return empresa, dftomados, dfpdf, dfentrada, False
            elif isinstance(dftomados['df'], pd.DataFrame):
                dftomados = dftomados['df']
            elif dftomados['df'] == 'SEM MOVIMENTO':
                self.printarInformacoes(f'''{empresa} SEM MOVIMENTO''')
                dftomados = pd.DataFrame()

        if Centrada:
            dfentrada = gerarentrada(Centrada)
            if dfentrada['df'] is None:
                self.salvarerro(dfentrada, empresa)
                return empresa, dftomados, dfpdf, dfentrada, False
            else:
                dfentrada =dfentrada['df']
        if Cpdf:
            dfpdf = gerarpdf(Cpdf)
            if dfpdf['df'] is None:
                self.salvarerro(dfpdf, empresa)
                return empresa, dftomados, dfpdf, dfentrada, False
            else:
                dfpdf = dfpdf['df']

        if not dfpdf.empty:
            dftomados = self.juntartomadospdf(dftomados, dfpdf)

        if dftomados.empty:
            return empresa, dftomados, dfpdf, dfentrada, False
        
        dftomados['Nome'] = dftomados['CNPJ'].map(self.banco)
        #terminiar leitura do banco e o resto embaixo (resolver juntar df tomados e dfentrada com linha vazia)
    
        if not dfentrada.empty:
            linha_vazia = pd.DataFrame({'Data': ['00'], 'Número': ['00'], 'Valor': ['00'], 'CNPJ': ['']})
            dftomados = pd.concat([dftomados, linha_vazia, dfentrada]).reset_index(drop=True)
            
        dftomados['Número'] = dftomados['Número'].astype(float).astype(int).apply(lambda x: f'{x:02}')
        dftomados = self.alterarnome(dftomados)
        dftomados['Vazia1'] = ''
        dftomados['Vazia2'] = ''        
        return empresa, dftomados, dfpdf, dfentrada, True

    def gerarNotas(self):
        self.printarInformacoes('LIMPAR')
        self.criar_pasta()
        for i in self.caminhos:
            pasta, Ctomados, Centrada, Cpdf = i
            empresa, dftomados, dfpdf, dfentrada, cond = self.lerarquivos(pasta, Ctomados, Centrada, Cpdf)
            if empresa:
                if cond:
                    self.salvar_em_excel(dftomados[[ 'Valor', 'Data', 'NF Nome', 'CNPJ']], f'{empresa}.xlsx', self.local_salvar)
                else:
                    self.printarInformacoes(f'''{empresa} SEM MOVIMENTO''')
        self.pradronizarxl(self.local_salvar)
        self.printarInformacoes(f'completou Notas')

class NotasUI(Notas):
    def __init__(self, local, local_salvar, mes, ano, ui):
        super().__init__(local, local_salvar, mes, ano)
        self.ui = ui

    def printarInformacoes(self, conteudo):
        self.ui.printNotas(conteudo)

    def tabelaCNPJ(self, df):
        self.ui.preencher_tabela(df)



if __name__ == "__main__": 
    base_directory = r'C:/Users/Alexandre/Downloads/drive-download-20250610T175842Z-1-001/PLANSERVI'
    saida = "C:/Users/Alexandre/Desktop/Nova pasta (2)"
    mes = '05'
    ano = '2025'

    notas = Notas(base_directory,  saida, mes, ano)
    #preciso terminas de colocar no UI agora , ele precisa das mesma coisa o local de salvar o local dos arquivos e os dois nomes dos arquivos