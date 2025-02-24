import pandas as pd
import re
from openpyxl import load_workbook
import os

class RAZAO_DFC:
    def __init__(self, local, locals, list_contra) -> None:
        self.local = local
        self.locals = locals
        self.contras = list_contra

    def resumir(self):
        if os.path.isfile(self.local):
            nome = os.path.splitext(os.path.basename(self.local))[0]
            diretorio = os.path.dirname(self.local)
            return self.gerar_dfc(diretorio, self.locals, nome)


        elif os.path.isdir(self.local):
            lista = os.listdir(self.local)
            for arquivo in lista:
                if arquivo.endswith('.txt'):
                    arq = os.path.splitext(arquivo)[0]
                    self.gerar_dfc(self.local, self.locals, arq)
            else:
                return True

    def printar(self, conteudo):
        print(conteudo)

    def gerar_dfc(self, local, locals, nomearq):
        with open(f"{local}/{nomearq}.txt", "r") as arquivo:
            dados = arquivo.read()

        padrao_cabecalho = re.compile(r'LUIZA ASSESSORIA CONTABIL LTDA                    .*?Saldo', re.DOTALL)

        # Substituir o cabeçalho por uma string vazia
        texto_sem_cabecalho = re.sub(padrao_cabecalho, '', dados)
        padrao_cabecalho = re.compile(r'-{131}', re.DOTALL)
        texto_sem_cabecalho = re.sub(padrao_cabecalho, '', texto_sem_cabecalho)
        padrao_cabecalho = re.compile(r'-{88}', re.DOTALL)
        texto_sem_cabecalho = re.sub(padrao_cabecalho, '', texto_sem_cabecalho)
        padrao_cabecalho = re.compile(r'-{50}', re.DOTALL)
        texto_sem_cabecalho = re.sub(padrao_cabecalho, '', texto_sem_cabecalho)
        texto_sem_cabecalho = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x9F]', '', texto_sem_cabecalho)
        texto_sem_cabecalho = texto_sem_cabecalho.split('\n')

        df = pd.DataFrame(columns=['Data', 'lanca', 'contra','nome','debito', 'credito', 'saldo'])
        anterior = 1

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Saldo do Mes:' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Saldo Atual:' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Saldo Anterior:' in linha:
                if anterior == 1:
                    anterior = linha
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Saldo Geral:' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Sem Movimento' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Conta Custo' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Conta Analisada:' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if 'Data    Lançamento Contrapartida' in linha:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if '' == linha.strip:
                texto_sem_cabecalho.pop(e)

        for e, linha in enumerate(texto_sem_cabecalho):
            if '' == linha:
                texto_sem_cabecalho.pop(e)

        texto_sem_cabecalho = [linha for linha in texto_sem_cabecalho if not linha.isspace()]

        linhas_organizadas = re.sub(r'\n {44}', '', '\n'.join(texto_sem_cabecalho), flags=re.DOTALL)
        linhas_organizadas = linhas_organizadas.split('\n')


        for e, linha in enumerate(linhas_organizadas):
            if len(linha.split()) < 4:
                linhas_organizadas.pop(e)

        for linha in linhas_organizadas:
            linha_32 = linha[:33].strip().split()
            data = linha_32[0]
            lanca = linha_32[1]
            contra = linha_32[2]
            linha_49 = linha[-53:].replace('C', ' ').replace('D', ' ')
            if any(char.isalpha() for char in linha_49):
                debito =  ''
                credito = ''
                saldo = ''
                nome = linha[33:].strip()
            else:
                debito =  linha_49[:16].strip().replace('.', '').replace(',', '')
                credito = linha_49[16:33].strip().replace('.', '').replace(',', '')
                saldo = linha_49[33:53].strip().replace('.', '').replace(',', '')
                nome = linha[33:-49].strip()
            
            df = pd.concat([df,pd.DataFrame([{'Data': data, 'lanca': lanca, 'contra': contra,'nome': nome,'debito': debito, 'credito': credito, 'saldo': saldo}])], ignore_index=True)



        df = df.fillna(0)
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')
        df['debito'] = pd.to_numeric(df['debito']) 
        df['contra'] = pd.to_numeric(df['contra'])  
        df['credito'] = pd.to_numeric(df['credito'])  
        df['saldo'] = pd.to_numeric(df['saldo']) 
        df = df.fillna(0)

        df['contra'] = df['contra']


        df['debito'] = df['debito'].apply(lambda x: float('{:.2f}'.format(x / 100)))
        df['credito'] = df['credito'].apply(lambda x: float('{:.2f}'.format(x / 100)))
        df['saldo'] = df['saldo'].apply(lambda x: float('{:.2f}'.format(x / 100)))

        dffiltrado = df[df['contra'].isin(self.contras)]

        dffiltrado = dffiltrado.sort_values(by='Data')
        dffiltrado['Data'] = dffiltrado['Data'].dt.strftime('%d/%m/%Y').copy()

        dffiltrado.to_excel(f'{locals}/{nomearq}.xlsx', index=False)
        self.printar(f'Aquivo gerado: {nomearq}.xlsx')
        return True
    
class RAZAO_DFCui(RAZAO_DFC):
    def __init__(self, local, locals, list_contra, ui):
        super().__init__(local, locals, list_contra)
        self.ui = ui

    def printar(self, conteudo):
        self.ui.printRAZAO(conteudo)