# Librairies
import dash
from dash import dash_table
from dash import html, dcc, ctx
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import plotly.express as px

import pandas as pd
import json

from style import style_data, style_cell, style_table, style_header



df = px.data.gapminder()

fig_1 = px.scatter(df.query("year == 1972"),
                            x= 'pop',
                            y= 'lifeExp',
                            color= 'continent',
                            title= '1972',
                            custom_data= ['country'],
                            template= 'simple_white')

fig_1.update_layout(clickmode='event+select', 
                    dragmode='select',
                    margin=dict(l=20, r=20, t=40, b=5))



fig_2 = px.scatter(df.query("year == 2007"),
                            x= 'pop',
                            y= 'lifeExp',
                            color= 'continent',
                            title= '2007',
                            custom_data= ['country'],
                            template= 'simple_white')

fig_2.update_layout(clickmode='event+select', 
                    dragmode='select',
                    margin=dict(l=20, r=20, t=40, b=5))



graph_1 = dcc.Graph(id='graph_1',
                    figure= fig_1,)

graph_2 = dcc.Graph(id='graph_2',
                    figure= fig_2)


table_1 = dash_table.DataTable(id='table_1',
                               style_data= style_data,
                               style_cell= style_cell,
                               style_table= style_table,
                               style_header= style_header
                               )

table_2 = dash_table.DataTable(id='table_2',
                               style_data= style_data,
                               style_cell= style_cell,
                               style_table= style_table,
                               style_header= style_header
                               )



# =============================================================================
# App 
# =============================================================================

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



# =============================================================================
# Layout
# =============================================================================

app.layout = html.Div(children=[

    dbc.Row([
            dbc.Col([graph_1,
                     html.Br(),
                     table_1],
                    width={'size':6},
                    className= 'col_for_test'),
            dbc.Col([graph_2,
                     html.Br(),
                     table_2],
                    width={'size':6},
                    className= 'col_for_test')
        ]),
    
    html.Div(id= 'test_div'),
    
    dcc.Store(id= 'fig_selection_store')
    
    ])



# =============================================================================
# Callback
# =============================================================================  

### STORE ###

@app.callback(Output('fig_selection_store', 'data'),
              [Input('graph_1', 'relayoutData'),
               Input('graph_2', 'relayoutData')],
              State('fig_selection_store', 'data')
              )
def selection_store_cb(relayoutData_1, relayoutData_2, prev_selections):
    
    last_input = ctx.triggered_id

    if last_input == 'graph_1':
        relayoutData =  relayoutData_1
    elif last_input == 'graph_2':
        relayoutData =  relayoutData_2    

    
    keys_list_select = ['x0', 'y0', 'x1', 'y1']
    keys_list_move = ['selections[0].x0', 'selections[0].y0', 'selections[0].x1', 'selections[0].y1']
        
    try:
        selections = {k: relayoutData['selections'][0][k] for k in keys_list_select}
    except:
        try:
            selections = {k_name: relayoutData[k_val] for k_name, k_val in zip(keys_list_select, keys_list_move)}
        except:
            raise PreventUpdate
    
    if selections != prev_selections:
        return selections
    else:
        raise PreventUpdate
        



### GRAPH ###
    
@app.callback(Output('graph_1', 'figure'),
              [Input('fig_selection_store', 'data')])
def graph_1_cb(selections):
    
    fig = fig_1
    fig.update_layout(selections= [selections])
    
    return fig



@app.callback(Output('graph_2', 'figure'),
              [Input('fig_selection_store', 'data')])
def graph_2_cb(selections):
    
    fig = fig_2
    fig.update_layout(selections= [selections])
    
    return fig
        


### TABLE ###
    
@app.callback([Output('table_1', 'data'),
               Output('table_1', 'columns'),
               Output('table_2', 'data'),
               Output('table_2', 'columns')],
              [Input('graph_1', 'selectedData'),
               Input('graph_2', 'selectedData')])
def tables_cb(graph_1, graph_2):
    
    try:
    
        countries_1 = [graph_1['points'][i]['customdata'][0] for i in range(len(graph_1['points']))]
        countries_2 = [graph_2['points'][i]['customdata'][0] for i in range(len(graph_2['points']))]

        df_1 = df.query("(country == @countries_1) & (year == 2007)")[['country', 'pop', 'lifeExp']].sort_values('lifeExp',
                                                                                                                 ascending= False)
        df_2 = df.query("(country == @countries_2) & (year == 1972)")[['country', 'pop', 'lifeExp']].sort_values('lifeExp',
                                                                                                                 ascending= False)
        
        columns=[{'id': c,
                  'name': c, 
                  'type': 'numeric', 
                  'format': dict(specifier=',', 
                                  locale=dict(group=' ', grouping=[3]))
                  } for c in df_1.columns]
        
        
        return df_1.round().to_dict('records'), columns, df_2.round().to_dict('records'), columns
    
    except:
                
        raise PreventUpdate
    
    
# =============================================================================
# Run App
# =============================================================================

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port='8050', debug=False)