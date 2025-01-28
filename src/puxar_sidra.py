import os
import requests
import pandas as pd

# URL da API SIDRA para a Tabela 1757
url = "https://apisidra.ibge.gov.br/values/t/1757/p/2007-2022/n1/1/n3/all/v/allxp"

# Verificar se o diretório de destino existe, caso contrário, criar
output_dir = 'data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Requisição HTTP
response = requests.get(url)

# Verificação de sucesso na requisição
if response.status_code == 200:
    data = response.json()
    
    # Verificar se os dados retornaram corretamente
    if data:
        # Converter os dados JSON em um DataFrame do pandas
        df = pd.DataFrame(data)
        
        # Exibir as primeiras linhas do DataFrame para ver como ficou
        print("Primeiras linhas do DataFrame:")
        print(df.head())
        
        # Ajustando o DataFrame, a primeira linha contém as descrições das colunas
        df.columns = df.iloc[0]  # Definir a primeira linha como cabeçalho
        df = df.drop(0)  # Remover a linha que foi usada como cabeçalho
        
        # Exibir as colunas após o ajuste do cabeçalho
        print("\nColunas após ajuste do cabeçalho:")
        print(df.columns)
        
        # Garantir que a coluna 'Ano' seja do tipo inteiro
        df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
        
        # Agora usaremos a coluna 'Ano' para filtrar os dados
        if 'Ano' in df.columns:
            # Filtrar os dados de 2007 a 2020
            df_2007_2020 = df[df['Ano'].between(2007, 2020)]
            
            # Filtrar os dados de 2021 e 2022
            df_2021_2022 = df[df['Ano'].between(2021, 2022)]
            
            # Salvar os dados em dois arquivos CSV
            df_2007_2020.to_csv(f'{output_dir}/dados_2007_2020.csv', index=False)
            df_2021_2022.to_csv(f'{output_dir}/dados_2021_2022.csv', index=False)
            
            print("Arquivos CSV salvos com sucesso!")
        else:
            print("A coluna 'Ano' não foi encontrada após o ajuste do cabeçalho.")
        
    else:
        print("Dados vazios ou inválidos retornados pela API.")
else:
    print(f"Erro na requisição: {response.status_code}")
