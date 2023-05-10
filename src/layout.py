import dash_cytoscape as cyto
import dash_bootstrap_components as dbc
import json
from dash import dcc, html

def make_layout(styles, graph_layouts):
    cyto.load_extra_layouts()
    options = [{'label':val, 'value':val} for val in graph_layouts.keys()]
    tool_panel = dbc.Card(dbc.CardBody(dbc.Row([
        dbc.Col(dbc.Select(
            id='layout_select',
            placeholder=f"Layout ({options[0]['label']})", # options[0]['label']
            options=options,
        ), width=2),
        dbc.Col(dbc.RadioItems(
            id="mode_btn",
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {"label": name, "value": val} for val, name in enumerate(['Explore', 'Add/Remove edges', 'TBD'])
            ],
            value=0
        ), width=6),
        dbc.Col(
            dcc.Upload(dbc.Button('Upload Graph'), id='upload_graph'),
            width=2
        ),
        dbc.Col(
            dbc.Button('Download Graph', id='download_btn'),
            width=2
        ),
    ])))

    main_graph = dbc.Row(dbc.Col(
        html.Div(cyto.Cytoscape(
            id='cytoscape',
            elements=[],
            style=styles['cytoscape'],
            layout={'name': 'preset', 'directed': True},
            responsive=False,
            autoRefreshLayout=False,
            stylesheet=styles['stylesheet']
        ))
    ))

    meta = html.Div([
        #html.Div(id = 'last_clicked', style={'display':'none'}),
        html.Div(id='test'),
        dcc.Download(id='download'),
        dcc.Store(id='graph_elems'),
    ])

    layout = html.Div(dbc.Container([
        tool_panel,
        html.Br(),
        main_graph,
        html.Br(),
        meta,
    ]))
    return layout