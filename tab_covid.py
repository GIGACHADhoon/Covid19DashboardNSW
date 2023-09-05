from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
from datetime import datetime,date
from cpthOne import cpthOne

fig_object = cpthOne()
tab_covid = dbc.Container(
    [
        html.H1("Confirmed Cases Dashboard for NSW by LGA", style={'textAlign': 'center'}),
        html.P('Date Range of Dashboard is between 2020/1/25 and 24/8/2023'),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                    html.Div(children=[
                    html.H4("Please Read"),
                    html.P("Please use this Chloropleth Map to visualize the density of the Confirmed Cases by LGA"),
                    html.P("To best utilize this dashboard, please do the following:"),
                    html.Ul(
                        [
                        html.Li("Select a Date Range on the Right"),
                        html.Li("Select an LGA in the Choropleth Map"),
                        html.Li("A brief description of the selected LGA and dates is shown below the Date Range Picker"),
                        html.Li("View the Line Graphs of the Chosen & Neighbouring LGAs within the chosen date Range"),
                        ],style={'text-align': 'left'}
                    )
            ],className="text-center p-3 border"),width=6),
            dbc.Col(
                html.Div(
                    [   
                        html.Div([
                        html.H4("Pick a Date Range"),
                        dcc.DatePickerRange(
                                id='my-date-picker-range',
                                min_date_allowed=date(2020, 1, 25),
                                max_date_allowed=date(2023, 8, 24),
                                calendar_orientation='vertical',
                                style={"margin-bottom": "15px", "width": "100%"},  # Make the date picker width 100%
                            )],className="text-center p-3 border"),
                            html.Div(
                            children=[
                                html.H4('Selection Summary'),
                                html.P(id = 'selected_message')
                            ],className="text-center p-3 border") 
                        ],
                className="text-center p-3 border")
            ,width=6),   
        ],align="center",justify="center",), # Center horizontally
        html.Br(),
        html.Div(children = [
        dbc.Row([
                dbc.Col(
                    html.Div(
                        children=[
                            html.H4('NSW Confirmed Cases Choropleth Map'),
                            dcc.Graph(id='geo_nsw'),
                        ]
                    ,className="text-center p-3 border"),
                    width=12,  # Adjust column width and order
                ),
            ],
            align="center",
            justify="center",  # Center horizontally
        ),
        html.Div(id = 'neighborPlots',className="text-center p-3 border")],className="text-center p-3 border"),
        html.Br()
    ],
    fluid=True,
    style={'background-color': '#f0f0f0', 'textAlign': 'center', 'padding': '20px', 'margin': '0',
           'height': '100vh', 'overflow': 'auto'},  # Adjust margin, set height, and enable overflow
)   

@callback(
Output('geo_nsw', 'figure'),
Input('geo_nsw', 'clickData'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'))
def update_figure(clickData,start_date,end_date):
    if clickData:
        location = clickData['points'][0]['location']
    else:
        location = None
    return fig_object.get_figure(location,start_date,end_date)

@callback(
Output('selected_message', 'children'),
Input('geo_nsw', 'clickData'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'))
def update_card(clickData,start_date,end_date):
    if (not clickData and start_date and end_date):
        summation = "{:,}".format(fig_object.get_sum(None,start_date,end_date))
        return f'In all Local Government Area there was a total of  {summation} \
            Confirmed Covid Cases From the {datetime.strptime(start_date,"%Y-%m-%d").strftime("%d/%m/%Y")} to {datetime.strptime(end_date,"%Y-%m-%d").strftime("%d/%m/%Y")} \
                inclusive.' 
    elif (clickData and start_date and end_date):
        location = clickData['points'][0]['location']
        summation = "{:,}".format(fig_object.get_sum(location,start_date,end_date))
        return f'In the {fig_object.get_lga(location)} Local Government Area there was a total of  {summation} \
            Confirmed Covid Cases From the {datetime.strptime(start_date,"%Y-%m-%d").strftime("%d/%m/%Y")} to {datetime.strptime(end_date,"%Y-%m-%d").strftime("%d/%m/%Y")} \
                inclusive.'
    else:

        if clickData:
            location = clickData['points'][0]['location']
            summation = "{:,}".format(fig_object.get_sum(location,'2020-01-25','2023-08-24'))
            return f'In the {fig_object.get_lga(location)} Local Government Areas there was a total of  {summation} \
                Confirmed Covid Cases From the {datetime.strptime("2020-01-25","%Y-%m-%d").strftime("%d/%m/%Y")} to {datetime.strptime("2023-08-24","%Y-%m-%d").strftime("%d/%m/%Y")} \
                    inclusive.' 
        else:
            summation = "{:,}".format(fig_object.get_sum(None,'2020-01-25','2023-08-24'))
            return f'In all Local Government Areas there was a total of  {summation} \
                Confirmed Covid Cases From the {datetime.strptime("2020-01-25","%Y-%m-%d").strftime("%d/%m/%Y")} to {datetime.strptime("2023-08-24","%Y-%m-%d").strftime("%d/%m/%Y")} \
                    inclusive.' 
    
@callback(
Output('neighborPlots', 'children'),
Input('geo_nsw', 'clickData'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'))
def update_history(clickData,start_date,end_date):
    if clickData:   
        location = clickData['points'][0]['location']
        neighbors = fig_object.get_neighbors(location)['lgaCode']
        subplot_divs = []
        # get location
        fig = fig_object.get_history(location,start_date,end_date)
        subplot_divs.append(
            dbc.Col(
                dcc.Graph(
                    id=f'subplot-{location}',
                    figure=fig
                ),width = 3)
            )
        # get neighbors
        for neighbor in neighbors:
            fig = fig_object.get_history(neighbor,start_date,end_date)
            subplot_divs.append(
                dbc.Col(
                    dcc.Graph(
                        id=f'subplot-{neighbor}',
                        figure=fig
                    ),width = 4)
            )
        
        subplots_row = dbc.Row(subplot_divs,align="center",justify="center")

        return [html.H4("Confirmed Cases of Chosen & Neighbouring LGAs"),subplots_row]
    else:
        # Display the original graph
        original_graph = dbc.Col(
            dcc.Graph(
                id='original',
                figure=fig_object.get_history(None, start_date, end_date)
            ), width=6
        )
        return [html.H4("Confirmed Cases of ALL LGAs"),dbc.Row([original_graph],align="center",justify="center")]