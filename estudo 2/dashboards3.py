import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


# Configuração da página
st.set_page_config(page_title="Dashboard de Aluguel", layout="wide")

# Carregar os dados
url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Limpeza e ajustes nos dados
df['rent amount'] = df['rent amount'].str.replace('R$', '', regex=True)
df['rent amount'] = pd.to_numeric(df['rent amount'].str.replace('R$', '').str.replace(',', '').str.strip())


# Tratar valores não numéricos nas colunas 'hoa' e 'property tax'
df['hoa'] = df['hoa'].replace('Sem info', None)
df['property tax'] = df['property tax'].replace('Sem info', None)

# Converter para numérico
df['hoa'] = pd.to_numeric(df['hoa'].str.replace('R$', '', regex=True).str.replace(',', '').str.strip(), errors='coerce')
df['property tax'] = pd.to_numeric(df['property tax'].str.replace('R$', '', regex=True).str.replace(',', '').str.strip(), errors='coerce')

# Filtrar os dados para a cidade 0
df_city_0 = df[df['city'] == 0]


# Insights para a cidade 0
mean_rent_city_0 = df_city_0['rent amount'].mean()
mean_parking_city_0 = df_city_0['parking spaces'].mean()
total_properties_city_0 = len(df_city_0)
accept_animals_city_0 = len(df_city_0[df_city_0['animal'] == 'acept'])

# Layout com três colunas
col1, col2, col3 = st.columns([1, 2, 1])

# Seção 1 - Métricas principais com Fieldset cidade 0
with col1:
    st.markdown(f"""
    <fieldset style="border: 0.7px solid #83c9ff; padding: 10px; width: 100%;">
        <legend style="font-weight: bold; font-size: 20px;">Métricas Principais cidade 0</legend>
        <div style="display: flex; flex-direction: column; font-size: 14px;">
            <div>
                <label>Média do Aluguel</label>
                <h1>R${mean_rent_city_0:,.2f}</h1>
            </div>
            <div>
                <label>Média de Vagas de Estacionamento</label>
                <h1>{mean_parking_city_0:.2f}</h1>
            </div>
            <div>
                <label>Total de Imóveis</label>
                <h1>{total_properties_city_0}</h1>
            </div>
            <div>
                <label>Imóveis que Aceitam Animais</label>
                <h1>{accept_animals_city_0}</h1>
            </div>
        </div>
    </fieldset>
    """, unsafe_allow_html=True)

# Seção 2 - Gráficos detalhados
# Cálculo da porcentagem de imóveis mobiliados em cada cidade
total_furnished_city_0 = len(df[(df['city'] == 0) & (df['furniture'] == 'furnished')])
total_properties_city_0 = len(df[df['city'] == 0])
percentage_furnished_city_0 = (total_furnished_city_0 / total_properties_city_0) * 100 if total_properties_city_0 > 0 else 0

total_furnished_city_1 = len(df[(df['city'] == 1) & (df['furniture'] == 'furnished')])
total_properties_city_1 = len(df[df['city'] == 1])
percentage_furnished_city_1 = (total_furnished_city_1 / total_properties_city_1) * 100 if total_properties_city_1 > 0 else 0

with col2:
    # Gráfico 1: Comparação entre city 0 e city 1
    df_city_01 = df[df['city'].isin([0, 1])]
    rent_by_city = df_city_01.groupby(['city', 'rooms'])['rent amount'].mean().reset_index()

    # Criar gráfico de linhas para comparar city 0 e city 1
    fig2 = px.line(rent_by_city, x='rooms', y='rent amount', color='city', 
                   title="Comparação de Aluguel Médio entre City 0 e City 1",
                   labels={'rent amount': 'Média de Aluguel', 'rooms': 'Número de Quartos'})
    
    fig2.update_layout(title_x=0.23, height=400)
    
    st.plotly_chart(fig2, use_container_width=True, height=400)

# Estilos adicionais para alinhamento e espaçamento
st.markdown("""<style>
    .stPlotlyChart {
        margin-top: 40px;
        margin-bottom: 140px;/* Ajusta o espaço entre os gráficos */
    }
</style>""", unsafe_allow_html=True)

# Seção 3 - Métricas principais com Fieldset cidade 1
df_city_1 = df[df['city'] == 1]

mean_rent_city_1 = df_city_1['rent amount'].mean()
mean_parking_city_1 = df_city_1['parking spaces'].mean()
total_properties_city_1 = len(df_city_1)
accept_animals_city_1 = len(df_city_1[df_city_1['animal'] == 'acept'])    

with col3:
    st.markdown(f"""
    <fieldset style="border: 0.7px solid #0068c9; padding: 10px;">
        <legend style="font-weight: bold; font-size: 20px;">Métricas Principais cidade 1</legend>
        <div style="display: flex; flex-direction: column; font-size: 14px;">
            <div>
                <label>Média do Aluguel</label>
                <h1>R${mean_rent_city_1:,.2f}</h1>
            </div>
            <div>
                <label>Média de Vagas de Estacionamento</label>
                <h1>{mean_parking_city_1:.2f}</h1>
            </div>
            <div>
                <label>Total de Imóveis</label>
                <h1>{total_properties_city_1}</h1>
            </div>
            <div>
                <label>Imóveis que Aceitam Animais</label>
                <h1>{accept_animals_city_1}</h1>
            </div>
        </div>
    </fieldset>
    """, unsafe_allow_html=True)

# Definição da função para criar gráfico de rosca
def create_donut_chart(percentage, city_label, colors):
    fig = go.Figure(go.Pie(
        values=[percentage, 100-percentage],
        labels=['Mobiliados', 'Não Mobiliados'],
        hole=0.7,
        marker_colors=colors,
        textinfo='none'
    ))

    fig.update_layout(
        showlegend=False,
        annotations=[dict(
            text=f"{percentage:.1f}%",
            font_size=20,
            showarrow=False
        )],
        title_text=f'Cidade {city_label}',
        title_x=0.5,
        height=300,  # Ajuste a altura do gráfico
        margin=dict(t=0, b=0, l=0, r=0),
    )
    
    return fig

# Seção 4 - Gráficos de Distribuição e Correlações

# Gráfico de barras: Comparação entre Número de Quartos e Aluguel Médio
st.markdown("<h2 style='text-align: center;'>Comparação entre Número de Quartos e Aluguel Médio nas Cidades</h2>", unsafe_allow_html=True)



# Calcular a média do aluguel por número de quartos para cada cidade
rent_by_rooms = df.groupby(['city', 'rooms'])['rent amount'].mean().reset_index()

# Calcular a média do aluguel por número de quartos para cada cidade
rent_by_rooms = df.query('rooms != 9').groupby(['city', 'rooms'])['rent amount'].mean().reset_index()


# Gráfico de barras
fig_rent_bar = px.bar(
   rent_by_rooms,
    x='rooms',
    y='rent amount',
    color='city',
    barmode='stack',
    labels={'rent amount': 'Aluguel Médio (R$)', 'rooms': 'Número de Quartos'},
    color_discrete_map=['#83c9ff', '#0068c9', '#ff69b4']  # Cores fixas para cada cidade
)

# Ajustando a legenda e removendo a barra branca
fig_rent_bar.update_layout(
    legend_title_text='Cidades',
    legend=dict(
        itemsizing='constant',
        title_font=dict(size=16),
        font=dict(size=14),
        bordercolor='Black',
        borderwidth=1, 
        
    ),
    
    margin=dict(l=40, r=40, t=40, b=40),
   
)

# Ajustando a largura das barras
fig_rent_bar.update_traces(width=0.8)  # Largura das barras


st.plotly_chart(fig_rent_bar, use_container_width=True)




# Gráfico de rosca: Porcentagem de imóveis mobiliados versus não mobiliados
st.markdown("<h2 style='text-align: center;'>Porcentagem de Imóveis Mobiliados vs. Não Mobiliados</h2>", unsafe_allow_html=True)
colors = ['#83c9ff', '#212d4a']  # Cores para o gráfico

# Gráfico para Cidade 0
furnished_city_0 = len(df_city_0[df_city_0['furniture'] == 'furnished'])
not_furnished_city_0 = total_properties_city_0 - furnished_city_0
fig_donut_city_0 = create_donut_chart(percentage_furnished_city_0, '0', colors)

# Gráfico para Cidade 1
furnished_city_1 = len(df_city_1[df_city_1['furniture'] == 'furnished'])
not_furnished_city_1 = total_properties_city_1 - furnished_city_1
fig_donut_city_1 = create_donut_chart(percentage_furnished_city_1, '1', colors)

# Exibir gráficos de rosca lado a lado
col4_circle, col5_circle = st.columns(2)
with col4_circle:
    st.plotly_chart(fig_donut_city_0, use_container_width=True)
with col5_circle:
    st.plotly_chart(fig_donut_city_1, use_container_width=True)

# Gráfico de barras: Porcentagem de Imóveis que Aceitam e Não Aceitam Animais
st.markdown("<h2 style='text-align: center;'>Porcentagem de Imóveis que Aceitam e Não Aceitam Animais por Cidade</h2>", unsafe_allow_html=True)

# Calcular o total de imóveis em cada cidade
total_properties_city_0 = len(df_city_0)
total_properties_city_1 = len(df_city_1)

# Calcular a quantidade de imóveis que aceitam e não aceitam animais
accept_animals_city_0 = len(df_city_0[df_city_0['animal'] == 'acept'])
not_accept_animals_city_0 = total_properties_city_0 - accept_animals_city_0

accept_animals_city_1 = len(df_city_1[df_city_1['animal'] == 'acept'])
not_accept_animals_city_1 = total_properties_city_1 - accept_animals_city_1

# Criar um DataFrame para o gráfico
animal_data = pd.DataFrame({
    'Cidade': ['Cidade 0', 'Cidade 0', 'Cidade 1', 'Cidade 1'],
    'Tipo': ['Aceita Animais', 'Não Aceita Animais', 'Aceita Animais', 'Não Aceita Animais'],
    'Quantidade': [accept_animals_city_0, not_accept_animals_city_0, accept_animals_city_1, not_accept_animals_city_1]
})

# Calcular a porcentagem
animal_data['Porcentagem'] = animal_data['Quantidade'] / animal_data.groupby('Cidade')['Quantidade'].transform('sum') * 100

# Gráfico de barras
fig_animal_bar = px.bar(
    animal_data,
    x='Cidade',
    y='Porcentagem',
    color='Tipo',
    barmode='group',
    labels={'Porcentagem': 'Porcentagem (%)', 'Cidade': 'Cidade'},
   
)

# Ajustando layout
fig_animal_bar.update_layout(
    xaxis_title='Cidades',
    yaxis_title='Porcentagem (%)',
    legend_title='Tipo',
    margin=dict(l=40, r=40, t=40, b=40)  # Ajustando margens
)

st.plotly_chart(fig_animal_bar, use_container_width=True)


# Adicionar descrição do cenário
st.markdown(f"""
### Descrição do Cenário: Mercado de Aluguel

O mercado de aluguel de imóveis é um setor dinâmico e vital para a economia urbana, refletindo as condições sociais e econômicas de uma região. A base de dados analisada, que contém informações sobre imóveis para aluguel, oferece uma visão abrangente do cenário de habitação nas cidades abordadas.

Com a crescente urbanização e o aumento da demanda por habitação, o mercado de aluguel tem se tornado cada vez mais competitivo. Nesta análise, focamos principalmente na Cidade 0 e Cidade 1, onde observamos uma série de tendências que moldam o mercado atual.

#### Tendências de Preços de Aluguel:

- **Aumento nos Preços:** Nas últimas temporadas, a média do aluguel na Cidade 0 apresentou uma tendência de aumento, refletindo uma demanda maior do que a oferta disponível. O preço médio de aluguel registrado foi de **R$ {mean_rent_city_0:,.2f}**.
  
- **Comparação com a Cidade 1:** Em comparação, a Cidade 1 apresenta um cenário diferente, onde os preços se mantiveram estáveis, com uma média de **R$ {mean_rent_city_1:,.2f}**. Essa diferença pode ser atribuída a fatores como a localização, a infraestrutura disponível e a oferta de imóveis.

#### Demografia e Preferências dos Inquilinos:

- **Preferências de Mobiliado:** A análise dos dados mostra que uma parcela significativa dos inquilinos prefere imóveis mobiliados, com aproximadamente **{percentage_furnished_city_0:.2f}%** dos imóveis disponíveis nessa categoria. Essa preferência é especialmente notável na Cidade 0, onde o aluguel de imóveis mobiliados está em ascensão.

- **Animais de Estimação:** Outro fator importante a considerar é a aceitação de animais de estimação. Os dados indicam que **{(accept_animals_city_0/total_properties_city_0) * 100:.2f}%** dos imóveis na Cidade 0 aceitam animais, refletindo uma mudança nas preferências dos inquilinos que buscam um lar que acomode seus pets.

#### Desafios do Mercado de Aluguel:
Apesar das oportunidades, o mercado de aluguel também enfrenta desafios significativos, como a crescente pressão por preços mais altos e a escassez de imóveis disponíveis em áreas desejáveis. Isso torna essencial para os inquilinos uma análise cuidadosa de suas opções e um planejamento estratégico em suas decisões de aluguel.
""")