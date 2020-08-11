import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

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

#with open('data/corridor_five.json','r') as json_file:
#    CORRIDOR_FULL = json.load(json_file)
    
#with open('data/corridor_network.json','r') as json_file:
#    CHANNELS_DETAILS_ITEMS_LIST = json.load(json_file)
   
with open('data/corridor_search.json','r') as json_file:
    SEARCH_DETAILS_ITEMS_LIST = json.load(json_file)

    
#CHANNELS_DETAILS_ITEMS_LIST = youtube_requests.youtube_channel_details_by_search('corridor crew',10)
    
# Get a list of dictionaries, where each dictionary represents details for a specific channel
#CHANNELS_DETAILS_ITEMS_LIST = youtube_requests.youtube_channel_details_by_network(CORRIDOR_FULL, 1)

# Graph the network of channels
G = network_graphs.create_nx_graph(SEARCH_DETAILS_ITEMS_LIST, True)

# Extract a columnar list of channel details
#CHANNELS_DETAILS_LIST = data_processing.extract_channel_details(CHANNELS_DETAILS_ITEMS_LIST)

# Create a dataframe
#DF = data_processing.create_df_from_details_list(CHANNELS_DETAILS_LIST)

# Graph G
FIG = network_graphs.plotly_network_graph(G)
#fig2 = network_graphs.graph_nx_graph(G)


CHANNELS_DETAILS_LIST = data_processing.extract_channel_details(SEARCH_DETAILS_ITEMS_LIST)

DF = data_processing.create_df_from_details_list(CHANNELS_DETAILS_LIST)

FEATURES = ['id','title','subscriberCount','viewCount','featuredChannelsCount']
DF = DF[FEATURES]
CHANNEL_ID_LIST = []



app.layout = html.Div(children=[
    html.H1(children='Corridor Digital Channel Network'),

    html.Div(children='''
        A directed graph of featured youtube channels
    '''),
    
    html.Div(className='row',children=
        [
            html.Div(className='six columns',children=
                [
                    dcc.Input(
                        id="channel_search_input",
                        type="text",
                        value="corridor",
                        placeholder="Search for relevant youtube channels"),
                    html.Div(id='search_output'),
                    html.Button('Search', id='submit-val',n_clicks=0),
                    html.Div(id='container-button-basic',
                        children='Enter a value and press submit')
                ]
            ),
            html.Div(className='six columns',
                    children=[
                        dash_table.DataTable(id='datatable-interactive',
                            columns=[{"name": i, "id": i, "selectable":True} for i in DF[FEATURES].columns],
                            data=DF.to_dict('records'),
                            filter_action='native',
                            #sort_action="multi",
                            sort_mode="single",
                            row_selectable='multi',
                            page_action='native',
                            page_current=0,
                            page_size=10
                        )
                    ]
            )
            
        ]),
    html.Div(id='channels_selected',className='row',children=''),
    html.Button('Network', id='submit_list',n_clicks=0),

    #html.Div(id='datatable-interactivity-container', children='string for container'),
    
    html.Div(id='graph_network',children=[
        dcc.Graph(
            id='plotly',
            figure=FIG,
            className ='six columns',
            responsive=True
        )
    ])
                        #className='six columns')
    
])

# Callback to update debugging for dcc.input
@app.callback(
    Output(component_id='search_output',component_property='children'),
    [Input(component_id='channel_search_input',component_property='value')]
)
def update_output_div(input_value):
    return f'Output: {input_value}'


# Call back for debugging html.Button
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel_search_input', 'value')])
def update_output(n_clicks, value):
    
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )


# Callback to update data table with search results
@app.callback(
    dash.dependencies.Output('datatable-interactive', 'data'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel_search_input', 'value')])
def update_output_table(n_clicks, value):
    
    print("Ran Update")
    
    # For a search query and number of results, get back a list of dictionaries of channel details
    channels_details_items_list = youtube_requests.youtube_channel_details_by_search(value,10)
      
    # Flatten the data and place into DataFrame
    channels_details_list = data_processing.extract_channel_details(channels_details_items_list)
    DF = data_processing.create_df_from_details_list(channels_details_list)
    
    # Subset the data, if we don't datatypes cause problems in dash_table.DataTable
    #features = ['id','title','subscriberCount','viewCount','featuredChannelsCount']
    DF = DF[FEATURES]
    
    return DF.to_dict('records')

@app.callback(
    dash.dependencies.Output('channels_selected','children'),
    [dash.dependencies.Input('datatable-interactive','selected_row_ids')])
def selected_rows(selected_row_ids):
    if selected_row_ids is None:
        print("No row Selected")
        return None
    else:
        print("Selected a row")
        return selected_row_ids


@app.callback(
    dash.dependencies.Output('plotly','figure'),
[dash.dependencies.Input('submit_list','n_clicks')],
[dash.dependencies.State('channels_selected','children')])

def update_network(n_clicks,children):
    if len(children) == 0:
        return FIG
    else:
        print(f'Running with {len(children)} channels')
        channels_details_items_list = youtube_requests.youtube_channel_details_by_network(children,4)
        g = network_graphs.create_nx_graph(channels_details_items_list)    

    return network_graphs.plotly_network_graph(g)

if __name__ == '__main__':
    app.run_server(debug=True)