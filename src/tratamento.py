import pandas as pd

def load_csv_files(file_paths):
    """Carrega e concatena múltiplos arquivos CSV em um único DataFrame."""
    dfs = [pd.read_csv(file) for file in file_paths]
    return pd.concat(dfs, ignore_index=True)

def get_unique_values(df):
    """Obtém valores únicos de cada coluna do DataFrame."""
    return {col: df[col].unique() for col in df.columns}

def print_unique_values(unique_values):
    """Exibe os valores únicos por coluna."""
    for col, values in unique_values.items():
        print(f"Coluna: {col}")
        print(values)
        print("-" * 50)

def filter_dataframe(df, column, value):
    """Filtra o DataFrame para manter apenas as linhas onde a coluna especificada possui um valor específico."""
    return df[df[column] == value]

def save_dataframe(df, file_path):
    """Salva um DataFrame em um arquivo CSV."""
    df.to_csv(file_path, index=False)

def rename_column(df, old_name, new_name):
    """Renomeia uma coluna do DataFrame."""
    df.rename(columns={old_name: new_name}, inplace=True)
    return df

def drop_columns(df, columns):
    """Remove colunas específicas do DataFrame."""
    return df.drop(columns=columns)

def aggregate_numeric_columns(df, group_by_columns, numeric_columns):
    """Agrupa o DataFrame removendo duplicatas e mantendo a média dos valores numéricos."""
    return df.groupby(group_by_columns, as_index=False)[numeric_columns].mean()

def main():
    # Definição dos caminhos dos arquivos CSV
    file_paths = ["data/dados_2007_2020.csv", "data/dados_2021_2022.csv"]
    
    # Carregar e combinar os arquivos CSV
    df_combined = load_csv_files(file_paths)
    
    # Exibir valores únicos por coluna
    unique_values = get_unique_values(df_combined)
    print_unique_values(unique_values)
    
    # Filtrar o DataFrame
    df_filtered = filter_dataframe(df_combined, "Variável", "Número de empresas ativas")
    save_dataframe(df_filtered, "data/dados_filtrados_numero_empresas_ativas.csv")
    
    # Renomear colunas e remover desnecessárias
    df_filtered = rename_column(df_filtered, "Variável (Código)", "Número de empresas ativas")
    df_filtered = drop_columns(df_filtered, ["Variável"])
    save_dataframe(df_filtered, "data/dados_filtrados_numero_empresas_ativas.csv")
    
    # Carregar dados populacionais e exibir valores únicos
    df_populacao = pd.read_csv("data/populacao_filtrada.csv")
    unique_values_populacao = get_unique_values(df_populacao)
    print_unique_values(unique_values_populacao)
    
    # Selecionar apenas colunas numéricas para agregação
    numeric_columns = ["Ano", "População", "Número de empresas ativas", "Razão População/Empresas"]
    merged_df = aggregate_numeric_columns(df_combined, ["Ano", "LOCAL"], numeric_columns)
    
    # Remover a coluna "SIGLA" antes da agregação
    if "SIGLA" in merged_df.columns:
        merged_df = drop_columns(merged_df, ["SIGLA"])
    
    # Salvar os dados processados
    save_dataframe(merged_df, "data/dados_agrupados.csv")
    print(merged_df.dtypes)

if __name__ == "__main__":
    main()