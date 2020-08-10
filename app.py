import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import numpy as np
import requests
import json
import networkx as nx
import matplotlib.pyplot as plt
#import seaborn as sns

import config
import youtube_requests
import data_processing
import network_graphs

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with open('data/corridor_five.json','r') as json_file:
    CORRIDOR_FULL = json.load(json_file)
    
with open('data/corridor_network.json','r') as json_file:
    CHANNELS_DETAILS_ITEMS_LIST = json.load(json_file)

# Get a list of dictionaries, where each dictionary represents details for a specific channel
#CHANNELS_DETAILS_ITEMS_LIST = youtube_requests.youtube_channel_details_by_network(CORRIDOR_FULL, 1)

# Graph the network of channels
G = network_graphs.create_nx_graph(CHANNELS_DETAILS_ITEMS_LIST, True)

# Extract a columnar list of channel details
#CHANNELS_DETAILS_LIST = data_processing.extract_channel_details(CHANNELS_DETAILS_ITEMS_LIST)

# Create a dataframe
#DF = data_processing.create_df_from_details_list(CHANNELS_DETAILS_LIST)

# Graph G
fig = network_graphs.plotly_network_graph(G)
#fig2 = network_graphs.graph_nx_graph(G)


app.layout = html.Div(children=[
    html.H1(children='Corridor Digital Channel Network'),

    html.Div(children='''
        A directed graph of featured youtube channels
    '''),
    html.Div(children=[
        dcc.Graph(
            id='plotly',
            figure=fig,
            #className = 'six columns',
            responsive=True
        )
    ])
])
    

if __name__ == '__main__':
    app.run_server(debug=True)