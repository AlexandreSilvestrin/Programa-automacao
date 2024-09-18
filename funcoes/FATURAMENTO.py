import re
import pandas as pd
import openpyxl
import os


class Faturamento:
    def __init__(self, caminho, caminhoSalvar, txtPrestados):
        self.caminho = caminho
        self.caminhoS = caminhoSalvar
        self.txtP = txtPrestados
        self.caminhosFat, self.pastaP = self.encontrar_arquivo(caminho, txtPrestados)

    def criar_pasta(self):
        ultimo_diretorio = os.path.basename(self.caminho)
        os.makedirs(f'{self.caminhoS}/{ultimo_diretorio}/FATURAMENTO', exist_ok=True)
        self.caminhoS = f'{self.caminhoS}/{ultimo_diretorio}/FATURAMENTO'

    def printarInformacoes(self, conteudo):
        print(conteudo)

    def encontrar_arquivo(self, caminho, txtPrestados, nome_pasta='prestados'):
        caminhosFat = []
        for dirpath, dirnames, filenames in os.walk(caminho):
            # Verifica se a pasta "Serv. Prestados" está no caminho atual
            if nome_pasta in dirpath.lower():
                # Verifica se o arquivo desejado está dentro da pasta
                if txtPrestados in filenames:
                    # Retorna o caminho completo do arquivo
                    caminhosFat.append(os.path.join(dirpath, txtPrestados)) 
        return caminhosFat, os.path.basename(os.path.normpath(caminho))

    def pegardata(self):
        nome = self.txtP.replace('.txt', '')
        return nome[-6:-4], nome[-4:]

    def faturamento(self, caminho):
        mes, ano = self.pegardata()

        caminhosalvar = self.caminhoS
        pastaP = self.pastaP

        with open(caminho, 'r') as arq:
            dados = arq.read()

        padrao_cnpj = r'CGC/CNPJ: \d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}'
        cnpj_encontrado = re.search(padrao_cnpj, dados).group().replace('CGC/CNPJ: ', '')

        cnpj = cnpj_encontrado

        dados = dados.replace('\n                                                            ', '')
        dados = dados.replace('\n|   |     |                 |              |                |      |              |              |          I', 'I')

        lista = dados.split('\n')

        listafiltrada= []
        for i in lista:
            padrao = r'\|\d{2}\s\|'
            if re.search(padrao, i):
                listafiltrada.append(i)

        novalista = []
        for e, linha in enumerate(listafiltrada):
            if 'Cancelada' not in linha.strip() and 'Canc.' not in linha.strip():
                novalista.append(linha)

        if not novalista:
            return 'vazio'

        from io import StringIO
        novalista = '\n'.join(novalista)


        lista_io = StringIO(novalista)
        df = pd.read_csv(lista_io, sep = '|', header=None)

        df.columns = ('nada', 'data', 'nada2', 'NF', 'cnpj', 'valorTotal', 'nada3', 'iss pagar', 'iss retido/pagar', 'valorTotal2', 'nada6', 'iss ret', 'nada', 'irrf', 'nada7', 'nada8')
        df['NF'] = pd.to_numeric(df['NF'], errors='coerce')
        df = df.sort_values(by='NF')


        df = df[['data', 'NF', 'valorTotal', 'iss pagar', 'iss retido/pagar', 'valorTotal2', 'irrf']]

        df.loc[:, 'data'] = df['data']
        df.loc[:, 'NF'] = df['NF']
        df.loc[:, 'valorTotal'] = df['valorTotal'].apply(lambda x: int(x.strip().replace('.', '').replace(',', '')))
        df.loc[:, 'iss pagar'] = df['iss pagar'].apply(lambda x: int(x.strip().replace('.', '').replace(',', '')))
        df.loc[:, 'iss retido/pagar'] = df['iss retido/pagar'].apply(lambda x: int(x.strip().replace('.', '').replace(',', '')))
        df.loc[:, 'valorTotal2'] = df['valorTotal2'].apply(lambda x: int(x.strip().replace('.', '').replace(',', '')))
        df.loc[:, 'irrf'] = df['irrf'].apply(lambda x: int(x.strip().replace('.', '').replace(',', '')))


        dfG = pd.read_excel('GUIA NOME.xlsx')
        dfG.dropna(inplace=True)
        dfG['CONTRATO'] = dfG['CONTRATO'].apply(lambda x: x.replace(' ', '').replace('-', '').replace('.', '').strip())
        dfG['RAZÃO SOCIAL'] = dfG['RAZÃO SOCIAL'].apply(lambda x: x.upper())

        linhaG = dfG[dfG['CNPJ DO CONSÓRCIO'] == cnpj.strip()].reset_index( drop=True)
        linhaG = linhaG.iloc[0].to_dict()

        lista = linhaG['PORCENTAGEM POR CONSORCIADA'].replace('%', '').replace(',', '.').split()
        listaP = [lista[i:i + 2] for i in range(0, len(lista), 2)]
        listaP = [[n, int(p)] for n, p in listaP]

        retencao = linhaG['RETENÇÕES'].split(',')
        retencao = [x.strip() for x in retencao]


        listadf = []
        for e, linha in df.iterrows():
            dia , numero, valortotal, iss_pagar, iss_retido_pagar, valortotal2, irrf = linha
            if valortotal > 0:
                valor_total = valortotal
            else:
                valor_total = valortotal2

            linha_total = { 'numero': 1, 'valor': valor_total, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
            listadf.append(linha_total)
            for nome, porcent in listaP:
                linha_total_porcent = {'numero': 1, 'valor': round(int(valor_total)*(porcent/100)), 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {nome}"}
                listadf.append(linha_total_porcent)
            
            pis = round(valor_total*(0.65/100))
            cofins = round(valor_total*(3/100))
            csll = round(valor_total*(1/100))

            for ret in retencao:
                if ret == 'IR':
                    linha_irrf = {'numero': 1, 'valor': irrf, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"IR RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                    listadf.append(linha_irrf)
                    for nome, porcent in listaP:
                        linha_total_porcent = {'numero': 1, 'valor': round(int(irrf)*(porcent/100)), 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"IR RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {nome}"}
                        listadf.append(linha_total_porcent)

                if ret == 'PIS':
                    linha_pis = {'numero': 1, 'valor': pis, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"PIS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                    listadf.append(linha_pis)
                    for nome, porcent in listaP:
                        linha_total_porcent = {'numero': 1, 'valor': round(int(pis)*(porcent/100)), 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"PIS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {nome}"}
                        listadf.append(linha_total_porcent)
                
                if ret == 'COFINS':
                    linha_cofins = {'numero': 1, 'valor': cofins, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"COFINS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                    listadf.append(linha_cofins)
                    for nome, porcent in listaP:
                        linha_total_porcent = {'numero': 1, 'valor': round(int(cofins)*(porcent/100)), 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"COFINS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {nome}"}
                        listadf.append(linha_total_porcent)
                
                if ret == 'CSLL':
                    linha_csll = {'numero': 1, 'valor': csll, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"CSLL RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                    listadf.append(linha_csll)
                    for nome, porcent in listaP:
                        linha_total_porcent = {'numero': 1, 'valor': round(int(csll)*(porcent/100)), 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"CSLL RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {nome}"}
                        listadf.append(linha_total_porcent)

            if iss_pagar >0:
                linha_iss_retido_pagar = {'numero': 1, 'valor': '', 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"ISS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                listadf.append(linha_iss_retido_pagar)
                linha_iss = {'numero': 1, 'valor': iss_pagar, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"ISS A PAGAR CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                listadf.append(linha_iss)
            else:
                linha_iss_retido_pagar = {'numero': 1, 'valor': iss_retido_pagar, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"ISS RETIDO CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                listadf.append(linha_iss_retido_pagar)
                linha_iss = {'numero': 1, 'valor': iss_retido_pagar, 'data': f'{dia}/{mes}/{ano}', 'vazio': '', 'nome': f"ISS A PAGAR CF. NF {numero} PRESTAÇÃO DE SERVIÇO {linhaG['RAZÃO SOCIAL']}- {linhaG['CONTRATO']}"}
                listadf.append(linha_iss)
                
            linha_vazia = {'numero': '', 'valor': '', 'data': '', 'vazio': '', 'nome': ''}
            listadf.append(linha_vazia)
            
        dffinal = pd.DataFrame(listadf)

        dffinal[['a', 'b', 'c']] = ''

        dffinal = dffinal[['a', 'b', 'c', 'numero', 'valor', 'data', 'vazio', 'nome']]

        dffinal.to_excel(f'{caminhosalvar}/{pastaP} FATURAMENTO {mes}.{ano} {linhaG["CONTRATO"]}.xlsx', index=False, header=None)

        self.printarInformacoes(f'FATURAMENTO {mes}.{ano} {linhaG["CONTRATO"]}.xlsx SALVO')
        self.printarInformacoes(f'LOCAL: {caminhosalvar}/{pastaP}')
        self.printarInformacoes('#'*62)

        workbook = openpyxl.load_workbook(f'{caminhosalvar}/{pastaP} FATURAMENTO {mes}.{ano} {linhaG["CONTRATO"]}.xlsx')

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
        workbook.save(f'{caminhosalvar}/{pastaP} FATURAMENTO {mes}.{ano} {linhaG["CONTRATO"]}.xlsx')

    def gerarFat(self):
        self.criar_pasta()
        for caminho in self.caminhosFat:
            print(caminho)
            self.faturamento(caminho)
        self.printarInformacoes('FATURAMENTO COMPLETO')

class FaturamentoUI(Faturamento):
    def __init__(self, caminho, caminhoSalvar, txtPrestados, ui):
        super().__init__(caminho, caminhoSalvar, txtPrestados)
        self.ui = ui

    def printarInformacoes(self, conteudo):
        self.ui.printNotas(conteudo)

if __name__ == "__main__": 
    base_directory = r"C:\Users\Alexandre\Downloads\drive-download-20240910T170737Z-001\LBR"
    saida = r"C:\Users\Alexandre\Desktop\tsets"
    txttomados = 'I51082024.txt'

    notas = Faturamento(base_directory,  saida, txttomados)
    notas.gerarFat()
    #preciso terminas de colocar no UI agora , ele precisa das mesma coisa o local de salvar o local dos arquivos e os dois nomes dos arquivos