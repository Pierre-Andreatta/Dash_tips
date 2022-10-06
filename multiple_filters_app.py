# Librairies
import dash
from dash import html
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import numpy as np

import calendar
import requests

from datetime import date

# =============================================================================
# Fonctions
# =============================================================================

#Options date

def annee_options():
    #201804
    start = 2018
    end = date.today().year
    return [i for i in range(start, end+1)]


def mois_options(annee):   
    if annee == date.today().year:
        if len(jour_options(annee, date.today().month)[0]) == 0:
            mois = [i for i in range(1, 13) if int(i) < int(date.today().month)]
        else:
            mois = [i for i in range(1, 13) if int(i) <= int(date.today().month)]
    elif annee == 2018:
        mois = [i for i in range(4,13)]
    else:
        mois = [i for i in range(1, 13)]
        
    return [i for i in mois]


def jour_options(annee, mois):
    response = list(requests.get(f"https://calendrier.api.gouv.fr/jours-feries/metropole/{annee}.json").json().keys())
    cal = np.array(calendar.monthcalendar(annee, mois))
    jours_semaine = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    dct = {}
    for i in range(0, len(cal)):    
        for k, j in zip(cal[i],jours_semaine):
            dct[k] = j   
            
    jours = [i for i in cal[np.where(cal[:,:-2] > 0)] if i not in [int(k[-2:]) for k in response if int(k[5:-3]) == int(mois)]]
    #Mois en cours
    if (int(annee) == int(date.today().year)) & (int(mois) >= int(date.today().month)):
        res = [i for i in jours if i < int(date.today().day)]
    else:
        res = jours
    
    options = [{'label': f'{i} - {j}','value': i} for i, j in zip(dct.keys(), dct.values()) if (i in res)]
    try:
        value = options[0]['value']
    except:
        value = None
        
    return options, value


# Jours ouvrés
def calendrier_jour_ouvrés(annee, mois):
    calendrier_mois = calendar.monthcalendar(annee, mois)
    
    #API jours fériés
    response = list(requests.get(f"https://calendrier.api.gouv.fr/jours-feries/metropole/{annee}.json").json().keys())
    
    #Calendrier du lundi au vendredi
    calendrier_mois_week = [i[:-2] for i in calendrier_mois]
    
    #Suppression des jours fériés
    for i in [int(i[-2:]) for i in [i[5:] for i in response if int(i[5:-3]) == mois]]:
        for k in range(len(calendrier_mois_week)):
            if i in calendrier_mois_week[k]:
                calendrier_mois_week[k].remove(i)
    
    return [i for l in calendrier_mois_week for i in l if i > 0]


def jour_ouvrés(annee, mois):
    return len(calendrier_jour_ouvrés(annee, mois))


def jour_ouvrés_cumul(annee, mois):
    return len([i for i in calendrier_jour_ouvrés(annee, mois) if i <= date['jour']])


#Exemple content
fig = px.scatter(px.data.gapminder().query('(year == 2002) & (continent == "Asia")'),
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

fig.update_layout({ 
    'plot_bgcolor': 'rgba(249, 254, 255, 1)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })


exemple_content = [html.Br(),
                   html.Br(),
                   dcc.Graph(figure=fig),
                   html.Br(),
                   html.Br()]


# =============================================================================
# col_options
# =============================================================================

col_annee = [dict(label=x, value=x) for x in annee_options()]
continents = [dict(label=x, value=x) for x in ['Asia', 'Africa', 'America', 'Europe', 'Oceania', 'Antarctica']]


# =============================================================================
# Style
# =============================================================================


# =============================================================================
# Components
# =============================================================================

# Selecteurs

dd_years = [html.Label("Year", 
                       className = 'dropdown-label'), 
            html.Div(children=[
                dcc.Dropdown(id="dd_years", 
                             placeholder="Year...",
                             
                             value=date.today().year,  
                             options=col_annee, 
                             multi=False,
                             style = {'color':'#0033a0'})]
                     )
            ]


dd_months = [html.Label("Month", 
                      className = 'dropdown-label'), 
           html.Div(children=[
               dcc.Dropdown(id="dd_months", 
                            placeholder="Month...",
                            value=1,
                            multi=False,
                            style = {'color':'#0033a0'})],
                    )
           ]


dd_days = html.Div([html.Label("Days", 
                      id='info_jour_ouvres',
                      className = 'dropdown-label'), 
           html.Div(children=[
               dcc.Dropdown(id="dd_days", 
                            placeholder="Days...",
                            multi=False,
                            style = {'color':'#0033a0'})],
                    )
           ], 
                   id='dd_days_div'
                   )


dd_country = html.Div([html.Label("Continents",
                      className = 'dropdown-label'), 
           html.Div(children=[
               dcc.Dropdown(id="dd_country", 
                            placeholder="Continent...",
                            value=continents[0],
                            options=continents,
                            multi=False,
                            style = {'color':'#0033a0'})],
                    )
           ], 
                   id='dd_country_div'
                   )




dd_graph_slider = [html.Br(), 
                   dcc.RangeSlider(id="dd_graph_slider", 
                                   min = 0,
                                   max = len(jour_options(2022, 8))-1,
                                   step = 1,
                                   marks = {k: v for k, v in zip(range(len(jour_options(2022, 8))), jour_options(2022, 8))},
                                   value = [1, 4]
                                   ),
                   html.Br(),
                   html.Br(),
                   dcc.Graph(figure=fig),
                   html.Br(),
                   html.Br()
                   ]


titre_head = 'Multiple filters'

# =============================================================================
# App 
# =============================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.title = 'Dash Tips'
server = app.server

# =============================================================================
# Layout
# =============================================================================
app.layout = html.Div(children=[
    
    dbc.Row([
        dbc.Col(
            titre_head,
            width={'size':6},
            className= 'titre-label-h2'
            )
        ]
        ),
    
    dbc.Row([
        dbc.Col(
            dd_years,
            width={'size':2}
            ),
        dbc.Col(
            dd_months,
            width={'size':2}
            ),
        dbc.Col(
            html.Div(id='filter'),
            width={'size':2}
            )
    ]),
    
    html.Br(),

    dbc.Card(
        dbc.Tabs(
        [
                dbc.Tab(exemple_content,
                        tab_id= 'tab_day', 
                        label="Tab day"),
                dbc.Tab(exemple_content,
                        tab_id= 'tab_continent', 
                        label="Tab continent"),
                dbc.Tab(dd_graph_slider,
                        tab_id= 'tab_slider',
                        label="Tab slider"),
            ],
        className='tabs_content_style',
        id= 'tabs'      
        ),
        className='card_content_style',
        id= 'cards'
    ), 
        
    ],
                      className='layout'   
    )


# =============================================================================
# Callback
# =============================================================================

# Style
     
@app.callback(Output('filter', 'children'),
              Input('tabs', 'active_tab'))
def filters(active_tab):
    if active_tab == 'tab_day':
        return dd_days
    elif active_tab == 'tab_continent':
        return dd_country
    else:
        return None
    
    
@app.callback(Output('info_jour_ouvres', 'children'),
              [Input('dd_days', 'value'),
               Input('dd_months', 'value'),
               Input('dd_years', 'value')])
def info_jour_ouvres(jour, mois, annee):  
    return f'Day ({jour_ouvrés_cumul(annee, mois)}/{jour_ouvrés(annee, mois)})'



# DropDown

@app.callback(Output('dd_months', 'options'),
              [Input('dd_years', 'value')])
def mois_options_update(annee):          
    return mois_options(annee)


@app.callback([Output('dd_days', 'options'),
               Output('dd_days', 'value')],
              [Input('dd_years', 'value'),
               Input('dd_months', 'value')])
def jour_options_update(annee, mois):        
    return jour_options(annee, mois)



@app.callback([Output('dd_graph_slider', 'max'),
               Output('dd_graph_slider', 'marks'),
               Output('dd_graph_slider', 'value')],
              [Input('dd_years', 'value'),
               Input('dd_months', 'value')])
def option_jour_slider(annee, mois):
    
    jours_update = jour_options(annee, mois)[0]
    jours_update_list = [jours_update[i]['value'] for i in range(len(jours_update))]
    
    marks = {k: v for k, v in zip(range(len(jours_update_list)), jours_update_list)}
    max = len(jours_update_list)-1
    value = [0, len(jours_update_list)-1]
    
    return max, marks, value


# Run app

if __name__ == '__main__':
    app.run_server(host= '0.0.0.0',port='8040', debug=False)
    