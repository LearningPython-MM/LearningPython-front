import dash_editor_components
import dash
from dash import html

import dash_core_components as dcc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_editor_components.PythonEditor(
        id='input'
    ),
    html.Br(),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Br(),
    html.Pre(id='my-output'),
    # html.Div(
    #     children=[
    #         html.Div(dcc.Graph(animate=True, id='graph-1'), className="six columns"),
    #         html.Img(
    #             src="https://t1.daumcdn.net/cfile/tistory/24283C3858F778CA2E",
    #             style={
    #                 'position': 'relative',
    #                 'top': '-400px',
    #                 'z-index': -1
    #             }
    #         )
    #     ]
    # ),
    # html.Img(
    #     src="https://png.pngtree.com/png-vector/20201112/ourmid/pngtree-cartoon-character-of-a-teen-png-image_2418571.jpg",
    #     id='player', 
    #     style={
    #         'height':'10%',
    #         'width':'10%',
    #         'position': 'relative',
    #         'top': '-400px',
    #         'z-index': 1
    #         }
    # )
])

@app.callback(
    Output('my-output', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input', 'value')
)
def update_output(n_clicks, value):
    a = [1,1,1,1,1,1,1]

    text = '{}'.format(value)
    exec(text, globals())
    a = solution(a)

    return 'return : {}'.format(a)

if __name__ == '__main__':
    app.run_server(debug=True)

def solution(a):
    alist = []

    for i in range(0, len(a), 1):
        if a[i] == 1:
            alist.append(i)
    
    return alist

# @app.callback(
#     Output('player', 'children')
# )
# def moveCharactor(alist):

    