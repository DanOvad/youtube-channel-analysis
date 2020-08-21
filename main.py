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

# Instantiate Dash app as "app"
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
                html.H1(style ={"margin":dict(b=20,l=40,r=10,t=40)},
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
    html.Div(id='search-channel-section',className='row',
        children=[
            html.Div(id='search-section-input', 
                    className='six columns',
                children=[
                    html.H5('Part 1 - Search Channels'),
                    html.P(children='Type in a search query and hit search to see a list of channels.'),
                    html.Div(id = 'box-one',
                            #className='six columns',
                            style = {"border":"1px black solid"},
                        children=
                    [
                        dcc.Input(
                            id="channel_search_input",
                            type="text",
                            #value='Corridor Crew',
                            #value="corridor crew",
                            placeholder="Search channels"),
                        html.Button('Search', id='submit-val',n_clicks=0)
                    ]
                         
                    ),
                                        html.H5(children='Part Two - Select Channels'),
                    html.P(children='Select which channels you want to graph"'),

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
            ),
            
            html.Div(id='selected-channel-table',
                     className='six columns',
                children=[
                    html.Div(id='selection-container',className='row',
                    children=[
                        html.Div(
                            children=[
                                html.P(children='You selected the following channels:'),
                                html.Div(style = {"border":"1px black solid"},
                                    children = [dash_table.DataTable(id='selected-data-table',
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
                    html.P(children='Select the max distance to crawl and hit "Network"'),
                    dcc.Dropdown(id='dropdown-max-degree',
                        className='six columns',
                        options=[
                            {'label': '1', 'value': 1},
                            {'label': '2', 'value': 2},
                            {'label': '3', 'value': 3},
                            {'label': '4', 'value': 4},
                            {'label': '5', 'value': 5},
                            {'label': '6', 'value': 6}
                        ],
                        placeholder='select max degree'
                        #,value=3
                    ),html.Button('Network', id='network-button',n_clicks=0, className='six columns')
                ])
                ]
            )
            
            
        ]
    ),
    #
    html.Div(id='graph_network',children=[
        dcc.Graph(
            id='plotly',
            style={'height': '100vh','width': '100%','textAlign': 'center'},
            #style={'height': '100vh','w},
            figure=BLANK_FIG,
            responsive=True
        )
    ])
    
])

server = app.server

@app.callback(
    dash.dependencies.Output('graph_network','style'),
    [dash.dependencies.Input('plotly','figure')]
)
def hide_graph(fig):
    if fig['data'] != []:
        return None
    else:
        return dict(visibility='hidden')#display='none')



# Callback to update data table with search results
@app.callback(
    dash.dependencies.Output('datatable-interactive', 'data'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('channel_search_input', 'value')])
def display_search_table(n_clicks, value):
    if value is None:
        print("Search Value  Is None")
        return None
    print(value)
    print("Ran Update Search datatable")
    df = run_update_search_DF(value)
    return df.to_dict('records')


@app.callback(
    dash.dependencies.Output('selected-data-table','data'),
    [dash.dependencies.Input('datatable-interactive','selected_row_ids'),
    dash.dependencies.Input('datatable-interactive','data')])
  
def update_selected_datatable(selected_row_ids, data):
    if data is None:
        print("Update_selected_datatable is None")
        return None
    else:
        df = pd.DataFrame(data)
        if selected_row_ids is None:
            print("No row Selected")
            return None
        selected_channel_boolean = (df['id'].isin(selected_row_ids))
        return df[selected_channel_boolean].to_dict('records')

@app.callback(
    dash.dependencies.Output('plotly','figure'),
    [dash.dependencies.Input('network-button','n_clicks')],
[dash.dependencies.State('selected-data-table','derived_viewport_row_ids'),
dash.dependencies.State('dropdown-max-degree','value')])



def update_network(n_clicks,row_ids, value):
    print("Ran Update Network graph")
    print(value)
    if row_ids is None:
        print("row_ids Is None - Update Network")
        return BLANK_FIG
    else:
        print(f'Running with {len(row_ids)} channels')
        channels_details_items_list = youtube_requests.youtube_channel_details_by_network(row_ids,value)
        g = network_graphs.create_nx_graph(channels_details_items_list)
        fig = network_graphs.plotly_network_graph(g, 'Distance')
        return fig

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8080, debug=True, use_reloader=True)