import numpy as np
import pandas as pd
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt

def get_dict(lis):
    resp = []
    for val in lis:
        resp.append({"label":val, "value":val})

    return resp

def get_curr(currency , currency_country):
    resp = []
    for currency , country in zip(currency , currency_country):
        resp.append({"label":country, "value":currency})

    return resp



def build_plot(pred_df,pred):
    x= pred_df["feature"].values
    measures  = ["relative" for i in range(len(x))]
    y_raw = (pred_df['weight']).values
    y=[y_raw[i] if(i==0) else y_raw[i]-y_raw[i-1] for i in range(len(y_raw))]
    mean_y = np.mean(y)
    text = [str(val) for val in y_raw]
    name="Feature Contribution"
    textposition = "outside"
    connector = {"line":{"color":"rgb(63, 63, 63)"}}

    fig = go.Figure(go.Waterfall(
    name = name, orientation = "v",
    measure = measures,
    x = x,
    textposition = textposition,
    text = text,
    y = y,
    connector = connector,
    decreasing = {"marker":{"color":"Maroon", "line":{"color":"red", "width":2}}},
    increasing = {"marker":{"color":"Teal"}},
    totals = {"marker":{"color":"deep sky blue", "line":{"color":'blue', "width":3}}}
     ))

    # fig.update_layout(
    #     plot_bgcolor='#00203FFF',
    #     paper_bgcolor='#ADEFD1FF',
    #     height = 800,
    #     title = "Model Interpretation",
    #     showlegend = True, 
    #     yaxis=dict(range=[-0.75 , 1.75]))
    rng_mean  = np.mean(np.abs(y_raw))
    ymax = max(y_raw)+rng_mean
    ymin = min(y_raw)-rng_mean
    fig.layout.height=700
    fig.layout.showlegend=True
    fig.layout.yaxis=dict(range=[ymin , ymax])
    fig.layout.title = f"Probability of Success {str(pred)[:5]}%"
    # fig.layout.plot_bgcolor='#00203f'   
    # fig.layout.paper_bgcolor='#ADEFD1'

    



    return dcc.Graph(id='sk',figure = fig)

def get_predict(launch_date , deadline_date , goal , subcategory , category , currency , country , description, rewards):
    pred_dict={
    "launched_at":launch_date,
    "deadline":deadline_date, 
    "goal":int(goal),
    "sub_category":subcategory,
    "category":category,
    "currency":currency,
    "location_country":country,
    "blurb":description, 
    "rewards":[] 
    }
    try:
        for reward in rewards.split(","):
            pred_dict["rewards"].append(int(reward))
    except Exception as e:
        raise Exception(f"Error sanatizing rewards with {e} error")

    return pred_dict

sample_campaign={
    'description':"""An encrypted dead man's switch service, designed to enable the targeted exposure of user submitted data.""",
    'launch_date':dt(2019, 11, 6),
    "deadline":dt(2019, 11, 6),
    "rewards":"7,10,15,20,65,75,85,90,175,3000",
    'category':'technology',
    'sub_category':'gadgets',
    'currency':'GBP',
    'country': 'the United Kingdom',
    'goal':56292
}