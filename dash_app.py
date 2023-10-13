import pandas as pd
import numpy as np
import os

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

data = pd.read_csv('europe_growth.tsv', sep='\t')
growth = data.iloc[[16,8,13,21],:].rename(columns={'freq,unit,s_adj,na_item,geo\TIME_PERIOD' : 'Countries'}).T\
             .iloc[1:,:].replace(to_replace=' p', value='', regex=True).rename(columns = {16 : 'France', 8 : 'Germany', 13 : 'Spain',21 : 'Italy'})

growth.index = growth.index.str.replace(" ", "", regex=True)
growth.index = pd.PeriodIndex(growth.index, freq='Q').to_timestamp()

growth['France'] = pd.to_numeric(growth['France'])
growth['Germany'] = pd.to_numeric(growth['Germany'])
growth['Spain'] = pd.to_numeric(growth['Spain'])
growth['Italy'] = pd.to_numeric(growth['Italy'])

growth_stack = growth.stack().reset_index().rename(columns = {'level_0' : 'date','level_1' : 'Country', 0 : 'growth'})

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Growth', style={'textAlign':'center'}),
    dash_table.DataTable(data=growth.reset_index().to_dict('records'), page_size=10, id=''),
    dcc.Dropdown(growth_stack.Country.unique(), 'France', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    growth_df = growth_stack[growth_stack.Country==value]
    return px.line(growth_df, x='date', y='growth')

if __name__ == '__main__':
    app.run(debug=True)
