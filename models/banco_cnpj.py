import pandas as pd
from resources.config.caminhos import Caminhos

class CNPJModel:
    filepath = Caminhos.CAMINHO_BANCO_CNPJ

    @staticmethod
    def load_data():
        """Lê o banco de dados e retorna o DataFrame"""
        try:
            return pd.read_excel(CNPJModel.filepath)
        except FileNotFoundError:
            # Cria um DataFrame vazio se o arquivo não existir
            return pd.DataFrame()

    @staticmethod
    def save_data(df):
        """Salva o DataFrame no banco de dados"""
        df.to_excel(CNPJModel.filepath, index=False)

    @staticmethod
    def banco_to_dict():
        """Retorna todo o banco de dados como um dicionário"""
        df = CNPJModel.load_data()
        df['CNPJ'] = df['CNPJ'].apply(lambda x: str(x).zfill(14))
        df['Nome'] = df['Nome'].apply(lambda x: x.strip())
        return dict(zip(df['CNPJ'], df['Nome']))

    @staticmethod
    def add_new_data(df):
        """Recebe um DataFrame e adiciona apenas as linhas que não existirem no banco"""
        existing_df = CNPJModel.load_data()

        # Verifica se a linha já existe com base no CNPJ
        new_data = df[~df['CNPJ'].isin(existing_df['CNPJ'])]

        # Adiciona os novos dados ao banco
        if not new_data.empty:
            updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            
            # Remove duplicatas, mantendo o primeiro registro
            updated_df = updated_df.drop_duplicates(subset='CNPJ', keep='first')
            
            # Salva os dados atualizados
            CNPJModel.save_data(updated_df)
    
    @staticmethod
    def info_data():
        """Recebe um DataFrame e adiciona apenas as linhas que não existirem no banco"""
        existing_df = CNPJModel.load_data()

        print(existing_df.shape)
    
if __name__ == '__main__':
    
    banco = CNPJModel()
    banco.info_data()