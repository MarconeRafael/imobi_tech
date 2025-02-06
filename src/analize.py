import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from sklearn.cluster import KMeans
import os

def carregar_dados_populacao(caminho_arquivo):
    """
    Carrega os dados populacionais e transforma os anos de colunas para linhas.
    """
    df = pd.read_csv(caminho_arquivo)
    anos = [str(ano) for ano in range(2007, 2023)]
    df = df[["LOCAL"] + anos]
    df = df.melt(id_vars=["LOCAL"], var_name="Ano", value_name="População")
    df["Ano"] = df["Ano"].astype(int)
    return df.groupby(["Ano", "LOCAL"], as_index=False).sum()

def carregar_dados_empresas(caminho_arquivo):
    """
    Carrega os dados de empresas ativas e padroniza as colunas.
    """
    df = pd.read_csv(caminho_arquivo)
    df.rename(columns={"Brasil e Unidade da Federação": "LOCAL"}, inplace=True)
    df = df[["LOCAL", "Ano", "Número de empresas ativas"]]
    return df.groupby(["Ano", "LOCAL"], as_index=False).sum()

def combinar_dados(populacao_df, empresas_df):
    """
    Une os dados populacionais com os dados de empresas e calcula a razão População/Empresas.
    """
    df = pd.merge(populacao_df, empresas_df, on=["LOCAL", "Ano"], how="inner")
    df["Número de empresas ativas"] = df["Número de empresas ativas"].astype(float)
    df["População"] = df["População"].astype(float)
    df["Razão População/Empresas"] = df["População"] / df["Número de empresas ativas"]
    return df.groupby(["Ano", "LOCAL"], as_index=False).agg({
        "População": "sum",
        "Número de empresas ativas": "sum",
        "Razão População/Empresas": "mean"
    }).dropna(subset=["Razão População/Empresas"])

def interpolar_dados(df):
    """
    Interpola valores para os anos de 2021 e 2022 com base nos anos anteriores.
    """
    estados = df["LOCAL"].unique()
    for estado in estados:
        estado_df = df[df["LOCAL"] == estado]
        if len(estado_df) < 2:
            continue

        anos_existentes = estado_df["Ano"].values
        razao_existente = estado_df["Razão População/Empresas"].values

        interpolador = interp1d(anos_existentes, razao_existente, kind='linear', fill_value="extrapolate")
        estimativas = interpolador([2021, 2022])

        df = pd.concat([
            df,
            pd.DataFrame({"LOCAL": [estado, estado],
                          "Ano": [2021, 2022],
                          "Razão População/Empresas": estimativas})
        ], ignore_index=True)
    
    return df.drop_duplicates(subset=["Ano", "LOCAL"])

def aplicar_clusterizacao(df, num_clusters=4):
    """
    Aplica K-Means para agrupar os estados de acordo com a razão População/Empresas.
    """
    X = df.pivot(index="Ano", columns="LOCAL", values="Razão População/Empresas").fillna(method="ffill").T
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X)
    
    mapa_clusters = {estado: cluster for estado, cluster in zip(X.index, clusters)}
    df["Cluster"] = df["LOCAL"].map(mapa_clusters)
    
    return df

def identificar_oportunidades_e_saturacao(df):
    """
    Identifica estados saturados e com oportunidades futuras baseando-se na razão População/Empresas.
    """
    media_razao_por_estado = df[df["Ano"].isin([2021, 2022])].groupby("LOCAL")["Razão População/Empresas"].mean()
    
    q75, q25 = np.percentile(media_razao_por_estado.dropna(), [75, 25])
    estados_saturados = media_razao_por_estado[media_razao_por_estado > q75].index.tolist()
    estados_oportunidades = media_razao_por_estado[media_razao_por_estado < q25].index.tolist()
    
    return estados_saturados, estados_oportunidades

def salvar_dados(df, caminho_pasta="data", nome_arquivo="merged_data.csv"):
    """
    Salva os dados processados em um arquivo CSV dentro da pasta especificada.
    """
    os.makedirs(caminho_pasta, exist_ok=True)
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)
    df.to_csv(caminho_completo, index=False)
    print(f"Arquivo salvo: {caminho_completo}")

def main():
    """
    Função principal que executa todo o pipeline de análise.
    """
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

if __name__ == "__main__":
    main()
