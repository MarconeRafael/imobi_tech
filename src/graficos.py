import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def criar_diretorio_saida(diretorio="resultados"):
    """
    Cria o diretório para salvar os resultados, caso não exista.
    """
    os.makedirs(diretorio, exist_ok=True)
    return diretorio

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados processados do arquivo CSV e realiza a limpeza inicial.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado. Execute o processamento dos dados primeiro.")
        return None

    df = pd.read_csv(caminho_arquivo)

    # Remover "Brasil" para análise por estado
    df = df[df["LOCAL"] != "Brasil"]

    # Garantir que as colunas numéricas estão no formato correto
    df["Ano"] = df["Ano"].astype(int)
    df["Razão População/Empresas"] = df["Razão População/Empresas"].astype(float)
    df["Cluster"] = df["Cluster"].astype(int)

    return df

def obter_estados_por_cluster(df):
    """
    Retorna um dicionário com a lista de estados por cluster.
    """
    cluster_estados = {}
    for cluster in df["Cluster"].unique():
        estados_cluster = df[df["Cluster"] == cluster]["LOCAL"].unique().tolist()
        cluster_estados[cluster] = estados_cluster
    return cluster_estados

def gerar_grafico_dispersao(df, diretorio_saida):
    """
    Gera e salva um gráfico de dispersão dos clusters ao longo do tempo.
    """
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x=df["Ano"], y=df["Razão População/Empresas"],
                    hue=df["Cluster"], palette="tab10", s=100)

    plt.xlabel("Ano")
    plt.ylabel("Razão População/Empresas")
    plt.title("Clusters de Estados por Razão População/Empresas")
    plt.legend(title="Cluster", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(True)

    caminho_grafico = os.path.join(diretorio_saida, "clusters_dispersao.png")
    plt.savefig(caminho_grafico, bbox_inches="tight")
    plt.show()
    return caminho_grafico

def gerar_grafico_tendencia(df, cluster_estados, diretorio_saida):
    """
    Gera e salva um gráfico de linhas mostrando a tendência temporal por cluster.
    """
    plt.figure(figsize=(14, 7))
    for cluster, estados in cluster_estados.items():
        for estado in estados:
            subset = df[df["LOCAL"] == estado]
            plt.plot(subset["Ano"], subset["Razão População/Empresas"], label=f"{estado} (Cluster {cluster})", linestyle="--")

    plt.xlabel("Ano")
    plt.ylabel("Razão População/Empresas")
    plt.title("Tendências Temporais por Cluster")
    plt.legend(loc="upper right", fontsize="small")
    plt.grid(True)

    caminho_grafico = os.path.join(diretorio_saida, "tendencias_temporais.png")
    plt.savefig(caminho_grafico, bbox_inches="tight")
    plt.show()
    return caminho_grafico

def gerar_heatmap_saturacao(df, diretorio_saida):
    """
    Gera e salva um heatmap para visualizar a saturação de mercado por estado ao longo do tempo.
    """
    pivot_data = df.pivot(index="LOCAL", columns="Ano", values="Razão População/Empresas")

    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, cmap="coolwarm", linewidths=0.5, annot=False, cbar_kws={'label': 'Razão População/Empresas'})

    plt.xlabel("Ano")
    plt.ylabel("Estados")
    plt.title("Heatmap de Saturação por Estado")

    caminho_grafico = os.path.join(diretorio_saida, "heatmap_saturacao.png")
    plt.savefig(caminho_grafico, bbox_inches="tight")
    plt.show()
    return caminho_grafico

def salvar_lista_clusters(cluster_estados, diretorio_saida):
    """
    Salva a lista de estados por cluster em um arquivo de texto.
    """
    caminho_arquivo = os.path.join(diretorio_saida, "clusters_estados.txt")
    with open(caminho_arquivo, "w") as f:
        for cluster, estados in cluster_estados.items():
            f.write(f"Cluster {cluster}:\n")
            f.write(", ".join(estados) + "\n\n")
    return caminho_arquivo

def main():
    """
    Função principal que executa o pipeline de visualização e análise dos clusters.
    """
    # Criar diretório para salvar os gráficos
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

if __name__ == "__main__":
    main()
