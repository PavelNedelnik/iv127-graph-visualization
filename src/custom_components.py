import dash_bootstrap_components as dbc
from dash import html

def place_in_container(component_body:list):
    return html.Div([
        dbc.Card(
            dbc.CardBody(
                component_body
            ),
            color = 'dark',
        )
    ])