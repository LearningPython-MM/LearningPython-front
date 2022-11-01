import dash_editor_components
import dash
from dash import html
from dash.dependencies import Input, Output, State

import io
import sys

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_editor_components.PythonEditor(
        id='input'
    ),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Pre(id='my-output')
])

@app.callback(
    Output('my-output', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input', 'value')
)

def update_output(n_clicks, value):
    sys.stdout = buffer = io.StringIO()
    
    map = [0, 0, 0, 0]

    exec('{}'.format(value))

    a = buffer.getvalue()

    return '{} \n\n {}'.format(a, a == "[0,0,0,0]")

if __name__ == '__main__':
    app.run_server(debug=True)
