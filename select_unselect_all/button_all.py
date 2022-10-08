import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



dd_options = [dict(label=l, value=v) for l, v in zip(['Blue', 'Green', 'Red', 'Brown', 'Yellow', 'Pink'],
                                                     [1, 2, 3, 4, 5, 6])]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    
    dbc.Row(
        dbc.Col(
        'DropDown exemple',
        className= 'titre-label-h2',
        width={'size':6}
        )),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id= 'dropdown',
                         placeholder= 'Colors...',
                         multi=True,
                         options=dd_options),
            
            html.Button(id= 'button',
                        n_clicks=0)
            ],
            width={'size': 4})
    ])
    
    
    ], className='layout')



@app.callback([Output('dropdown', 'value'),
               Output('button', 'children'),
               Output('button', 'className')],
              Input('button', 'n_clicks'))
def update_tous(n_clicks):
    if (n_clicks % 2) == 0:
        return None, 'Select (All)', 'buttonGreen'
    else:
        return [1, 2, 3, 4, 5, 6], 'Unselect (All)', 'buttonBlink'
    
    
    
if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port='8040',debug=False)