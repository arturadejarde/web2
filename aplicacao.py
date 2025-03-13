import streamlit as st
import pandas as pd
import random
from faker import Faker
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Inicializando o Faker para gerar dados fictícios em português
fake = Faker('pt_BR')

# Lista com os 187 municípios de Pernambuco (apenas alguns exemplos para simplificação)
municipios_pernambuco = [
    'Afogados da Ingazeira', 'Afrânio', 'Agrestina', 'Águas Belas', 'Alagoinha', 'Aliança', 
    'Altinho', 'Amaraji', 'Angelim', 'Araripina', 'Arcoverde', 'Barra de Guabiraba', 'Barreiros', 
    'Belém de Maria', 'Belém de São Francisco', 'Belo Jardim', 'Betânia', 'Bezerros', 'Bodocó', 
    'Bom Conselho', 'Bom Jardim', 'Bonito', 'Brejão', 'Brejinho', 'Buique', 'Cabrobó', 'Cachoeirinha', 
    'Caetés', 'Calçado', 'Calumbi', 'Camaragibe', 'Campo Alegre', 'Canhotinho', 'Carnaíba', 'Carpina', 
    'Casinhas', 'Catende', 'Cedro', 'Chã Grande', 'Chã Preta', 'Cupira', 'Custódia', 'Dormentes', 
    'Escada', 'Exu', 'Feira Nova', 'Floresta', 'Frei Miguelinho', 'Garanhuns', 'Glória do Goitá', 
    'Iati', 'Ibiporanga', 'Ibirajuba', 'Igarassu', 'Ilha de Itamaracá', 'Inajá', 'Ipojuca', 'Ipubi', 
    'Itacuruba', 'Itambé', 'Itapetim', 'Itapissuma', 'Jaboatão dos Guararapes', 'Jaqueira', 'Jataúba', 
    'João Alfredo', 'Joaquim Nabuco', 'Jucati', 'Jupi', 'Jurema', 'Lagoa de Itaenga', 'Lagoa do Carro', 
    'Lagoa do Ouro', 'Lagoa Grande', 'Lajedo', 'Limoeiro', 'Macaparana', 'Machados', 'Manari', 'Maraial', 
    'Mirandiba', 'Moreilândia', 'Moreno', 'Nazaré da Mata', 'Olinda', 'Orobó', 'Ouro Preto', 'Palmares', 
    'Panelas', 'Paranatama', 'Parnamirim', 'Passira', 'Paudalho', 'Paulista', 'Pedra', 'Pesqueira', 
    'Petrolândia', 'Petrolina', 'Poção', 'Pombos', 'Primavera', 'Quipapá', 'Quixaba', 'Recife', 
    'Riacho das Almas', 'Ribeirão', 'Rio Formoso', 'Sairé', 'Salgadinho', 'Saloá', 'Sanharó', 
    'Santa Cruz da Baixa Verde', 'Santa Cruz do Capibaribe', 'Santa Maria da Boa Vista', 'Santa Terezinha', 
    'São Benedito do Sul', 'São Caitano', 'São João', 'São Joaquim do Monte', 'São José da Coroa Grande', 
    'São José do Belmonte', 'São Lourenço da Mata', 'São Vicente Férrer', 'Serra Talhada', 'Sertânia', 
    'Sirinhaém', 'Solidão', 'Surubim', 'Tabira', 'Tacaratu', 'Tamandaré', 'Taquaritinga do Norte', 'Toritama', 
    'Tracunhaém', 'Trindade', 'Triunfo', 'Tupanatinga', 'Tuparetama', 'Venturosa', 'Verdejante', 
    'Vertentes', 'Vicência', 'Vitoria de Santo Antão', 'Xexéu'
]

# Número de unidades que estamos simulando
num_unidades = 50

# Função para gerar dados fictícios para a tabela
def gerar_dados():
    unidades = []
    for i in range(num_unidades):
        unidade = {
            'ID_Unidade': i + 1,
            'Nome_Unidade': fake.company(),
            'Cidade': random.choice(municipios_pernambuco),  # Usando a lista de municípios
            'Macro_Region': random.choice(['Norte', 'Sul', 'Leste', 'Oeste']),
            'Data_Inicio_Instalacao': fake.date_between(start_date=datetime(2025, 1, 1), end_date=datetime(2025, 12, 31)),
            'Data_Treinamento_Iniciado': fake.date_between(start_date=datetime(2025, 6, 1), end_date=datetime(2026, 6, 30)),
            'Data_Treinamento_Concluido': fake.date_between(start_date=datetime(2025, 6, 1), end_date=datetime(2026, 12, 31)),
            'Status_Instalacao': random.choice(['Em andamento', 'Concluída', 'Pendente']),
            'Status_Treinamento': random.choice(['Em andamento', 'Concluído', 'Pendente']),
            'Avaliacoes_Realizadas': random.randint(0, 5),
            'Feedback_Avaliado': random.choice(['Positivo', 'Negativo', 'Neutro']),
            'Meta_Implementacao_2025': random.choice([True, False]),
            'Meta_Implementacao_2026': random.choice([True, False]),
            'Meta_Implementacao_2027': random.choice([True, False]),
            'Comentario_Avaliacao': fake.text(max_nb_chars=100),  # Comentário aleatório em português
        }
        unidades.append(unidade)
    return pd.DataFrame(unidades)

# Gerando os dados fictícios
df = gerar_dados()

# Título do Streamlit
st.title('Monitoramento da Implementação do Sistema em Pernambuco')

# Exibindo o DataFrame no Streamlit
st.subheader('Resumo das Unidades de Implementação')
st.dataframe(df)

# Mapa interativo com Folium
st.subheader('Mapa de Localização das Unidades')
m = folium.Map(location=[-8.0476, -35.8626], zoom_start=7)  # Centro de Pernambuco
marker_cluster = MarkerCluster().add_to(m)

# Adicionando os municípios ao mapa
for _, row in df.iterrows():
    folium.Marker(
        location=[random.uniform(-8.5, -7.5), random.uniform(-36.5, -34.5)],  # Coordenadas aproximadas
        popup=f"Unidade: {row['Nome_Unidade']}<br>Cidade: {row['Cidade']}<br>Status: {row['Status_Instalacao']}",
        icon=folium.Icon(color='blue')
    ).add_to(marker_cluster)

# Exibindo o mapa
st.write("Mapa de unidades implementadas em Pernambuco.")
folium_static(m)

# Filtros interativos
st.sidebar.subheader("Filtros de Pesquisa")

# Filtro por status da instalação
status_instalacao = st.sidebar.selectbox('Selecione o Status da Instalação', ['Todos', 'Em andamento', 'Concluída', 'Pendente'])
if status_instalacao != 'Todos':
    df = df[df['Status_Instalacao'] == status_instalacao]

# Filtro por status do treinamento
status_treinamento = st.sidebar.selectbox('Selecione o Status do Treinamento', ['Todos', 'Em andamento', 'Concluído', 'Pendente'])
if status_treinamento != 'Todos':
    df = df[df['Status_Treinamento'] == status_treinamento]

# Exibindo o DataFrame filtrado
st.subheader('Unidades Filtradas')
st.dataframe(df)

# Gráfico de progresso
st.subheader('Progresso da Implementação')
df_progresso = df[['ID_Unidade', 'Meta_Implementacao_2025', 'Meta_Implementacao_2026', 'Meta_Implementacao_2027']]
df_progresso.set_index('ID_Unidade', inplace=True)

# Soma do progresso por ano
df_progresso_sum = df_progresso.sum()

# Exibindo o gráfico de barras para o progresso de implementação por ano
st.bar_chart(df_progresso_sum)

# Exibindo o gráfico de avaliação
st.subheader('Avaliação das Unidades Concluídas')

# Função para criar estrelas
def estrelas(avaliacao):
    return '★' * avaliacao + '☆' * (5 - avaliacao)

# Exibindo avaliações para unidades concluídas
df_concluidas = df[df['Status_Instalacao'] == 'Concluída']
for _, row in df_concluidas.iterrows():
    st.write(f"**Unidade:** {row['Nome_Unidade']}")
    st.write(f"**Avaliação:** {estrelas(row['Avaliacoes_Realizadas'])}")
    st.write(f"**Comentário:** {row['Comentario_Avaliacao']}")
    st.write('---')