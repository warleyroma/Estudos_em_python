import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para layout "wide" e título
st.set_page_config(page_title="Dashboard de Aluguel", layout="wide")

# Carregar os dados
url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Remover 'R$' e converter a coluna 'rent amount' para numérico
df['rent amount'] = df['rent amount'].str.replace('R\$', '', regex=True)
df['rent amount'] = pd.to_numeric(df['rent amount'].str.replace(',', '').str.strip())

# Organizar os dados pela cidade
df = df.sort_values(["city"])

# Criar um filtro de cidade na barra lateral
city = st.sidebar.selectbox("Cidade", df["city"].unique())

# Filtrar os dados com base na cidade selecionada
df_filtered = df[df["city"] == city]

# Layout com três colunas para distribuir as visualizações
col1, col2, col3 = st.columns(3)

# Gráfico 1: Distribuição de valores de aluguel (Boxplot)
fig = px.box(df_filtered, y='rent amount', title=f"Distribuição de Aluguel em {city}",
             height=350)  # Ajuste de altura para caber na tela
col1.plotly_chart(fig, use_container_width=True)

# Gráfico 2: Comparação do aluguel médio por número de quartos
rooms_range = pd.DataFrame({'rooms': range(1, 11)})
rent_by_rooms = df_filtered.groupby('rooms')['rent amount'].mean().reset_index()
rent_by_rooms_full = rooms_range.merge(rent_by_rooms, on='rooms', how='left').fillna(0)

fig = px.bar(rent_by_rooms_full, x='rooms', y='rent amount', title="Média do Aluguel por Número de Quartos (1-10)",
             height=350)  # Reduzindo a altura do gráfico
col2.plotly_chart(fig, use_container_width=True)

# Gráfico 3: Correlação entre Aluguel e HOA (condomínio)
fig = px.scatter(df_filtered, x='hoa', y='rent amount', trendline="ols",
                 title=f"Correlação: Aluguel vs Condomínio em {city}", height=350)
col3.plotly_chart(fig, use_container_width=True)

# Segunda linha com mais três colunas
col4, col5, col6 = st.columns(3)

# Gráfico 4: Gráfico de pizza para animais permitidos
animal_counts = df_filtered['animal'].value_counts().reset_index()
animal_counts.columns = ['animal_status', 'count']

fig = px.pie(animal_counts, names='animal_status', values='count',
             title=f"Imóveis com e sem Animais Permitidos em {city}", height=350)
col4.plotly_chart(fig, use_container_width=True)

# Gráfico 5: Heatmap entre banheiros e vagas de estacionamento
heatmap_data = df_filtered.pivot_table(index='bathroom', columns='parking spaces', aggfunc='size', fill_value=0)

fig = px.imshow(heatmap_data, labels=dict(x="Vagas de Estacionamento", y="Banheiros", color="Contagem"),
                title=f"Relação entre Banheiros e Vagas de Estacionamento em {city}", height=350)
col5.plotly_chart(fig, use_container_width=True)

# Estilo adicional para ajustar a altura e manter tudo na viewport
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 10px;
            padding-bottom: 10px;
            padding-left: 0px;
            padding-right: 0px;
        }
        .css-18e3th9 {
            padding: 0px;
        }
        .element-container {
            margin-bottom: 5px;
        }
    </style>
    """, unsafe_allow_html=True)
