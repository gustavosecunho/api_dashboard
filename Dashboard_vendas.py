import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
import ipywidgets as widgets
import plotly.graph_objects as go
from IPython.display import display
from dash.dependencies import Input, Output

# Carregar o conjunto de dados
df = pd.read_excel('Base de Dados.xlsx')

# Convertendo a coluna 'Data_Pedido' para o tipo datetime
df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'])

# Mapeando os números de mês para nomes de mês
nome_mes = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}

# Extraindo o mês da coluna 'Data_Pedido' e mapeando para nomes de mês
df['Mês'] = df['Data_Pedido'].dt.month.map(nome_mes)


#1
#____________________
tm = df.groupby('Mês')['Valor_Total_Venda'].sum().reset_index()

fig1 = px.line(tm, x="Mês", y="Valor_Total_Venda",
               line_shape="spline", render_mode="svg",
               title="O Total de Vendas por Mês",
               labels={'Mês': 'Mês', 'Valor_Total_Venda': 'Total de Vendas'})

#____________________
fig2 = px.line(df, x="Mês", y="Valor_Total_Venda",
              color='Nome_Produto',
              line_shape="spline", render_mode="svg",
              title="Total de Vendida de um produto por Mês",
              hover_name='Nome_Produto',
              labels={'Mês': 'Mês', 'Valor_Total_Venda': 'Total de Vendas','Nome_Produto': 'Nome do Produto' })
#____________________
tm = df.groupby('Nome_Representante')['Valor_Total_Venda'].sum().reset_index()

fig3 = px.bar(tm, x="Nome_Representante", y="Valor_Total_Venda",
              title="Total de Vendas por Representante",
              labels={'Nome_Representante': 'Representante', 'Valor_Total_Venda': 'Total de Vendas'})
#____________________
fig4 = px.bar(df, x='Nome_Representante', y='Valor_Total_Venda',
             color='Nome_Produto', 
             title='Total de Vendas de um produto por Representante',
             hover_name='Nome_Produto',
             labels={'Nome_Representante': 'Representante', 'Valor_Total_Venda': 'Total de Vendas','Nome_Produto':'Nome do Produto'})

fig4.update_yaxes(showticklabels=False)
fig4.update_traces(marker_line_width=0)
#____________________
tp = df.groupby('Nome_Produto')['Valor_Total_Venda'].sum().reset_index()

# Criando a figura
fig5 = go.Figure(data=[go.Table(
    header=dict(values=["Produto", "Total de Vendas"]),
    cells=dict(values=[tp["Nome_Produto"], tp["Valor_Total_Venda"]]))
])

fig5.update_layout(
    title="Tabela de Total de Vendas por Produto"
)
                       
#__________________
fig6 = px.pie(df, values='Valor_Total_Venda', names='Regional', 
             title='Total de Vendas por Região',
             labels={'Regional': 'Região','Valor_Total_Venda': 'Total de Venda'  })
# Ajustando o layout para colocar a legenda ao lado
fig6.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
#__________________
te = df.groupby('Estado_Cliente')['Valor_Total_Venda'].sum().reset_index()

# Criando o gráfico de barras com Plotly Express
fig7 = px.bar(te, x='Estado_Cliente', y='Valor_Total_Venda',
             title='Total de Vendas por Representante',
             labels={'Estado_Cliente': 'Estado', 'Valor_Total_Venda': 'Total de Vendas'})
#__________________
fig8 = px.bar(df, x='Estado_Cliente', y='Valor_Total_Venda',
             color='Nome_Produto', 
             title='Total de Vendas De Produto por Representante',
             hover_name='Nome_Produto',
             labels={'Estado_Cliente': 'Estado', 'Valor_Total_Venda': 'Total de Vendas','Nome_Produto':'Nome do Produto' })
fig8.update_yaxes(showticklabels=False)
fig8.update_traces(marker_line_width=0);


#2-
#__________________
# Filtrando os dados para criar os gráficos
total_vendas_por_mes = df.groupby('Mês')['Valor_Total_Venda'].sum().reset_index()
total_vendas_por_representante = df.groupby('Nome_Representante')['Valor_Total_Venda'].sum().reset_index()
total_vendas_por_regional = df.groupby('Cidade_Cliente')['Valor_Total_Venda'].sum().reset_index()

# Define the figure for total_vendas_por_mes
fig9 = go.Figure(data=[go.Scatter(x=total_vendas_por_mes['Mês'],
                                  y=total_vendas_por_mes['Valor_Total_Venda'],
                                  mode='lines',
                                  name='fig1')],
                 layout=go.Layout(title='O Total de Vendas por Mês'))

# Define the figure for total_vendas_por_representante
fig10 = go.Figure(data=[go.Bar(x=total_vendas_por_representante['Nome_Representante'],
                               y=total_vendas_por_representante['Valor_Total_Venda'],
                               name='fig2')],
                  layout=go.Layout(title='O Total de Vendas por Representante'))

# Define the figure for total_vendas_por_regional
fig11 = go.Figure(data=[go.Scatter(x=total_vendas_por_regional['Cidade_Cliente'],
                                   y=total_vendas_por_regional['Valor_Total_Venda'],
                                   mode='lines',
                                   fill='tozeroy',
                                   name='fig3')],
                  layout=go.Layout(title='O Total de Vendas por Região'))




app = dash.Dash(__name__)

#3-4
#_________________

# Primeiro layout do aplicativo sem abas
layout_sem_abas = html.Div(children=[
    html.H1(children='Meu Dashboard Em PythonAnywhere'),
    html.Div(children=''' '''),
    dcc.Graph(id='total_mes', figure=fig1),
    dcc.Graph(id='total_mes_por_produto', figure=fig2),
    dcc.Graph(id='Total_Vendas_Representante', figure=fig3),
    dcc.Graph(id='Total_Vendas_produto_Representante', figure=fig4),
    dcc.Graph(id='Total_Vendas_produto', figure=fig5),
    dcc.Graph(id='Total_Vendas_Regiao', figure=fig6),
    dcc.Graph(id='Total_Vendas_Estado', figure=fig7),
    dcc.Graph(id='Total_Vendas_produto_Estado', figure=fig8)
])

# Segundo layout do aplicativo com abas
layout_com_abas =html.Div([
    html.H1("Filtragem Com Seleção de Abas"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Mês', value='tab-1'),
        dcc.Tab(label='Representante', value='tab-2'),
        dcc.Tab(label='Regional', value='tab-3'),
    ]),
    html.Div(id='tabs-content')
])

# Callback para atualizar o conteúdo com base na aba selecionada
@app.callback(
    dash.dependencies.Output('tabs-content', 'children'),
    [dash.dependencies.Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-1':
        return dcc.Graph(id='mes', figure=fig9)
    elif tab == 'tab-2':
        return dcc.Graph(id='representante', figure=fig10)
    elif tab == 'tab-3':
        return dcc.Graph(id='regiao', figure=fig11)


# Layout da aplicação
layout_dropdown = html.Div([
    html.H1("Análise De Vendas Da Cidade de um Estado"),
    html.Label('Estado'),
    dcc.Dropdown(
        id='estado-dropdown',
        options=[{'label': estado, 'value': estado} for estado in df['Estado_Cliente'].unique()],
        value=df['Estado_Cliente'].unique()[0]  # Valor padrão
    ),

    html.Label('Cidade'),
    dcc.Dropdown(id='cidade-dropdown'),

    dcc.Graph(id='sales-graph')
])

# Callback para atualizar as opções da dropdown de cidade com base no estado selecionado
@app.callback(
    Output('cidade-dropdown', 'options'),
    [Input('estado-dropdown', 'value')]
)
def update_city_options(selected_state):
    cities = df[df['Estado_Cliente'] == selected_state]['Cidade_Cliente'].unique()
    return [{'label': city, 'value': city} for city in cities]

# Callback para atualizar o gráfico com base no estado e cidade selecionados
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('estado-dropdown', 'value'),
     Input('cidade-dropdown', 'value')]
)
def update_sales_graph(selected_state, selected_city):
    filtered_data = df[(df['Estado_Cliente'] == selected_state) & (df['Cidade_Cliente'] == selected_city)]
    sales_data = filtered_data.groupby('Mês').agg({'Valor_Total_Venda': 'sum', 'Quantidade_Vendida': 'sum'}).reset_index()
    
    fig = px.bar(sales_data, x='Mês', y='Valor_Total_Venda', 
                 hover_data={'Quantidade_Vendida'},
                 labels={'Valor_Total_Venda': 'Total de Vendas', 'Quantidade_Vendida': 'Quantidade Vendida'},
                 title=f'Quantidade de Vendas por Mês em {selected_city}, {selected_state}')
    fig.update_xaxes(title='Mês da Venda')
    fig.update_yaxes(title='Valor Total Venda')
    return fig

# Layout principal combinando os dois layouts
app.layout = html.Div([layout_sem_abas, layout_com_abas,layout_dropdown ])

# Executando o servidor
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
