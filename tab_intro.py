from dash import html
import dash_bootstrap_components as dbc

intro_container_style = {
    'background-color': '#f0f0f0',
    'textAlign': 'center',
    'padding': '20px',
    'margin': '0',
    'height': '100vh',
}

content_container_style = {
    'max-width': '600px',
    'margin': '0 auto',
}

# Create a list of content elements
content = [
    html.H4("Aims & Shortcomings", style={'textAlign': 'center'}),
    html.P(
        "The Aim of this Dashboard is to be utilised as a resource for understanding "
        "the Behavior of Federal Government, NSW Government and citizens of NSW throughout the Covid-19 Pandemic"
    ),
    html.P(
        "One major shortcoming of this report is that Data Sources are not Synchronized by date, "
        "however the dates overlap majorly."
    ),
    html.P(
        "The Date Range of the Data Sources used for each Dashboard is mentioned below each Main Title"
    ),
    html.Hr(),
    html.H4("Data Sources", style={'textAlign': 'center'}),
    html.Ol(  # Ordered list for Data Sources
        [
            html.Li([
                "Data Source for the Confirmed Cases can be found ",
                html.A(
                    'here',
                    href='https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/distribution/dist-nsw-ckan-5d63b527-e2b8-4c42-ad6f-677f14433520/details?q=',
                    target='_blank',  # Open the link in a new tab
                )
            ]),
            html.Li([
                "Data Source to build the map in Confirmed Cases Tab can be found ",
                html.A(
                    'here',
                    href='https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.003July%202019?OpenDocument',
                    target='_blank',
                )
            ]),
            html.Li([
                "Data Source for the Vaccination Tab can be found ",
                html.A(
                    'here',
                    href='https://www.health.gov.au/resources/collections/covid-19-vaccination-vaccination-data?language=en',
                    target='_blank',
                )
            ]),
        ]
    ),
    html.Hr(),
    html.H4("Contact Information", style={'textAlign': 'center'}),
    html.P("For more information or assistance, please contact:"),
    html.P("Email: hkim9936@protonmail.com"),
]

tab_intro = dbc.Container(
    [
        html.H2("COVID-19 Dashboard Introduction", style={'textAlign': 'center'}),
        html.Hr(),
        html.Div(content, style=content_container_style),
    ],
    fluid=True,
    style=intro_container_style,
)