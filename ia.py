import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

# Configuração da página
st.set_page_config(page_title="Painel de Transporte - Recife", layout="wide")

# Inicializando o Faker para gerar dados falsos
fake = Faker()

# Lista de rotas fictícias em Recife (bairros e pontos de referência)
rotas_recife = [
    "Boa Viagem", "Centro", "Aeroporto", "Pina", "Imbiribeira", "Casa Forte", 
    "Tamarineira", "Olinda", "Caxangá", "Graças", "Cordeiro", "Jardim São Paulo",
    "Afogados", "San Martin", "Ipsep"
]

# Função para gerar dados de transporte (Histórico de 2 anos)
def gerar_dados_transporte(num_linhas=100, anos=2):
    dados = []
    for _ in range(num_linhas):
        data_inicio = pd.Timestamp.today() - pd.DateOffset(years=anos)
        for i in range(anos * 365):  # Gerar dados para 2 anos
            data = data_inicio + pd.DateOffset(days=i)
            dados.append({
                "Rota": np.random.choice(rotas_recife),
                "Distância Percorrida (km)": np.random.randint(100, 500),
                "Distância Planejada (km)": np.random.randint(100, 500),
                "Tempo Médio (h)": np.random.uniform(1, 8),
                "Consumo de Combustível (L)": np.random.uniform(10, 50),
                "Custo por Viagem (R$)": np.random.uniform(100, 500),
                "Status Entrega": np.random.choice(["Concluída", "Atrasada"]),
                "Custo de Combustível (R$)": np.random.uniform(50, 200),
                "Custo de Manutenção (R$)": np.random.uniform(10, 100),
                "Satisfação Cliente (NPS)": np.random.randint(1, 10),
                "Taxa de Ocupação (%)": np.random.uniform(60, 100),
                "Data": data
            })
    return pd.DataFrame(dados)

# Gerar dados históricos
df_transporte = gerar_dados_transporte()

# Título do app
st.title("Painel de BI para Gestão de Transporte - Recife")

# Filtros de Seleção
st.sidebar.header("Filtros de Dados")
rota_selecionada = st.sidebar.selectbox("Selecione a Rota", ["Todas"] + rotas_recife)
status_selecionado = st.sidebar.selectbox("Selecione o Status de Entrega", ["Todos", "Concluída", "Atrasada"])
nps_min = st.sidebar.slider("Selecione o NPS Mínimo", 1, 10, 1)

# Filtrando os dados com base nos filtros selecionados
df_filtrado = df_transporte.copy()

if rota_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Rota"] == rota_selecionada]
    
if status_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Status Entrega"] == status_selecionado]
    
df_filtrado = df_filtrado[df_filtrado["Satisfação Cliente (NPS)"] >= nps_min]

# Criando as guias
tab1, tab2 = st.tabs(["Histórico de Transporte", "Previsão para os Próximos 2 Anos"])

# Guia de Histórico de Transporte
with tab1:
    st.subheader("Dados de Transporte Históricos (Últimos 2 anos)")
    st.dataframe(df_filtrado)
    
    # Gráfico de desempenho das rotas
    st.subheader("Desempenho das Rotas")
    sns.set(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Rota", y="Distância Percorrida (km)", data=df_filtrado, ax=ax)
    ax.set_title("Distância Percorrida por Rota")
    ax.set_xlabel("Rota")
    ax.set_ylabel("Distância (km)")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    # Gráfico de custos de transporte
    st.subheader("Custo de Transporte")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Rota", y="Custo por Viagem (R$)", data=df_filtrado, ax=ax)
    ax.set_title("Custo por Viagem por Rota")
    ax.set_xlabel("Rota")
    ax.set_ylabel("Custo (R$)")
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Guia de Previsão para os Próximos 2 Anos
with tab2:
    st.subheader("Previsão de Desempenho para os Próximos 2 Anos")
    
    # Preparando os dados para a previsão
    df_previsao = df_filtrado[['Data', 'Distância Percorrida (km)']]
    df_previsao = df_previsao.groupby('Data').agg({'Distância Percorrida (km)': 'sum'}).reset_index()

    # Preparando os dados para o Prophet
    df_previsao.rename(columns={'Data': 'ds', 'Distância Percorrida (km)': 'y'}, inplace=True)
    modelo = Prophet()
    modelo.fit(df_previsao)
    
    # Fazendo a previsão para os próximos 2 anos
    futuro = modelo.make_future_dataframe(periods=365*2, freq='D')
    previsão = modelo.predict(futuro)
    
    # Plotando a previsão
    # st.subheader("Previsão da Distância Percorrida para os Próximos 2 Anos")
    fig2 = modelo.plot(previsão)
    st.pyplot(fig2)
    
    # Exibindo dados de previsão
    previsão_pt = previsão[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].rename(
    columns={
        'ds': 'Data',
        'yhat': 'Previsão (km)',
        'yhat_lower': 'Limite Inferior (km)',
        'yhat_upper': 'Limite Superior (km)'
    })
    
    # Gráfico da previsão
    st.subheader("Projeção da Distância Percorrida")
    fig3, ax = plt.subplots(figsize=(10, 6))
    ax.plot(previsão['ds'], previsão['yhat'], label='Previsão', color='blue')
    ax.fill_between(previsão['ds'], previsão['yhat_lower'], previsão['yhat_upper'], color='orange', alpha=0.3)
    ax.set_title("Projeção da Distância Percorrida (Próximos 2 Anos)")
    ax.set_xlabel("Data")
    ax.set_ylabel("Distância Percorrida (km)")
    st.pyplot(fig3)

    # Explicação simplificada sobre o cálculo da previsão
    st.markdown("""
    **Como foi realizada a previsão:**
    
    A previsão foi feita usando o modelo de séries temporais `Prophet`, que analisa o histórico de distâncias percorridas ao longo do tempo e gera uma projeção para os próximos dois anos. A linha azul no gráfico representa a previsão de distância percorrida, enquanto a área sombreada em laranja indica a faixa de incerteza, que varia com base nos dados históricos e nas tendências observadas.
    """)

# Eficiência da Frota (Histórico)
st.subheader("Eficiência da Frota - Histórico")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x="Distância Percorrida (km)", y="Custo de Combustível (R$)", data=df_filtrado, ax=ax)
ax.set_title("Distância Percorrida vs. Custo de Combustível (Histórico)")
ax.set_xlabel("Distância Percorrida (km)")
ax.set_ylabel("Custo de Combustível (R$)")
st.pyplot(fig)

# Alerta
st.warning("Os dados de previsão são baseados em simulação e podem não refletir a realidade. Ajuste o modelo conforme necessário!")
