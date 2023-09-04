import dash
from dash import callback
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import random

tab_gov =  html.Div([
    html.H1("Under Construction", style={'textAlign': 'center'}),
    html.Div(id='construction-text', children="👷‍♂️ Construction in Progress..."),
    dcc.Interval(
        id='construction-interval',
        interval=1000,  # Update every 1 second
        n_intervals=0
    ),
    html.Div(id='construction-animation', children=""),
])

# Callback to create a humorous animation
@callback(
    [Output('construction-animation', 'children'),
     Output('construction-text', 'children')],
    [Input('construction-interval', 'n_intervals')]
)
def update_animation(n_intervals):
    # Define a list of humorous emojis or messages
    animations = [
        "👷‍♂️👷‍♀️⚠️",
        "🔨🪚👷‍♂️",
        "🚧🏗️🛠️",
        "⚒️👷‍♀️🔧",
        "⛏️👷‍♂️👷‍♀️",
        "⚙️👷‍♂️🔩",
        "🧰🔨🚦",
    ]

    # Randomly select an animation and update the message
    random_animation = random.choice(animations)
    message = "👷‍♂️ Construction in Progress..."

    return random_animation, message