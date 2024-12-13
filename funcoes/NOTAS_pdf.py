import tabula
import pandas as pd
import traceback
import PyPDF2

def verifica_tipo_pdf(caminho):
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


def gerarpdf(caminho):
    try:
        tipo = verifica_tipo_pdf(caminho)
        
        if 'Tipo 3' == tipo:
            dfFINAL = pd.DataFrame(columns=['Data',	'Número', 'CNPJ', 'Tipo', 'Valor'])
            return {"df": dfFINAL}
        elif tipo == 'Tipo 1':
            # Specify the area coordinates (left, top, right, bottom) for extraction
            area = [120.285,12.375,573.705,765.765]

            df_list = tabula.read_pdf(caminho, pages=1, area=area,lattice=True)

            tabela = pd.concat(df_list, ignore_index=True)
            # Print the extracted data
            
            tabela.rename(columns={'Seg\rSocial': 'ValorSS'}, inplace=True)
            tabela.rename(columns={'Unnamed: 0': 'Data'}, inplace=True)
            tabelaF = tabela[['Data', 'Número', 'CNPJ/CPF', 'PIS Retido',  'COFINS Retida', 'CSLL retida', 'IRRF', 'ValorSS']].copy()
            tabelaF.rename(columns={'CNPJ/CPF': "CNPJ"}, inplace=True)
            tabelaF = tabelaF.replace(r'\r', ' ', regex=True)
            tabelaF = tabelaF.replace(r',', '', regex=True)
            tabelaF = tabelaF.replace(r'.', '')
            tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']] = tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].apply(lambda x: x.str.split())
            tabelaF['PIS Retido'] =tabelaF['PIS Retido'].apply(lambda x: x[0])
            tabelaF['COFINS Retida'] =tabelaF['COFINS Retida'].apply(lambda x: x[0])
            tabelaF['CSLL retida'] =tabelaF['CSLL retida'].apply(lambda x: x[0])
            tabelaF['CNPJ'] = tabelaF['CNPJ'].str.replace(r'[^\d]', '', regex=True)
            tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']] =tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].apply(lambda x: pd.to_numeric(x))
            tabelaF['Valor'] = tabelaF[['PIS Retido', 'COFINS Retida', 'CSLL retida']].sum(axis=1)
            tabelaF['IRRF'] = tabelaF['IRRF'].astype(int)
            tabelaF['ValorSS'] = tabelaF['ValorSS'].astype(int)
            tabelaF['Data'] = pd.to_datetime(tabelaF['Data'], format='%d/%m/%Y')
            tabelaF['Data'] = tabelaF['Data'].dt.day.astype(str)
            dadosIRRF = tabelaF[tabelaF['IRRF']>0].copy()
            dadosIRRF['Tipo'] = 'IRRF'
            dadosIRRF = dadosIRRF[['Data', 'Número', 'CNPJ', 'Tipo', 'IRRF',]].reset_index(drop=True)
            dadosIRRF.rename(columns={'IRRF': 'Valor'}, inplace=True)
            dadosRS = tabelaF.copy()
            dadosRS['Tipo'] = 'Retencao Social'
            dadosRS = dadosRS[['Data', 'Número', 'CNPJ', 'Tipo', 'Valor',]].reset_index(drop=True)
            dadosINSS = tabelaF[tabelaF['ValorSS']>0].copy()
            dadosINSS['Tipo'] = 'INSS'
            dadosINSS = dadosINSS[['Data', 'Número', 'CNPJ', 'Tipo', 'ValorSS']].reset_index(drop=True)
            dadosINSS.rename(columns={'ValorSS': 'Valor'}, inplace=True)
            dfFINAL = pd.concat([dadosRS, dadosIRRF, dadosINSS], ignore_index=True)
            dfFINAL['Número'] = dfFINAL['Número'].astype(str).str.zfill(10)
        elif tipo == 'Tipo 2':
            area = [123.672,31.476,562.523,779.733]

            df_list = tabula.read_pdf(caminho, pages=1, area=area,lattice=True)

            tabela = pd.concat(df_list, ignore_index=True)
            tabela.columns = ['Data', 'nada', 'Número', 'CNPJ', 'nada', 'nadaa', 'asdf', 'PIS', 'COFINS', 'CSLL' ,'IRRF', 'INSS']
            tabela = tabela[['Data', 'Número', 'CNPJ', 'PIS', 'COFINS', 'CSLL' ,'IRRF', 'INSS']]
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
            dfFINAL['CNPJ'] = dfFINAL['CNPJ'].str.replace(r'[-./]', '', regex=True)
            dfFINAL['Número'] = dfFINAL['Número'].astype(str).str.zfill(10)
        else:
            return 'faill'
        
        return {
            "df": dfFINAL
            }
    except Exception as e:
        erro = str(e)
        trace = traceback.format_exc()
        info = f'''INFO: HOUVE UM ERRO AO GERAR PDF\nErro: {erro}'''
        print(info)
        return {
            "df": None,
            "info" : info,
            "erro": str(e),  # Mensagem da exceção
            "erroF": traceback.format_exc(),  # Detalhes completos do traceback
            "arquivo": "PDF retencao"
            }
    
if __name__ == "__main__": 
    print(gerarpdf(r"C:\Users\Alexandre\Downloads\drive-download-20241010T171031Z-001\LBR\ARTESP8- Consorcio LBR Modera\Serv tomados\Relatorio retenção serv tomados LBR Modera 09-2024.pdf"))