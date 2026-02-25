import pandas as pd
from decimal import Decimal, ROUND_HALF_UP
import datetime
from datetime import date

def tratar_excel(file_path):
    df = pd.read_excel(file_path, dtype={2: str})

    # Transforma valores em decimal e arredonda para 2 casas decimais
    df["receb liquido"] = df["receb liquido"].apply(lambda x: Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
    df["comissao"] = 0
    df["imposto"] = 0

    df['data contrato'] = pd.to_datetime(df['data contrato'], errors='coerce')
    df['data baixa'] = pd.to_datetime(df['data baixa'], errors='coerce')

    df["cpf/cnpj"] = df["cpf/cnpj"].str.replace(r'[./-]', '', regex=True)
    df['razao social'] = df['razao social'].apply(lambda x: str(x).strip())
    df["mes"] = df["data baixa"].dt.month
    df = df[["codigo", "razao social", "cpf/cnpj", "data contrato", "mes", "comissao", "receb liquido", "imposto"]].groupby(["codigo", "razao social", "cpf/cnpj", "data contrato", "mes"], as_index=False).sum()

    df_pivot = df.pivot_table(
        index=["razao social","cpf/cnpj", "data contrato"],  # colunas que identificam a pessoa
        columns="mes",
        values=["receb liquido", "imposto", "comissao"],
        aggfunc="sum"
    )

    df_pivot = df_pivot.swaplevel(0, 1, axis=1)
    df_pivot = df_pivot.sort_index(axis=1, level=0)

    df_pivot.columns = [
        f"{mes}_{valor}"
        for mes, valor in df_pivot.columns
    ]

    df_pivot = df_pivot.reset_index()

    return df_pivot

def converter_excel(df_pivot, output_path):

    df = df_pivot
    df.fillna(0, inplace=True)

    colunas_excluir = ["razao_social", "cpf", "cnpj", "data"]

    colunas_numericas = [
        col for col in df.select_dtypes(include=["int64", "float64"]).columns
        if col not in colunas_excluir
    ]

    for col in colunas_numericas:
        df[col] = df[col].apply(
            lambda x: Decimal(str(x)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            if pd.notnull(x) else x
        )

    #DADOS FIXOS
    cnpj_nbb = '00420613000188'
    nome_locador = 'NBB CONSULTORIA LTDA'
    endereco_contribuente = 'RUA AFONSO BRAS, 579 12 ANDAR CJ 122 VILA NOVA CONCEICAO'
    endereco_imovel = 'Av Nações unidas, 12551 26 Andar  - Quotas wtc'
    ano =  2025
    uf = 'SP'
    codigo_municipio = 7107
    sequencial = 1
    cpf = "02697394753"
    cep = '04511011'

    def formatar_data(data, tamanho):
        if pd.isna(data) or data == 'NaT':
                return '0' * tamanho
        else:
            data = datetime.datetime.strptime(str(data), "%Y-%m-%d %H:%M:%S").strftime("%d%m%Y")
            return data

    def formatar_cpf_cnpj(valor, tamanho):
        if len(valor) < 14:
            return valor.strip().ljust(tamanho, ' ')
        else:
            return valor.strip()

    def formatar_valores(valores, tamanho):
        linha_formatada = ''
        
        # Organiza os dados por mês
        dados_por_mes = {}

        for coluna, valor in valores.items():
            mes, tipo = coluna.split("_", 1)
            if mes not in dados_por_mes:
                dados_por_mes[mes] = {}
            
            dados_por_mes[mes][tipo] = valor

        # Define ordem fixa dos tipos
        ordem_tipos = ["receb liquido", "comissao", "imposto"]

        # Agora monta na ordem correta
        for mes in dados_por_mes.keys():
            for tipo in ordem_tipos:
                valor = dados_por_mes[mes].get(tipo, 0)

                valor = str(valor).replace('.', '').replace(',', '')
                valor_formatado = formatar_numero(valor, tamanho)

                linha_formatada += valor_formatado

        return linha_formatada

    def formatar_texto(texto, tamanho):
        texto = str(texto).strip()
        return texto.ljust(tamanho)

    def formatar_numero(numero, tamanho):
        numero = str(numero).strip()
        return numero.rjust(tamanho, '0')

    def gerar_header():
        header = [
        formatar_texto('DIMOB', 5),  #TIPO 1 
        formatar_texto('', 369),
        ]
        return ''.join(header) + "\r\n"

    def gerar_linha(linha):
        nonlocal sequencial

        razao_social , cpf_cnpj, data_contrato, *resto = linha

        lista_linha = [
            formatar_texto('R02', 3), #TIPO 1 
            formatar_cpf_cnpj(cnpj_nbb, 14), #CNPJ do declarante 2
            formatar_numero(ano, 4), #ano atual 3
            formatar_numero(sequencial, 7), #Sequencial da locacao 4
            formatar_cpf_cnpj(cnpj_nbb, 14), #CPF/CPNJ do locador 5
            formatar_texto(nome_locador, 60), #Nome/Nome Empresarial do Locador 6
            formatar_cpf_cnpj(cpf_cnpj, 14), #CPF/CNPJ do Locatário 7
            formatar_texto(razao_social, 60), #Nome/Nome Empresarial do Locatário 8
            formatar_texto('S/N', 6), #Número do Contrato 9
            formatar_data(data_contrato, 8), #Data do Contrato 10
            formatar_valores(linha[3:], 14),  #todos os valores dos meses sendo feito
            formatar_texto('U', 1),#Tipo do Imóvel 47
            formatar_texto(endereco_imovel, 60), # Endereço do Imóvel 48
            formatar_numero(cep, 8), #CEP 49
            formatar_numero(codigo_municipio, 4), #Código do Município do Imóvel 50
            formatar_texto('', 20), #Reservado 51
            formatar_texto(uf, 2), #UF 52
            formatar_texto('', 10) #Reservado 53 # Delimitador de Registro 54
        ] 

        sequencial += 1
        return ''.join(lista_linha)

    def gerar_R01():
        r01 = [
            formatar_texto('R01', 3),
            formatar_cpf_cnpj(cnpj_nbb, 14),
            formatar_numero(ano, 4),
            formatar_numero(0, 1),
            formatar_numero(0, 10),
            formatar_numero(0, 1),
            formatar_numero(0, 8),
            formatar_numero(0, 2),
            formatar_texto(nome_locador, 60),
            formatar_texto(cpf, 11),
            formatar_texto(endereco_contribuente, 120),
            formatar_texto(uf, 2),
            formatar_texto(codigo_municipio, 4),
            formatar_texto('', 20),
            formatar_texto('', 10)
        ]
        return ''.join(r01) + "\r\n"

    def gerar_trailler():
        trailler = [
        formatar_texto('T9', 2),  #TIPO 1 
        formatar_texto('', 100),
        ]
        return ''.join(trailler) + "\r\n"

    lista = []
    for _, linha in df.iterrows():
        razao_social , cpf_cnpj, data_contrato, *resto = linha
        lista.append(gerar_linha(linha)+ "\r\n")

    ano = date.today().year -1
    with open(f'{output_path}/DIMOB_{ano}.txt', 'w', newline='', encoding="windows-1252") as arq:
        arq.write(gerar_header() + gerar_R01() + ''.join(lista) + gerar_trailler())

    return f'{output_path}/DIMOB_{ano}.txt'

def conversao_dimob(file_path, output_path):
    try:
        print(f"Processando arquivo: {file_path}")
        df_pivot = tratar_excel(file_path)
        nome = converter_excel(df_pivot, output_path)
        print(f"Arquivo convertido e salvo em: {nome}")
        return True, "Conversão realizada com sucesso" , nome
    except Exception as e:
        import traceback 
        traceback.print_exc()
        print(f"Erro ao processar o arquivo: {e}")
        return False, str(e), ''

if __name__ == "__main__":
    
    a, e, nome = conversao_dimob(r"C:\Users\Alexandre\Downloads\DIMOB NBB 2025- HENRIQUE.xlsx", r"C:\Users\Alexandre\Desktop\Nova pasta\Nova pasta")