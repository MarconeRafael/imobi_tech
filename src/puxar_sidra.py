import os
import requests
import pandas as pd

# URL da API SIDRA para a Tabela 1757
url = "https://apisidra.ibge.gov.br/values/t/1757/p/2007-2022/n1/1/n3/all/v/allxp"

# Função para verificar e criar o diretório de destino
def verificar_criar_diretorio(diretorio):
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

# Função para fazer a requisição à API SIDRA
def obter_dados_sidra(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na requisição: {response.status_code}")
        return None

# Função para ajustar o DataFrame, com cabeçalho e conversão de colunas
def ajustar_dataframe(data):
    df = pd.DataFrame(data)
    df.columns = df.iloc[0]  # Definir a primeira linha como cabeçalho
    df = df.drop(0)  # Remover a linha que foi usada como cabeçalho
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')  # Garantir que a coluna 'Ano' seja do tipo inteiro
    return df

# Função para filtrar os dados entre os anos especificados
def filtrar_dados_por_ano(df, inicio, fim):
    return df[df['Ano'].between(inicio, fim)]

# Função para salvar o DataFrame em um arquivo CSV
def salvar_csv(df, caminho):
    df.to_csv(caminho, index=False)
    print(f"Arquivo salvo em: {caminho}")

# Função principal para executar todas as etapas
def processar_dados_sidra(url, output_dir):
    verificar_criar_diretorio(output_dir)

    # Obter dados da API SIDRA
    dados = obter_dados_sidra(url)
    
    if dados:
        # Ajustar o DataFrame
        df = ajustar_dataframe(dados)
        
        # Verificar se a coluna 'Ano' está presente
        if 'Ano' in df.columns:
            # Filtrar os dados de 2007 a 2020 e de 2021 a 2022
            df_2007_2020 = filtrar_dados_por_ano(df, 2007, 2020)
            df_2021_2022 = filtrar_dados_por_ano(df, 2021, 2022)
            
            # Salvar os arquivos CSV
            salvar_csv(df_2007_2020, f'{output_dir}/dados_2007_2020.csv')
            salvar_csv(df_2021_2022, f'{output_dir}/dados_2021_2022.csv')
        else:
            print("A coluna 'Ano' não foi encontrada após o ajuste do cabeçalho.")
    else:
        print("Dados vazios ou inválidos retornados pela API.")

# Definir o diretório de destino
output_dir = 'data'

# Chamar a função principal
processar_dados_sidra(url, output_dir)
