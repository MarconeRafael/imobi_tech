import requests
import os
import pandas as pd
import numpy as np

# URL do arquivo de projeção de população no IBGE
ibge_url = "https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab1_idade_simples.xlsx"
excel_file_path = "data/projecoes_2024_tab1_idade_simples.xlsx"
csv_input_path = "data/populacao.csv"
csv_output_path = "data/populacao_filtrada.csv"

# Função para baixar o arquivo do IBGE
def baixar_arquivo_ibge(url, output_path):
    print("Baixando arquivo do IBGE...")
    response = requests.get(url)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Criar diretório, se não existir
    with open(output_path, 'wb') as file:
        file.write(response.content)
    print(f"Arquivo baixado e salvo em: {output_path}")

# Função para salvar os dados do Excel em CSV (removendo as 5 primeiras linhas)
def salvar_csv(excel_path, csv_output_path):
    # Ler o arquivo Excel, ignorando as 5 primeiras linhas
    print("Lendo o arquivo Excel...")
    df_pop = pd.read_excel(excel_path, header=5)  # Pular as 5 primeiras linhas

    # Exibir as primeiras linhas para verificar a estrutura
    print("Estrutura do arquivo:")
    print(df_pop.head(15))

    # Exibir os nomes das colunas para verificar como são
    print("Colunas do arquivo:")
    print(df_pop.columns)

    # Salvar o arquivo em CSV sem filtrar nenhuma coluna
    print(f"Salvando os dados no CSV: {csv_output_path}")
    df_pop.to_csv(csv_output_path, index=False)
    return df_pop

# Função para filtrar a população na faixa etária de 38 a 58 anos e para os anos de 2007 a 2022
def filtrar_csv(csv_input_path, csv_output_path, faixa_etaria=(38, 58), anos=(2007, 2022)):
    # Ler o arquivo CSV
    print("Lendo o arquivo CSV...")
    df_pop = pd.read_csv(csv_input_path)

    # Exibir as primeiras linhas para verificar a estrutura
    print("Estrutura do arquivo:")
    print(df_pop.head(10))

    # Exibir os nomes das colunas para verificar como são
    print("Colunas do arquivo:")
    print(df_pop.columns)

    # Filtrar os dados de acordo com a faixa etária de 38 a 58 anos
    print("Filtrando a população na faixa etária de 38 a 58 anos...")
    df_pop = df_pop[(df_pop['IDADE'] >= faixa_etaria[0]) & (df_pop['IDADE'] <= faixa_etaria[1])]

    # Filtrar os dados para os anos entre 2007 e 2022
    anos_colunas = [str(ano) for ano in range(anos[0], anos[1] + 1)]
    df_pop = df_pop[['IDADE', 'SEXO', 'CÓD.', 'SIGLA', 'LOCAL'] + anos_colunas]

    # Interpolação para estimar os anos de 2021 e 2022 com base nos anos de 2007 a 2020
    print("Interpolando os dados para os anos de 2021 e 2022...")
    df_pop[anos_colunas] = df_pop[anos_colunas].apply(pd.to_numeric, errors='coerce')
    df_pop[anos_colunas] = df_pop[anos_colunas].interpolate(method='linear', axis=1)

    # Exibir as primeiras linhas para verificar a interpolação
    print("Estrutura do arquivo após interpolação:")
    print(df_pop.head(10))

    # Salvar os dados filtrados e interpolados em um novo arquivo CSV
    print(f"Salvando os dados filtrados em: {csv_output_path}")
    df_pop.to_csv(csv_output_path, index=False)
    return df_pop

# Baixar o arquivo do IBGE
baixar_arquivo_ibge(ibge_url, excel_file_path)

# Executar as funções
salvar_csv(excel_file_path, csv_input_path)
filtrar_csv(csv_input_path, csv_output_path)
