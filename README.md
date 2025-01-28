---

# Análise Temporal do Mercado Imobiliário

Este projeto analisa a razão entre consumidores da faixa etária predominante (38 a 58 anos) e o número de empresas de construção ativas por estado no Brasil entre 2007 e 2022. O objetivo é identificar estados saturados e aqueles com maior potencial de crescimento no mercado imobiliário.

## Objetivos

1. **Analisar séries temporais (2007-2022):** Calcular a razão entre consumidores na faixa de 38 a 58 anos e o número de empresas ativas por estado.
2. **Prever os anos de 2021 e 2022:** Utilizando dados históricos de 2007 a 2020.
3. **Agrupar estados com comportamentos similares:** Identificar padrões nas séries temporais e realizar agrupamentos.
4. **Identificar oportunidades e saturação:** Detectar estados saturados e aqueles com maior potencial de crescimento.

---

## Fontes de Dados

1. **Dados das empresas de construção**  
   - Tabela: [Tabela 1757 - Dados gerais das empresas de construção](https://apisidra.ibge.gov.br/home/ajuda)  
   - Obtido pela API do SIDRA (IBGE).  

2. **Dados populacionais**  
   - Tabela: [População por sexo e idade simples](https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html)  
   - Arquivo disponível em formato `xlsx` ou `ods`.  

---

## Requisitos

Certifique-se de ter instalado o Python 3.7 ou superior e as seguintes dependências listadas no arquivo `requirements.txt`:

```
pandas
numpy
requests
scikit-learn
matplotlib
seaborn
```

Para instalar as dependências, execute:  
```bash
pip install -r requirements.txt
```

---

## Estrutura do Projeto

```plaintext
.
├── data/                   # Diretório para armazenar os dados baixados
├── notebooks/              # Notebooks de validação e análise
├── src/                    # Código-fonte principal
│   ├── sidra_api.py        # Script para obter dados da API do SIDRA
│   ├── population_data.py  # Script para manipulação de dados populacionais
│   ├── analysis.py         # Scripts de análise e visualização
│   ├── clustering.py       # Script de agrupamento das séries temporais
├── results/                # Resultados (gráficos, tabelas, etc.)
├── README.md               # Documentação do projeto
├── requirements.txt        # Lista de dependências do projeto
└── .gitignore              # Arquivos e pastas ignorados pelo Git
```

---

## Como Executar

1. **Clone o repositório:**
   ```bash
   git clone <link-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. **Baixe os dados populacionais:**
   - Faça o download da tabela "População por sexo e idade simples" no formato `xlsx` ou `ods` e salve no diretório `data/`.

3. **Execute o código:**
   - Extraia os dados das empresas via API:
     ```bash
     python src/sidra_api.py
     ```
   - Manipule os dados populacionais:
     ```bash
     python src/population_data.py
     ```
   - Realize a análise e previsões:
     ```bash
     python src/analysis.py
     ```
   - Realize o agrupamento:
     ```bash
     python src/clustering.py
     ```

4. **Visualize os resultados:**
   - Os gráficos e análises finais serão salvos no diretório `results/`.

---

## Metodologia

### 1. **Extração de Dados**
   - Utiliza requisições HTTP para acessar a API do SIDRA (Tabela 1757).
   - Manipula dados populacionais com interpolação para a faixa de idade de 38 a 58 anos.

### 2. **Análise de Séries Temporais**
   - Divide os dados em treino (2007-2020) e teste (2021-2022).
   - Realiza previsões usando modelos de séries temporais (ex.: ARIMA).

### 3. **Agrupamento**
   - Utiliza algoritmos como k-means para identificar padrões de comportamento entre os estados.

### 4. **Identificação de Saturação e Oportunidades**
   - Analisa as razões calculadas e tendências para determinar os estados saturados ou com maior potencial.

---

## Resultados Esperados

1. **Gráficos de séries temporais por estado.**
2. **Agrupamento de estados com comportamentos similares.**
3. **Lista dos estados mais saturados e com maior potencial futuro.**

---

## Referências

[1] SCOD Brasil. [Tendências do Mercado Imobiliário para 2023](https://scod.com.br/blog/post/tend%C3%AAncias-do-mercado-imobili%C3%A1rio-para-2023).  

[2] IBGE. [API SIDRA](https://apisidra.ibge.gov.br/home/ajuda).  

[3] IBGE. [Projeção da População](https://www.ibge.gov.br/estatisticas/sociais/populacao/9109-projecao-da-populacao.html).  

---