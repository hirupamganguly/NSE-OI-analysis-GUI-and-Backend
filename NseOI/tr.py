import dash_bootstrap_components as dbc
import dash
from dash import html
app=dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div(dbc.Row([
                    dbc.Col(html.Div("One of 1 columns")),
                    dbc.Col(html.Div("One of 2 columns")),
                ]))),
                    dbc.Col(html.Div("One of 3 columns")),
                ])
            ])
        ]),
        dbc.Col([
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div("One of 4 columns")),
                    dbc.Col(html.Div("One of 5 columns")),
                ])
            ])
        ])
    ])
    ])


if __name__ == '__main__':
    app.run_server(debug=True)