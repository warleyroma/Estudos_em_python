import pandas as pd
import plotly.express as px
import streamlit

# Load CSV file from GitHub
url = "https://raw.githubusercontent.com/warleyroma/Estudos_em_python/main/estudo%202/houses_to_rent.csv"
df = pd.read_csv(url)

# Preprocess the data
df['hoa'] = df['hoa'].str.replace(r'R\$', '', regex=True).str.replace(',', '').replace(['Sem info', 'Incluso'], 0).astype(float)
df['rent amount'] = df['rent amount'].str.replace(r'R\$', '', regex=True).str.replace(',', '').astype(float)
df['property tax'] = df['property tax'].str.replace(r'R\$', '', regex=True).str.replace(',', '').replace(['Sem info', 'Incluso'], 0).astype(float)
df['fire insurance'] = df['fire insurance'].str.replace(r'R\$', '', regex=True).str.replace(',', '').astype(float)

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='city-dropdown',
                options=[{'label': i, 'value': i} for i in df['city'].unique()],
                value=df['city'].unique()[0],
                placeholder="Select a city"
            ), width=3),
            dbc.Col(dcc.RangeSlider(
                id='rent-slider',
                min=df['rent amount'].min(),
                max=df['rent amount'].max(),
                value=[df['rent amount'].min(), df['rent amount'].max()],
                marks={i: str(i) for i in range(int(df['rent amount'].min()), int(df['rent amount'].max()), 1000)}
            ), width=9)
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='price-histogram'), width=6),
            dbc.Col(dcc.Graph(id='area-vs-rent'), width=6)
        ]),
    ], className="p-5")
])

# Callbacks
@app.callback(
    Output('price-histogram', 'figure'),
    Output('area-vs-rent', 'figure'),
    Input('city-dropdown', 'value'),
    Input('rent-slider', 'value')
)
def update_graphs(selected_city, rent_range):
    filtered_df = df[(df['city'] == selected_city) & 
                     (df['rent amount'] >= rent_range[0]) & 
                     (df['rent amount'] <= rent_range[1])]

    price_histogram = px.histogram(filtered_df, x='rent amount', nbins=20, title='Rent Distribution')
    area_vs_rent = px.scatter(filtered_df, x='area', y='rent amount', color='rooms', title='Area vs Rent')

    return price_histogram, area_vs_rent

if __name__ == '__main__':
    app.run_server(debug=True)
