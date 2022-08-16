import dash
from dash.dependencies import Output,Input
import dash_core_components as dcc
import dash_html_components as html
from random import random
import plotly

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Graph(id='live-update-graph-bar'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000
        )
    ])
)


@app.callback(Output('live-update-graph-scatter', 'figure'),
              [Input('interval-component', 'interval')])
def update_graph_scatter():

    traces = list()
    for t in range(2):
        traces.append(plotly.graph_objs.Scatter(
            x=[1, 2, 3, 4, 5],
            y=[(t + 1) * random() for i in range(5)],
            name='Scatter {}'.format(t),
            mode= 'lines+markers'
            ))
    return {'data': traces}

@app.callback(Output('live-update-graph-bar', 'figure'),
              [Input('interval-component', 'interval')])
def update_graph_bar():

    traces = list()
    for t in range(2):
        traces.append(plotly.graph_objs.Bar(
            x=[1, 2, 3, 4, 5],
            y=[(t + 1) * random() for i in range(5)],
            name='Bar {}'.format(t)
            ))
    layout = plotly.graph_objs.Layout(
    barmode='group'
)
    return {'data': traces, 'layout': layout}


if __name__ == '__main__':
    app.run_server(debug=True)
