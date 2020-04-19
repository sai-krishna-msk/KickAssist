import os
import time
from random import randint
import flask 
import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
import joblib
from ml_model.model import KickModel
import dash_bootstrap_components as dbc
from utils import get_dict , get_curr , build_plot ,get_predict, sample_campaign


server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
StyleSheets = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css","https://codepen.io/chriddyp/pen/brPBPO.css",dbc.themes.BOOTSTRAP ]
app = dash.Dash(__name__, external_stylesheets=StyleSheets, server = server)


model_oh = joblib.load('./ml_model/estimators/model_oh.sav')
model_hel = joblib.load('./ml_model/estimators/model_hel.sav')
encoder_oh = joblib.load('./ml_model/estimators/encoder_oh.sav')
encoder_hel = joblib.load('./ml_model/estimators/encoder_hel.sav')
encoder_label = joblib.load('./ml_model/estimators/encoder_label.sav')
prev_clicks=0
prev_resp =None





categories = get_dict([each[0] for each in pd.read_csv("data/category_data.csv", header =None).values])
sub_categories = get_dict([each[0] for each in pd.read_csv("data/sub_category_data.csv", header =None).values])
country = get_dict([each[0] for each in pd.read_csv("data/country_data.csv",  header =None).values])
currency_arr = [each[0] for each in pd.read_csv("data/currency_data.csv",  header =None).values]
currency_country_arr = [each[0] for each in pd.read_csv("data/currency_country_data.csv", header =None).values]
currency = get_curr(currency_arr , currency_country_arr)



app.layout = html.Div(style={'background-color':'white'}, children=[

    dbc.Jumbotron([

    html.H1(children="KickAssist", style={"color":"white"}),
    html.P(children="""An Interface enabling you to make data driven decisions about your campaign""", style={"color":"white"},className="lead"),
     html.Hr(className="my-2", style={"color":"white"}),
     html.P(
            children ="""Dashboard is a part of Data Science Project to help Kickstarter Creators to maximize their proabability of success, For further details 
            and process click below"""
        , style={"color":"white"}),
      html.P(dbc.Button("Learn more", color="primary", href='http://github.com/sai-krishna-msk/KickAssist'), className="lead")
    ],style={'background-color':'#195190'}),

    dbc.Row([
         dbc.Col(html.Label("Select Launched Date"), style={'font-size': 25, 'font-style':'italic', 'margin-left':15}),
         dbc.Col(html.Label("Select Date of Deadline"), style={'font-size': 25, 'font-style':'italic'}),
         dbc.Col(html.Label("Enter the Goal of the Campaign"), style={'font-size': 25, 'font-style':'italic'}),


        ]
        ),

    dbc.Row([
        dbc.Col(dcc.DatePickerSingle(
        id='launch-date',
        date=sample_campaign["launch_date"]), 
        style={'margin-left':20}),

         dbc.Col(dcc.DatePickerSingle(
        id='deadline-date',
        date=sample_campaign["deadline"])),
         dbc.Col(dcc.Input(
        id='goal',
        placeholder='Enter a value...',
        type='number',
        value=sample_campaign["goal"],
        style={'width':100, 'height':40})),
        

        ]
        ),
    html.Br(),

    dbc.Row([
         dbc.Col(html.Label("Select the Category", style={'font-size': 25, 'font-style':'italic', 'margin-left':15})),
        dbc.Col(html.Label("Select the Sub Category"), style={'font-size': 25, 'font-style':'italic', 'margin-left':15}),

        ],
        justify="around",
        ),


    dbc.Row([

        dbc.Col(dcc.Dropdown(
        id='category',
        options=categories,
        value=sample_campaign["category"],
        style={'margin-left':10})), 
        dbc.Col( dcc.Dropdown(
        id='subcategory',
        options=sub_categories,
        value=sample_campaign["sub_category"])),
        ]),
    html.Br(),

     dbc.Row([
         dbc.Col(html.Label("Select the Currency",  style={'font-size': 25, 'font-style':'italic', 'margin-left':15})),
        dbc.Col(html.Label("Enter the Country from which the Campaign is being registerd"), style={'font-size': 25, 'font-style':'italic', 'margin-left':15}),

        ]
        ),

     dbc.Row([
        dbc.Col(dcc.Dropdown(
        id='currecy',
        options=currency,
        value=sample_campaign["currency"],
        style={'margin-left':10})), 
        dbc.Col(dcc.Dropdown(
        id='country',
        options=country,
        value=sample_campaign["country"])),
        ]),
     html.Br(),

      dbc.Row([
         dbc.Col(html.Label("Enter the Description of the Campaign",  style={'font-size': 25, 'font-style':'italic', 'margin-left':15})),
        dbc.Col(  html.Label("Enter comma seperated values for Rewards", style={'font-size': 25, 'font-style':'italic', 'margin-left':15})),

        ]
        ),

      dbc.Row([
        dbc.Col(dcc.Textarea(
        id='description',
        placeholder='Enter a value...',
        value=sample_campaign["description"],
        style={'width': '80%','margin-left':20})),

        dbc.Col(
           dcc.Input(
        id='rewards',
        placeholder='Enter a value...',
        type='text',
        value=sample_campaign["rewards"], 
        style={'width':500, 'height':50})),

        ]),
      html.Br(),
   
      dbc.Row([



        dbc.Col(
             dbc.Button(id='pred', 
        children ='Predict', 
         outline=True, 
         color="primary", 
         className="mr-1",
        style= {'fontSize':24, 'margin-left': 920}
        )


            )

        ], justify='center'),

      dbc.Row([
        dbc.Col(id='scroll-down')

        ]),



   


   
    html.Div(id='output-graph')
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id = 'pred', component_property = 'n_clicks'),

       

        Input(component_id='launch-date', component_property='date'),
        Input(component_id='deadline-date', component_property='date'),
        Input(component_id='category', component_property='value'),
        Input(component_id='subcategory', component_property='value'),
        Input(component_id='currecy', component_property='value'),
        Input(component_id='country', component_property='value'),
        Input(component_id='goal', component_property='value'),
        Input(component_id='description', component_property='value'),
        Input(component_id='rewards', component_property='value'),
        ]

    
)
def update_graph(n_clicks,launch_date, deadline_date, category,subcategory, currency, country, goal, description, rewards):

    global prev_clicks
    global prev_resp
    if(n_clicks==None):
        return None
    elif(n_clicks<=prev_clicks):
        return prev_resp

    prev_clicks+=1

 

    pred_dict = get_predict(launch_date , deadline_date , goal , subcategory , category , currency , country , description, rewards)



    obj = KickModel(model_oh , model_hel , encoder_oh , encoder_hel , encoder_label)
    obj.load_data(pred_dict)
    obj.pred()
    pred_oh = (obj.pred_oh[0][1])*100
    pred_hel = (obj.pred_hel[0][1])*100
    pred_oh_df = obj.pred_oh_intr.round(3)
    pred_hel_df = obj.pred_hel_intr.round(3)
    plot_model = build_plot(pred_hel_df, pred_hel)

    prev_resp = plot_model
    return plot_model

@app.callback(
    Output(component_id='scroll-down', component_property='children'),
    [Input(component_id='sk', component_property='children')]
)
def update_scrollDown(children):
    return html.A(className="fa fa-arrow-down fa-3x",style={
        'margin-left': 950,
        'margin-top':20,
        'color':'#52A6FF'
        } )



    # return html.H4("Scroll down below", style={})


if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)