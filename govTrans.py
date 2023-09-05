import pandas as pd 
import plotly_express as px
import plotly.graph_objs as go
from datetime import datetime, timedelta

def get_previous_day(x):

    # Convert the input date string to a datetime object
    x = datetime.strptime(x, '%Y-%m-%d')

    # Calculate the previous date by subtracting one day
    previous_date = x - timedelta(days=1)

    # Format the previous date as a string in the same format
    previous_date_str = previous_date.strftime('%Y-%m-%d')

    return previous_date_str

class govTrans:

    def __init__(self):
        self.df = pd.read_excel('nswGov.xlsx')
        self.df['Date'] = pd.to_datetime(self.df['Date'],format= "%Y%m%d")

    def line_case(self,st,ed):
        fig = go.Figure()
        if st and ed:
            filtered_df = self.df[(self.df.Date>=pd.to_datetime(st)) & (self.df.Date<=pd.to_datetime(ed))]
        else:
            filtered_df = self.df
        fig.add_trace(go.Scatter(x=filtered_df['Date'],y=filtered_df['ConfirmedCases']))
        fig.add_trace(go.Scatter(x=filtered_df['Date'],y=filtered_df['ConfirmedDeaths']))
        return fig


    def get_cols(self):
        return self.df.columns[1:26]
    
    def get_filtered_df(self,x):
        return self.df[self.df['Date'] == x]

    def get_deaths(self,x):
        return self.df[self.df['Date'] == x]['ConfirmedDeaths'].values[0] - self.df[self.df['Date'] == get_previous_day(x)]['ConfirmedDeaths'].values[0]

    def get_cases(self,x):
        return self.df[self.df['Date'] == x]['ConfirmedCases'].values[0] - self.df[self.df['Date'] == get_previous_day(x)]['ConfirmedCases'].values[0]
    