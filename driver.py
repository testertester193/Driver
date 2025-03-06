import dash
from dash import dcc, html, Input, Output, State, ctx
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
from flask import Flask

# Generate last 30 days from today - 1
last_30_days = [(datetime.today() - timedelta(days=i+1)).strftime('%Y-%m-%d') for i in range(30)]

# Sample Data
transaction_data = pd.DataFrame({
    "Date": ["2025-02-01", "2025-02-02", "2025-02-03"],
    "Usage Category": ["Best", "Normal", "Worst"],
    "Cost": [5, 7, 10],
    "Amount Paid": [5, 5, 10]
})

# Dash App
external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div(style={'backgroundColor': '#2E2E2E', 'minHeight': '100vh', 'padding': '20px'}, children=[
     # Header Section with Logo
    html.Div([
        html.Nav([
            html.Div([
                html.Div([
                    html.Img(src="/assets/logo.png", style={"height": "50px"})
                ], style={"flex": "1", "textAlign": "left"}),
                html.Div([
                    html.Ul([
                        html.Li(html.A("Logout", id="user-menu", className="waves-effect waves-light btn red darken-3", style={"display": "none"}))
                    ], className="right")
                ], style={"flex": "1", "textAlign": "right"})
            ], style={"display": "flex", "alignItems": "center", "width": "100%"})
        ], className="nav-wrapper blue darken-3")
    ], className="container"),
    
    # Login Section
    html.Div(id='login-screen', children=[
        html.Div([
            html.H4("Login", className="center-align white-text"),
            html.Div([
                dcc.Input(id='username', type='text', placeholder='Enter username', className="input-field col s12"),
                dcc.Input(id='password', type='password', placeholder='Enter password', className="input-field col s12"),
                html.Button("Login", id='login-button', n_clicks=0, className="waves-effect waves-light btn green darken-3 col s12"),
                html.Div(id='login-output', className='red-text center-align mt-2')
            ], className="row")
        ], className="card-panel grey darken-3 white-text", style={"maxWidth": "400px", "margin": "auto", "padding": "20px"})
    ], className='container center-align', style={'marginTop': '100px'}),
    
    # Dashboard Content
    html.Div(id='dashboard-content', style={'display': 'none'}, children=[
        html.Div([
            html.Div("Battery Usage: 80%", className="card-panel blue darken-3 white-text center col s12 m4"),
            html.Div("Remaining Balance: £25", className="card-panel green darken-3 white-text center col s12 m4"),
            html.Div("Total Cost Last 30 Days: £150", className="card-panel red darken-3 white-text center col s12 m4")
        ], className="row"),
        
        # Graphs Section
        html.Div(style={'backgroundColor': '#1E1E1E', 'padding': '20px', 'borderRadius': '10px'}, children=[
            dcc.Graph(
                id='cost_chart',
                figure={
                    'data': [
                        go.Bar(x=["Best", "Normal", "Worst"], y=[50, 60, 40], marker_color=['darkgreen', 'gold', 'darkred'], name="Cost Over Last 30 Days")
                    ],
                    'layout': go.Layout(title="Cost Over Last 30 Days", xaxis_title="Usage Category", yaxis_title="Cost (£)", height=400, plot_bgcolor='#1E1E1E', paper_bgcolor='#1E1E1E', font=dict(color='white'))
                },
                className="col s12 m6"
            ),
            dcc.Graph(
                id='daily_cost_chart',
                figure={
                    'data': [
                        go.Bar(x=last_30_days, y=[20, 18, 25, 15, 12, 10, 22, 24, 19, 17, 14, 21, 18, 25, 15, 12, 10, 22, 24, 19, 17, 14, 21, 18, 25, 15, 12, 10, 22, 24], marker_color=['darkgreen', 'gold', 'darkred']*10, name="Daily Cost")
                    ],
                    'layout': go.Layout(title="Daily Cost Trend", xaxis_title="Date", yaxis_title="Cost (£)", height=400, plot_bgcolor='#1E1E1E', paper_bgcolor='#1E1E1E', font=dict(color='white'))
                },
                className="col s12 m6"
            )
        ], className="row"),
        
        # Transaction History
        html.Div([
            html.H4("Transaction History", className="center-align white-text"),
            html.Table([
                html.Thead(html.Tr([html.Th(col) for col in transaction_data.columns], className="grey darken-3 white-text")),
                html.Tbody([
                    html.Tr([html.Td(transaction_data.iloc[i][col]) for col in transaction_data.columns]) for i in range(len(transaction_data))
                ])
            ], className="striped centered white-text", style={"backgroundColor": "#2E2E2E", "borderRadius": "10px", "padding": "10px"})
        ], className="container")
    ], className='container')
])

# Login & Logout Functionality
@app.callback(
    [Output('dashboard-content', 'style'), Output('login-screen', 'style'), Output('user-menu', 'style')],
    [Input('login-button', 'n_clicks'), Input('user-menu', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login_logout(n_clicks, logout_clicks, username, password):
    if ctx.triggered_id == 'login-button' and n_clicks > 0:
        if username == "admin" and password == "password":
            return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    elif ctx.triggered_id == 'user-menu' and logout_clicks:
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
