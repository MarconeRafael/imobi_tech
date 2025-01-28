import pandas as pd

# Função para converter um arquivo Excel para CSV
def excel_to_csv(excel_file, csv_file):
    df = pd.read_excel(excel_file, engine='openpyxl')
    df.to_csv(csv_file, index=False, sep=';')  # Use ';' como separador para evitar conflito com vírgulas nos números

# Exemplo de uso para o arquivo de população
excel_file_populacao = '/home/m/beanalytic/imobi_tech/data/projecoes_2024_tab1_idade_simples.xlsx'  # Caminho do arquivo de população
csv_file_populacao = 'data/populacao.csv'  # Caminho do arquivo CSV de saída
excel_to_csv(excel_file_populacao, csv_file_populacao)

print("Arquivo CSV gerado com sucesso!")
