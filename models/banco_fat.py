import pandas as pd
from resources.config.caminhos import Caminhos

class FATModel:
    filepath = Caminhos.CAMINHO_GUIA_NOME

    @staticmethod
    def load_data():
        """Lê o banco de dados e retorna o DataFrame"""
        try:
            return pd.read_excel(FATModel.filepath)
        except FileNotFoundError:
            # Cria um DataFrame vazio se o arquivo não existir
            print('erro')
            return pd.DataFrame()

    @staticmethod
    def save_data(df):
        """Salva o DataFrame no banco de dados"""
        df.to_excel(FATModel.filepath, index=False)

    @staticmethod
    def add_new_data(lista):
        # Carrega os dados existentes
        df = FATModel.load_data()
        
        # Supondo que a lista tenha o CNPJ na primeira posição (ou em uma posição específica)
        cnpj_novo = lista[2]  # Substitua pelo índice correto onde o CNPJ está na lista
        
        # Verifica se o CNPJ já existe no DataFrame
        if cnpj_novo in df['CNPJ'].values:
            # Se o CNPJ já existir, substitui a linha existente
            df.loc[df['CNPJ'] == cnpj_novo] = lista
        else:
            # Se não existir, adiciona uma nova linha
            df.loc[len(df)] = lista
        
        # Salva os dados atualizados
        FATModel.save_data(df)

    @staticmethod
    def info_data():
        """Recebe um DataFrame e adiciona apenas as linhas que não existirem no banco"""
        existing_df = FATModel.load_data()

        print(existing_df.shape)
    
    @staticmethod
    def pesquisar_cnpj(CNPJ):
        """Recebe um DataFrame e adiciona apenas as linhas que não existirem no banco"""
        existing_df = FATModel.load_data()
        df = existing_df[existing_df['CNPJ']== CNPJ]
        if not df.empty:
            codigo, razao, cnpj, porcent, ret= df.iloc[0]
            return [codigo, razao, cnpj, porcent, ret]
        else:
            return False
        
    def exportar_db(folder_path):
        dfbanco = FATModel.load_data()
        dfbanco.to_excel(f'{folder_path}/GUIA NOME.xlsx', index=False)

    def importar_db(folder_path):
        dfbanco = pd.read_excel(folder_path, dtype=str)
        df = FATModel.load_data()
        dfbanco["CNPJ"] = dfbanco["CNPJ"].apply(lambda x: str(x).zfill(14).strip())
        df["CNPJ"] = df["CNPJ"].str.strip()

        df_final = pd.concat([dfbanco, df]).drop_duplicates(subset=["CNPJ"], keep="first")
        FATModel.save_data(df_final)

if __name__ == '__main__':
    banco = FATModel()
    print(banco.pesquisar_cnpj('49.685.243/0001-08'))