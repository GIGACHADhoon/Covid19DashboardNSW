from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from govTrans import govTrans
import numpy as np
import pandas as pd
from datetime import datetime,date

figure_object = govTrans()

tab_gov = dbc.Container(
    [
        html.H1("Government Action Dashboard for NSW", style={'textAlign': 'center'}),
        html.P('Date Range of Dashboard is between 2020/1/1 and 2020/12/31'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                html.Div(children=[
                    html.H4("Please Read"),
                    html.P("This Dashboard provides a view of the Government Actions with respect to the number of Confirmed Cases and Deaths in NSW due to Covid-19"),
                    html.P("To best utilize this dashboard, please do the following:"),
                    html.Ul(
                        [
                        html.Li("Select a Date Range on the Right"),
                        html.Li("Click on the line plot below corresponding to the date to investigate "),
                        html.Li("A brief description of the selected Date is shown below the Date Range Picker"),
                        html.Li("The latest announced government policies on that date are outlined below the line plot"),
                        ],style={'text-align': 'left'}
                    )
                ], className="text-center p-3 border"),width=8),
                dbc.Col(html.Div(
                    [   
                        html.Div([
                        html.H4("Pick a Date Range"),
                        dcc.DatePickerRange(
                                id='dpr',
                                min_date_allowed=date(2020, 1, 1),
                                max_date_allowed=date(2022, 12, 31),
                                calendar_orientation='vertical',
                                style={"margin-bottom": "15px", "width": "100%"},  # Make the date picker width 100%
                            )],className="text-center p-3 border"),
                            html.Div(
                            children=[
                                html.H4('Selection Summary'),
                                html.P(id = 'govt_message')
                            ],className="text-center p-3 border") 
                        ],
                className="text-center p-3 border"),width=4),
        ], align="center", justify="center", ),  # Center horizontally
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([dcc.Graph(id='casesdeaths',)], className="text-center p-3 border"),width = 12),
        ]),
        html.Div(id = 'policyCards',className="text-center p-3 border"),
        html.Br()
    ],
    fluid=True,
    style={'background-color': '#f0f0f0', 'textAlign': 'center', 'padding': '20px', 'margin': '0',
           'height': '100vh', 'overflow': 'auto'},  # Adjust margin, set height, and enable overflow
)

@callback(
Output('casesdeaths', 'figure'),
Input('casesdeaths', 'clickData'),
Input('dpr', 'start_date'),
Input('dpr', 'end_date'))
def update_figure(clickData,start_date,end_date):
    fig = figure_object.line_case(start_date,end_date)

    if clickData:   
        # add v_line
        selected_x = clickData['points'][0]['x']
        fig['layout'].update(
            shapes=[dict(
                type='line',
                x0=selected_x,
                x1=selected_x,
                y0=np.min(fig['data'][0]['y']),
                y1=np.max(fig['data'][0]['y']),
                xref='x',
                yref='y',
                line=dict(color='blue', width=2)
            )]
        )
    return fig

@callback(
Output('policyCards', 'children'),
Input('casesdeaths', 'clickData'))
def update_history(caseClick):
    if caseClick:
        selected_x = caseClick['points'][0]['x']
        subcards = []
        filtered_df = figure_object.get_filtered_df(selected_x)
        for col in figure_object.get_cols():
            if col != 'Date' and pd.notna(filtered_df[col].values[0]):
                subcards.append(
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([
                                html.H4(f'{col}', className="card-title"),
                                html.P(f'{filtered_df[col].values[0]}', className="card-text")
                            ]),
                            style={'margin': '10px', 'padding': '10px'}
                        ),
                        width={'size': 3}  # Four cards in each row
                    )
                )
        return [html.H4("Latest Announced Government Policies"),dbc.Row(subcards)]
    
@callback(
Output('govt_message', 'children'),
Input('casesdeaths', 'clickData'))
def update_card(clickData):
    if clickData:
        selected_x = clickData['points'][0]['x']
        deaths = figure_object.get_deaths(selected_x)
        cases = figure_object.get_cases(selected_x)
        return f'On {selected_x} there were {cases} cases and {deaths} deaths reported in NSW'
    else:
        return 'Please Click on the line on a Specific Date.'
