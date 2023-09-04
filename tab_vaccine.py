from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime,date
from vaxTrans import vaxTrans

vaxT = vaxTrans()

tab_vaccine = dbc.Container(
    [
        html.H1("Vaccination Dashboard for NSW by LGA", style={'textAlign': 'center'}),
        html.P('Date Range of Dashboard is between 2021/9/20 and 24/3/2023'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.Div(children=[
                    html.H4("Please Read"),
                    html.P("This Dashboard provides a view of the Population Coverage (%) for the 4 Covid-19 Vaccinations in NSW LGAs"),
                    html.P("Pick LGAs to compare on the right"),
                ], className="text-center p-3 border"),
                width=8),
            dbc.Col(
                html.Div(
                    children=[
                        html.H4("Pick Multiple LGAs to compare!"),  
                        dcc.Dropdown(
                            id='lgaPick',
                            options=vaxT.getLgas(),
                            value=['Albury', 'Hornsby'],
                            multi=True
                        ),
                    ]
                    , className="text-center p-3 border"),
                width=4),
        ], align="center", justify="center", ),  # Center horizontally
        html.Br(),
        html.Div(children=[
            html.H4("Population Coverage of Chosen LGAs by Vaccination"),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(id='doseLine1'),
                        ]
                        , className="text-center p-3 border"),
                    width=6,  # Adjust column width and order
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(id='doseLine2'),
                        ]
                        , className="text-center p-3 border"),
                    width=6,  # Adjust column width and order
                )
            ],
                align="center",
                justify="center",  # Center horizontally
            ),
            dbc.Row([
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(id='doseLine3'),
                        ]
                        , className="text-center p-3 border"),
                    width=6,  # Adjust column width and order
                ),
                dbc.Col(
                    html.Div(
                        children=[
                            dcc.Graph(id='doseLine4'),
                        ]
                        , className="text-center p-3 border"),
                    width=6,  # Adjust column width and order
                )
            ],
                align="center",
                justify="center",  # Center horizontally
            )],
            className="text-center p-3 border"),
    ],
    fluid=True,
    style={'background-color': '#f0f0f0', 'textAlign': 'center', 'padding': '20px', 'margin': '0',
           'height': '100vh', 'overflow': 'auto'},  # Adjust margin, set height, and enable overflow
)


@callback(
Output('doseLine1', 'figure'),
Output('doseLine2', 'figure'),
Output('doseLine3', 'figure'),
Output('doseLine4', 'figure'),
Input('lgaPick', 'value'))
def update_history(lgas):
    if lgas:
        return vaxT.updateFigure('dose1',lgas),vaxT.updateFigure('dose2',lgas),vaxT.updateFigure('dose3',lgas),vaxT.updateFigure('dose4',lgas)