import dash
from dash import dash_table, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px


import pandas as pd



def gapminder_filter(year, continent):
    df = px.data.gapminder().query(f'(year == {year}) & (continent == "{continent}")')
    df['lifeExp'] = df['lifeExp'].round(0)
    return df



year_options = [dict(label=x, value=x) for x in px.data.gapminder()['year'].unique()]
continent_options = [dict(label=x, value=x) for x in px.data.gapminder()['continent'].unique()]


dd_year = [html.Label("Year", 
                      className = 'dropdown-label'), 
           html.Div(children=[
               dcc.Dropdown(id="dd_year", 
                            placeholder="Year...",  
                            options=year_options, 
                            value=year_options[0]['value'],
                            multi=False,
                            style = {'color':'#0033a0'})]
                    )
           ]


dd_continent = html.Div(id= 'dd_continent_div',
                        children= [html.Label("Continent", 
                                              className = 'dropdown-label'), 
                                   dcc.Dropdown(id="dd_continent", 
                                                placeholder="Continent...",  
                                                options=continent_options, 
                                                value=continent_options[0]['value'],
                                                multi=False,
                                                style = {'color':'#0033a0'})
                                   ]
                        )


title = html.H1('Table from Graph',
                className= 'titre-label-h2')



graph = dcc.Graph(id='graph',
                  config = {'displaylogo': False}
                  )


table = dash_table.DataTable(id='table', 
                             columns=[{'id': i,
                                       'name': n,
                                       'type': 'numeric', 
                                       'format': dict(specifier=',', 
                                                      locale=dict(group=' ', 
                                                                  grouping=[3])
                                                      )
                                       } for i, n in zip(['hovertext', 'x', 'y', 'marker.size'], 
                                                         ['Country', 'Population', 'Life_exp', 'gdpPercap'])],
                             export_format='xlsx',
                             export_headers='display',
                             fixed_rows={'headers':True, 'data':0},
                             style_header={'backgroundColor': '#5c5c5c',
                                           'fontWeight': 'bold',
                                           'minWidth': '120px',
                                           'textAlign': 'center',
                                           'color': 'white',
                                           'whiteSpace': 'normal', 
                                           'height': 'auto'},
                             
                             style_cell={'border': '2px solid black',
                                         'minWidth': '120px',
                                         'maxWidth': '300px',
                                         'textAlign': 'right',
                                         'whiteSpace': 'normal', 
                                         'height': 'auto'},
                             
                             sort_action='native',
                             
                             #page_size=14,
                             
                             style_table={'minWidth': '100%',
                                          'overflowY': 'auto',
                                          'overflowX': 'auto',
                                          'max-height': '1200px'}
                             )

# =============================================================================
# App 
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Dash Tips'

# =============================================================================
# Layout
# =============================================================================

app.layout = html.Div(children=[
    
    dbc.Row([
        dbc.Col(
            title,
            width={'size':4}
        )
        ]),
    
    dbc.Row([
        dbc.Col(
            dd_year,
            width={'size':2}
        ),
        dbc.Col(
            dd_continent,
            width={'size':2}
        )
        ]),
    
    dbc.Row([
        dbc.Col(
            graph,
            width={'size':8}
        ),
        dbc.Col(
            html.Div(id= 'table_row'),
            width={'size':4},
            align="center"
        )
        ])
    ],
    className='layout'
)


# =============================================================================
# Callback
# =============================================================================

#Display Table
@app.callback(Output('table_row', 'children'),
              [Input('graph', 'selectedData')])
def show_layout_table(selectedData):
    try:
        len( pd.DataFrame.from_dict(selectedData['points'])['x']) > 0
        return table
    except:
        return None

        

#Graph
@app.callback(Output('graph', 'figure'),
              [Input('dd_year', 'value'),
               Input('dd_continent', 'value')])
def graph_scatter(year, continent):
    return px.scatter(gapminder_filter(year, continent).round(2),
                      x= 'pop',
                      y= 'lifeExp',
                      hover_name= 'country',
                      hover_data=['country'],
                      size= 'gdpPercap',
                      color= 'gdpPercap',
                      color_continuous_scale= 'RdYlGn',
                      template= 'none',
                      height=700
                      )



#Table
@app.callback(Output('table', 'data'),
              [Input('graph', 'selectedData')])
def table_select(selectedData):
    return selectedData['points']



# Run app

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port='8050', debug=False)