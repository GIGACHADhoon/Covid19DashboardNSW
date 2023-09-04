from dash import Dash,  dcc
import dash_bootstrap_components as dbc

from tab_covid import tab_covid
from tab_vaccine import tab_vaccine
from tab_intro import tab_intro
from tab_gov import tab_gov
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Tabs(
        [
            dcc.Tab(label="Introduction & Credits", children=[tab_intro]),
            dcc.Tab(label="Government Actions", children=[tab_gov]),
            dcc.Tab(label="Confirmed Cases", children=[tab_covid]),
            dcc.Tab(label="Vaccinations", children=[tab_vaccine]),
        ]
    )   
],
    fluid=True,
    style={'background-color': '#f0f0f0', 'textAlign'   : 'center', 'padding': '20px', 'margin': '0', 'height': '100vh', 'overflow': 'hidden'})

if __name__=="__main__":
    app.run()           