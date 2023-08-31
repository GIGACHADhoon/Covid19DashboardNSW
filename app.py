from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
from cpthOne import cpthOne
from datetime import date, datetime

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
fig_object = cpthOne()
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = dbc.Container([
        html.H1("Covid-19 Dashboard for NSW", style={'textAlign': 'center'}),
        html.H4("Displays the number of Confirmed Cases by Local Government Area", style={'textAlign': 'center'}),
        html.H6('Inbetween 5/1/2020 and 24/8/2023 Inclusive, there was a total number of 3,879,200 Confirmed Cases in NSW', style={'textAlign': 'center'}),
        html.Hr(),
        dbc.Row([
            dbc.Col(dcc.Graph(
                    id='geo_nsw',
                    ), width=8),
            dbc.Col(html.Div(children = [
                dbc.Card(
                        dbc.CardBody(
                            [
                            html.P(
                            "Pick the Data Range and click on the LGAs to Investigate",
                            className="card-text",)
                        ]),style={"width": "18rem"},),
                dcc.DatePickerRange(
                    id='my-date-picker-range',
                    min_date_allowed=date(2020, 1, 5),
                    max_date_allowed=date(2023, 8, 24),
                    calendar_orientation='vertical',
                    style={"margin-bottom": "15px"}),
                dbc.Card(
                        dbc.CardBody(
                            [
                            html.P("",id = "card_data_sum",
                            className="card-text text-center")
                        ]),style={"width": "18rem"},)
            ]), width=4)
            ],align="center"),
    ],fluid=True)

@callback(
Output('geo_nsw', 'figure'),
Input('geo_nsw', 'clickData'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'))
def update_figure(clickData,start_date,end_date):
    if clickData is not None:
        location = clickData['points'][0]['location']
        fig_object.update_sel(location)
    return fig_object.get_figure(start_date,end_date)

@callback(
Output('card_data_sum', 'children'),
Input('geo_nsw', 'clickData'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'))
def update_figure(clickData,start_date,end_date):
    if (start_date and end_date and clickData):
        summation = "{:,}".format(fig_object.get_sum(start_date,end_date))
        return f'In the {fig_object.get_lga()} Local Government Areas there was a total of  {summation} \
            Confirmed Covid Cases From the {datetime.strptime(start_date,"%Y-%m-%d").strftime("%d/%m/%Y")} to {datetime.strptime(end_date,"%Y-%m-%d").strftime("%d/%m/%Y")} \
                inclusive.'
    else:
        return ''