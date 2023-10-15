import pandas as pd
import numpy as np

from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px

data = pd.read_csv('europe_growth.tsv', sep='\t')
covid = pd.read_csv('owid-covid-data.csv',parse_dates=['date'])
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
server = app.server

fig1 = px.line(growth_stack, x='date', y='growth', color='Country', title='GROWTH')

fig2 = px.scatter(covid, x="human_development_index", y="gdp_per_capita",\
                 size="population", hover_name="location", color = "location" ,template='simple_white', size_max=100)
fig2.update_layout(
    height=500,
    title_text="GDP per Capita vs HDI"
) 

app.layout = html.Div([
    html.H1(children='Growth', style={'textAlign':'center'}),
    dcc.Graph(figure = fig1),
    dcc.Graph(figure = fig2)
])

if __name__ == '__main__':
    app.run(debug=True)
