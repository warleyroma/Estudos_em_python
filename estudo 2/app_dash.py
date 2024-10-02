import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Limpeza de dados com regex=True para remover o símbolo R$ e as vírgulas
df['rent amount'] = df['rent amount'].str.replace(r'R\$', '', regex=True).str.replace(',', '').astype(float)
df['total'] = df['total'].str.replace(r'R\$', '', regex=True).str.replace(',', '').astype(float)

# Substituir valores não numéricos como "Sem info" e "Incluso" por NaN e depois converter para float
df['hoa'] = df['hoa'].str.replace(r'R\$', '', regex=True).str.replace(',', '')
df['hoa'] = df['hoa'].replace(['Sem info', 'Incluso'], np.nan).astype(float)

df['property tax'] = df['property tax'].str.replace(r'R\$', '', regex=True).str.replace(',', '')
df['property tax'] = df['property tax'].replace(['Sem info', 'Incluso'], np.nan).astype(float)

df['fire insurance'] = df['fire insurance'].str.replace(r'R\$', '', regex=True).str.replace(',', '').astype(float)

# Inicializar o app Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Aluguel de Imóveis: Análise de Dados"),
    
    html.Div([
        html.Label("Selecione a Cidade:"),
        dcc.Dropdown(
            id='city-filter',
            options=[{'label': city, 'value': city} for city in df['city'].unique()],
            value=None,
            multi=True,
            placeholder="Selecione uma ou mais cidades"
        )
    ]),
    
    dcc.Graph(id='area-rent-scatter'),
    
    html.Div([
        html.Div([dcc.Graph(id='furniture-pie')], style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Graph(id='animal-pie')], style={'width': '48%', 'display': 'inline-block'}),
    ]),
    
    dcc.Graph(id='rooms-rent-bar'),
])

# Callback para atualizar os gráficos
@app.callback(
    [Output('area-rent-scatter', 'figure'),
     Output('furniture-pie', 'figure'),
     Output('animal-pie', 'figure'),
     Output('rooms-rent-bar', 'figure')],
    [Input('city-filter', 'value')]
)
def update_dashboard(selected_cities):
    filtered_df = df if selected_cities is None else df[df['city'].isin(selected_cities)]
    
    scatter_fig = px.scatter(filtered_df, x='area', y='total', color='city', title="Área vs Valor Total")
    
    furniture_fig = px.pie(filtered_df, names='furniture', title="Imóveis Mobiliados")
    
    animal_fig = px.pie(filtered_df, names='animal', title="Aceitação de Animais")
    
    rooms_rent_fig = px.bar(filtered_df.groupby('rooms')['total'].mean().reset_index(),
                            x='rooms', y='total', title="Aluguel Médio por Número de Quartos")
    
    return scatter_fig, furniture_fig, animal_fig, rooms_rent_fig

# Rodar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
