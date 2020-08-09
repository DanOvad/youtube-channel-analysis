import requests
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# api_key is stored in config.py
import config
import networkx as nx

import collections


def graph_channels(channel_response):
    
    # Dictionary comprehension to create channelId:featuredChannelUrls data structure
    channel_network = {channel['id']:channel['brandingSettings']['channel']['featuredChannelsUrls'] \
                       if 'featuredChannelsUrls' in channel['brandingSettings']['channel'] else [] \
                       for channel in channel_response}

    # Dict Comp to create channelId:Channelname data structure
    channel_names = {channel['id']:channel['snippet']['title'] \
                       if 'title' in channel['snippet'] else [] \
                       for channel in channel_response}
    
    channel_ids = [channel['id'] for channel in channel_response]
    
    # Create a Directional Graph from the channel network
    g = nx.DiGraph(channel_network)
    
    
    
    # Create positional values using networkx.drawing.layout functions
    pos = nx.drawing.layout.spring_layout(g)
    #POS = nx.drawing.layout.circular_layout(G)
    
    # Plot the graph
    plt.figure(figsize = (12,12))
    nx.draw_networkx(g,
                 with_labels=True,
                     pos=pos,
                 labels=channel_names,
                 font_size=12, font_color = 'red')
    return g


def simple_page_rank(g):
    a = nx.adjacency_matrix(g)
    n, _ = a.shape
    v0 = np.ones(n) / n
    for i in range(20):
        v1 = a @ v0
        v1 /= v1.sum(0)
        print(np.linalg.norm(v1 - v0))
        v0 = v1
    return v1


def extract_connected_components():
    sizes = []
    ccs = []
    for cc in nx.connected_components(G.to_undirected()):
        ccs.append(cc)
        sizes.append(len(cc))
    print(sorted(sizes))
    return ccs#collections.Counter(sizes)


def plotly_network_graph(g):
    '''"Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>"'''
    edge_x = []
    edge_y = []
    for edge in H.edges():
        x0, y0 = H.nodes[edge[0]]['pos']
        x1, y1 = H.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    node_x = []
    node_y = []
    for node in H.nodes():
        x, y = H.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    
    
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title='<br>Network graph made with Python',
                    titlefont_size=16,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text=f"Graph of connected channels",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()