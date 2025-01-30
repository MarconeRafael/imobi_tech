from puxar_sidra import processar_dados_sidra
from populacao_dados import baixar_arquivo_ibge, salvar_csv, filtrar_csv
from tratamento import (
    load_csv_files, get_unique_values, print_unique_values, filter_dataframe, 
    save_dataframe, rename_column, drop_columns, aggregate_numeric_columns
)
from analize import (
    carregar_dados_populacao, carregar_dados_empresas, combinar_dados, 
    interpolar_dados, aplicar_clusterizacao, identificar_oportunidades_e_saturacao, salvar_dados
)
from graficos import (
    criar_diretorio_saida, carregar_dados, obter_estados_por_cluster, 
    gerar_grafico_dispersao, gerar_grafico_tendencia, gerar_heatmap_saturacao, salvar_lista_clusters
)
import os
import pandas as pd

def baixar_e_processar_dados():
    """Baixa e processa os dados da SIDRA e do IBGE."""
    output_dir = 'data'
    sidra_url = "https://apisidra.ibge.gov.br/values/t/1757/p/2007-2022/n1/1/n3/all/v/allxp"
    
    # Puxar dados da SIDRA
    processar_dados_sidra(sidra_url, output_dir)

    # Baixar projeção populacional do IBGE
    ibge_url = "https://ftp.ibge.gov.br/Projecao_da_Populacao/Projecao_da_Populacao_2024/projecoes_2024_tab1_idade_simples.xlsx"
    excel_file_path = "data/projecoes_2024_tab1_idade_simples.xlsx"
    csv_input_path = "data/populacao.csv"
    csv_output_path = "data/populacao_filtrada.csv"

    baixar_arquivo_ibge(ibge_url, excel_file_path)
    salvar_csv(excel_file_path, csv_input_path)
    filtrar_csv(csv_input_path, csv_output_path)

def tratar_dados():
    """Carrega, trata e salva os dados da população e empresas ativas."""
    file_paths = ["data/dados_2007_2020.csv", "data/dados_2021_2022.csv"]
    
    # Carregar e combinar arquivos CSV
    df_combined = load_csv_files(file_paths)

    # Exibir valores únicos por coluna
    unique_values = get_unique_values(df_combined)
    print_unique_values(unique_values)

    # Filtrar dados de empresas ativas
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

    # Agregar colunas numéricas
    numeric_columns = ["Ano", "População", "Número de empresas ativas", "Razão População/Empresas"]
    merged_df = aggregate_numeric_columns(df_combined, ["Ano", "LOCAL"], numeric_columns)

    # Remover coluna "SIGLA" se existir
    if "SIGLA" in merged_df.columns:
        merged_df = drop_columns(merged_df, ["SIGLA"])

    # Salvar dados tratados
    save_dataframe(merged_df, "data/dados_agrupados.csv")
    print(merged_df.dtypes)

def analisar_dados():
    """Realiza a análise dos dados e aplica clusterização."""
    # Carregar dados
    dados_populacao = carregar_dados_populacao("data/populacao_filtrada.csv")
    dados_empresas = carregar_dados_empresas("data/dados_filtrados_numero_empresas_ativas.csv")

    # Combinar e processar dados
    dados_combinados = combinar_dados(dados_populacao, dados_empresas)
    dados_interpolados = interpolar_dados(dados_combinados)

    # Aplicar clusterização
    dados_clusterizados = aplicar_clusterizacao(dados_interpolados)

    # Identificar saturação e oportunidades
    estados_saturados, estados_oportunidades = identificar_oportunidades_e_saturacao(dados_clusterizados)

    # Exibir resultados
    print("\nEstados Saturados (Alta razão População/Empresas):", estados_saturados)
    print("\nEstados com Oportunidades (Baixa razão População/Empresas):", estados_oportunidades)

    # Salvar os resultados
    salvar_dados(dados_clusterizados)

def gerar_graficos():
    """Gera e salva os gráficos baseados nos dados processados."""
    # Criar diretório de saída para gráficos
    diretorio_saida = criar_diretorio_saida()

    # Carregar os dados processados
    caminho_arquivo = "data/merged_data.csv"
    dados = carregar_dados(caminho_arquivo)

    if dados is None:
        return

    # Obter estados por cluster
    estados_por_cluster = obter_estados_por_cluster(dados)

    # Gerar e salvar gráficos
    caminho_dispersao = gerar_grafico_dispersao(dados, diretorio_saida)
    caminho_tendencia = gerar_grafico_tendencia(dados, estados_por_cluster, diretorio_saida)
    caminho_heatmap = gerar_heatmap_saturacao(dados, diretorio_saida)

    # Salvar lista de estados por cluster
    caminho_clusters = salvar_lista_clusters(estados_por_cluster, diretorio_saida)

    # Exibir confirmação dos arquivos gerados
    print("\nGráficos salvos em:", diretorio_saida)
    print(f"- {caminho_dispersao}")
    print(f"- {caminho_tendencia}")
    print(f"- {caminho_heatmap}")
    print("\nLista de estados por cluster salva em:", caminho_clusters)

def main():
    """Função principal que executa todas as etapas do pipeline."""
    print("\n=== Etapa 1: Baixando e processando dados ===")
    baixar_e_processar_dados()

    print("\n=== Etapa 2: Tratando dados ===")
    tratar_dados()

    print("\n=== Etapa 3: Analisando dados ===")
    analisar_dados()

    print("\n=== Etapa 4: Gerando gráficos ===")
    gerar_graficos()

if __name__ == "__main__":
    main()
