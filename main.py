import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from dash.exceptions import PreventUpdate

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

import plotly.graph_objects as go


# Search for the default value which will be "Corridor Crew"
#SEARCH_DETAILS_ITEMS_LIST = youtube_requests.youtube_channel_details_by_search("corridor crew", 10)

# Graph the network of channels
#G = network_graphs.create_nx_graph(SEARCH_DETAILS_ITEMS_LIST, directed=True)

# Graph G
#FIG = network_graphs.plotly_network_graph(G, color_setting='Connections')

BLANK_FIG = go.Figure()
##
FEATURES = ['id','title','outDegree','subscribers','views', 'videos']

#CHANNELS_DETAILS_LIST = data_processing.extract_channel_details(SEARCH_DETAILS_ITEMS_LIST)
#DF = data_processing.create_df_from_details_list(CHANNELS_DETAILS_LIST)

def run_update_search_DF(query):
    print("run_update_search_DF")
    search_details_items_list = youtube_requests.youtube_channel_details_by_search(query, 10)
    channels_details_list = data_processing.extract_channel_details(search_details_items_list)
    df = data_processing.create_df_from_details_list(channels_details_list)
    df = df[FEATURES]
    return df

#DF = run_update_search_DF("corridor crew")
# Define External Stylesheet

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css','https://use.fontawesome.com/releases/v5.8.1/css/all.css']
#{
#    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
#    'rel': 'stylesheet',
#    'integrity': 'sha384-#50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
#    'crossorigin': 'anonymous'
#}#'href':'https://use.fontawesome.com/releases/v5.8.1/css/all.css', 
    #'rel':'icon'
#]
#https://use.fontawesome.com/releases/v5.8.1/css/all.css
#external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']#['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Instantiate Dash app

app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets, 
                meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

# Define app layout
app.layout = html.Div(children=[
    html.Div(id='header_section',style={'backgroundColor':'#EFDDEF',
                                        "border":"1px black solid"},
        children=
            [
                html.H1(style ={"margin":dict(b=20,l=30,r=100,t=40)},
                    children=[
                        html.I(className="fab fa-youtube",
                                    style={'size':'14px','color':'#FF0000'}),
                        ' YouTube Network through Featured Channels'
                    ],
                ),
                html.H5(
                    children='''
                    A tool to graph how YouTube channels are connected through featured channels
                    ''')#, style={"border":"2px black solid"})
             ]
    ),
    
    # FIRST SECTION
    html.Div(id='search-channel-section',
             className='row',
             
        children=[
            html.Div(id='search-section-input', 
                className='six columns',
                #style = {"border":"1px black solid"},
                ##        "margin-left": "30px"},
                children=[
                    html.H5('Part One - Search Channels'),
                    html.P(children='Type in a search query and hit search to see a list of channels.'),
                    html.Div(id = 'box-one',
                            #className='six columns',
                            style = {"border":"1px black solid"},
                        children=[
                            dcc.Input(
                                id="channel_search_input",
                                type="text",
                                #value='Corridor Crew',
                                #value='Corridor Crew',
                                placeholder="Search channels"),
                            html.Button('Search', id='submit-val',n_clicks=0)
                        ]

                    )
                ]
            ),
            html.Div(id='right-side',
                className='six columns',
                children=[html.H5(children='Part Two - Select Channels'),
                    html.P(children='Select channels to graph'),

                    html.Div(style = {"border":"1px black solid"},
                        children=[
                            dash_table.DataTable(id='datatable-interactive',
                                columns=[{"name": column, "id": column, "selectable":True} \
                                         for column in FEATURES],
                                css=[{"selector": ".show-hide", "rule": "display: none"}],
                                # Hide the id column, but need it to generate selected list
                                hidden_columns=['id'],

                                # Call Back replaces this field 
                                data=None,#DF.to_dict('records'),

                                filter_action='native',
                                #sort_action="multi",
                                sort_mode="single",
                                row_selectable='multi',
                                page_action='native',
                                page_current=0,
                                page_size=10,
                                style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                style_cell_conditional=[
                                    {'if': {'column_id': c},
                                        'textAlign': 'left'
                                    } for c in ['title']
                                ],
                                style_as_list_view=True
                            )
                        ]
                    )
                         
                ]
            )
            

            
            
        ]
             
        # SECOND SECTION
    ),
    html.Div(id='section-section',
        className='row',
        children=[
            html.Div(id='selected-channel-table',
                className='six columns',
                children=[
                    html.Div(id='selection-container',className='row',
                    children=[
                        html.Div(children=[
                                html.P(children='You selected the following channels:'),
                                html.Div(style = {"border":"1px black solid"},
                                    children = [
                                        dash_table.DataTable(id='selected-data-table',
                                        style_as_list_view=True,
                                        style_cell={
                                            'whiteSpace': 'normal',
                                            'height': 'auto',
                                        },
                                        style_cell_conditional=[
                                            {'if': {'column_id': c},
                                                'textAlign': 'left'
                                            } for c in ['title']
                                        ],
                                        css=[{"selector": ".show-hide", "rule": "display: none"}],
                                        columns=[{"name": column, "id": column, "selectable":True} for column in FEATURES],
                                        hidden_columns=['id'])
                                    ]
                                )
                            ]
                        )
                    ]
                    ),

                html.Div(className='row',children=[
                    html.H5(children='Part Three - Select Distance'),
                    html.P(children='Select the max distance to crawl and hit "Network"'),
                    dcc.Dropdown(id='dropdown-max-degree',
                        className='six columns',
                        options=[
                            {'label': '1', 'value': 1},
                            {'label': '2', 'value': 2},
                            {'label': '3', 'value': 3},
                            {'label': '4', 'value': 4}
                            #,{'label': '5', 'value': 5},
                            #{'label': '6', 'value': 6}
                        ],
                        placeholder='select max degree'
                        #,value=3
                    ),html.Button('Network', 
                                  id='network-button',
                                  n_clicks=0, 
                                  className='six columns')
                ])
                ]
            )
            
        ]
    ),
    html.Div(children=[
        dcc.Store(id='channel-items-store'),
        dcc.Store(id='graph-dict-store'),
        html.Div(id='results-section'),
        html.Div(id='graph_network',
                 style = dict(visibility='hidden'),
                 children=[
        dcc.Graph(
            id='plotly',
            style={'height': '100vh','width': '100%','textAlign': 'center'},
            figure=BLANK_FIG,
            responsive=True
            )
        ])
    ])
    
])
app.title = "YouTube Featured Network"
server = app.server

# Hide graph
@app.callback(
    dash.dependencies.Output('graph_network','style'),
    [dash.dependencies.Input('plotly','figure')]
)
def hide_graph(fig):
    print("Checking hide graph")
    if fig is None:
        print("Fig is none")
    if fig['data'] != []:
        print("fig data is empty list")
        return None
    else:
        print("hiding figure")
        return dict(visibility='hidden')#display='none')



# Update Search DataTable with response
@app.callback(
    dash.dependencies.Output('datatable-interactive', 'data'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel_search_input', 'value')]
)
def display_search_table(n_clicks, value):
    if value is None:
        print("Search Value  Is None")
        return None
    print(f"Searching {value}")
    print("Ran Update Search datatable")
    df = run_update_search_DF(value)
    return df.to_dict('records')

# Display Channels to network (Selected Datatable)
@app.callback(
    dash.dependencies.Output('selected-data-table','data'),
    [dash.dependencies.Input('datatable-interactive','selected_row_ids'),
    dash.dependencies.Input('datatable-interactive','data')]
)
def update_selected_datatable(selected_row_ids, data):
    if data is None:
        print("Update_selected_datatable is None")
        raise PreventUpdate
        return None
    else:
        df = pd.DataFrame(data)
        if selected_row_ids is None:
            print("No row Selected")
            return None
        selected_channel_boolean = (df['id'].isin(selected_row_ids))
        return df[selected_channel_boolean].to_dict('records')

# Generate Network Channel Dictionary for Items Store
@app.callback(
        dash.dependencies.Output('channel-items-store','data'),
        [dash.dependencies.Input('network-button','n_clicks')],
        [dash.dependencies.State('selected-data-table','derived_viewport_row_ids'),
        dash.dependencies.State('dropdown-max-degree','value')])
def store_items(n_clicks, row_ids,value):
    if row_ids is None:
        print("row_ids Is None - Update Network")
        return None
    channels_details_items_list = youtube_requests.youtube_channel_details_by_network(row_ids,value)
    return channels_details_items_list


# Store graph positional dictionary
@app.callback(dash.dependencies.Output('graph-dict-store','data'),
[dash.dependencies.Input('channel-items-store','data')])
def store_graph_dict(data):
    if data is None:
        #raise PreventUpdate
        print("Data is None")
        raise PreventUpdate
    else:
        print("Calculating position dictionary")
        g = network_graphs.create_nx_graph(data)
        pos_dict = {g.nodes[node]['id']:g.nodes[node]['pos'] for node in g.nodes()}
        
    print("Finished calculating position")
    return pos_dict
    
## Generate Graph from Items store and create Graph Store
#  Also need to figure out where betweeness will be calculated. 
#   Will the dataframe be generated after both items-store and graph-store are created?
#   graph-stats are stored at first in graph-store. Create DF using items-store, then add in graph-store?


# Print out Results to Results-section
@app.callback(
        dash.dependencies.Output('results-section','children'),
        [dash.dependencies.Input('channel-items-store','data')])
def return_states(data):
    if data is None:
        raise PreventUpdate
        return None
    network_size = len(data)
    origin_size = len([channel['id'] for channel in data if channel['distance'] == 0])
    g = network_graphs.create_nx_graph2(data)
    return html.Div(f"You Selected {origin_size} channels; displaying results for network with {network_size} nodes")


        
# Callback to generate figure from Graph Store
@app.callback(
    dash.dependencies.Output('plotly','figure'),
    [dash.dependencies.Input('graph-dict-store','data')],
    [dash.dependencies.State('channel-items-store','data')]
    )
def update_network(pos_data, channel_data):
    if pos_data is None:
        print("No position Data")
    if channel_data is None:
        #raise PreventUpdate
        print("row_ids Is None - Update Network")
        return BLANK_FIG
    else:
        g = network_graphs.create_nx_graph2(channel_data)
        nx.set_node_attributes(g, pos_data, name='pos')
        #pos_dict = {g.nodes[node]['id']:g.nodes[node]['pos'] for node in g.nodes()}
        fig = network_graphs.plotly_network_graph(g, 'Distance')
        return fig
    
# Callback to generate Data Table from items store and graph store
    
# Callback to generate SCC from Graph Store

# Callback to generate Page Rank graph from Graph Store
# Callback to generate In-Degree Centrality graph from Graph Store
# Callback to generate Betweenness Centrality graph from Graph Store

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)