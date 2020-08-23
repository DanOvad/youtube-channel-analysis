import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# api_key is stored in config.py
import networkx as nx

import plotly.graph_objects as go

import time


def create_nx_graph2(channel_response, directed = True):
    '''Takes in a list of channel details response items and returns a graph object in networkX.
    
    Specifically subsets only those channels queried.
    
    channel_response: list of dictionaries, each entry represents a channel node;
    directed: boolean, if true produces a directed graph instead of a undirected graph.'''
    
    # Create dictionary to instantiate graph
    channel_network = {channel['id']:channel['brandingSettings']['channel']['featuredChannelsUrls'] \
                       if 'featuredChannelsUrls' in channel['brandingSettings']['channel'] else [] \
                       for channel in channel_response}

    # Create dictionary to attribute names
    channel_names = {channel['id']:channel['snippet']['title'] \
                     if 'title' in channel['snippet'] else [] \
                     for channel in channel_response}
    
    # Create dictionary to attribute subscribeCount
    subscriber_count_dict = {channel['id']:int(channel['statistics']['subscriberCount']) \
                             for channel in channel_response}
    
    t0=time.clock()
    # Create a Directional Graph from the channel network
    g = nx.DiGraph(channel_network)
    t1 = time.clock()-t0
    print("Time elapsed create graph: ",t1)
    
    t0=time.clock()
    # Create a list of channelIds to subset the graph
    channel_ids = [channel['id'] for channel in channel_response]
    channel_id_dict = {channel_id:channel_id for channel_id in channel_ids}
    
    t1 = time.clock()-t0
    print("Time elapsed channelId list: ",t1)
    
    # Create a dictionary of distance
    distance_dict = {channel['id']:channel['distance'] \
                     if 'distance' in channel\
                     else '' for channel in channel_response}
    
    # Subset created graph to only include channels we have details on
    if directed == True:
        h = g.subgraph(channel_ids)#.to_undirected()
        # In-degree Centrality only matters for Directed graphs
        in_degree_dict = {node:h.in_degree()[node] for node in h.nodes()}
        
        # Set attribute for in_degree
        nx.set_node_attributes(h,
                               values=in_degree_dict,
                               name='in_degree')
    else:
        
        
        h = g.subgraph(channel_ids)#.to_undirected()

        
    # Set node attributes to include position
    #pos = nx.drawing.layout.spring_layout(g)
    #pos = nx.nx.drawing.layout.fruchterman_reingold_layout(g)
    
    #t0=time.clock()
    
    # Assigning positional layout
    #pos = nx.drawing.layout.kamada_kawai_layout(h)
    #nx.set_node_attributes(g, pos, name='pos')
    #t1 = time.clock()-t0
    
    print("Time elapsed determine position: ",t1)
    t0=time.clock()
    # Set attribute for names
    nx.set_node_attributes(h, channel_names, name='title')
    # Set attribute for SubscribeCount
    nx.set_node_attributes(h, subscriber_count_dict, name='subscriberCount')
    # Set the Id as an attribute
    nx.set_node_attributes(h, channel_id_dict, name='id')
    # Set the distance of each node
    nx.set_node_attributes(h, distance_dict, name='distance')
    t1 = time.clock()-t0
    print("Time elapsed Setting Attributes: ",t1)
    return h




### ORIGINAL
def create_nx_graph(channel_response, directed = True):
    '''Takes in a list of channel details response items and returns a graph object in networkX.
    
    Specifically subsets only those channels queried.
    
    channel_response: list of dictionaries, each entry represents a channel node;
    directed: boolean, if true produces a directed graph instead of a undirected graph.'''
    
    # Create dictionary to instantiate graph
    channel_network = {channel['id']:channel['brandingSettings']['channel']['featuredChannelsUrls'] \
                       if 'featuredChannelsUrls' in channel['brandingSettings']['channel'] else [] \
                       for channel in channel_response}

    # Create dictionary to attribute names
    channel_names = {channel['id']:channel['snippet']['title'] \
                     if 'title' in channel['snippet'] else [] \
                     for channel in channel_response}
    
    # Create dictionary to attribute subscribeCount
    subscriber_count_dict = {channel['id']:int(channel['statistics']['subscriberCount']) \
                             for channel in channel_response}
    
    t0=time.clock()
    # Create a Directional Graph from the channel network
    g = nx.DiGraph(channel_network)
    t1 = time.clock()-t0
    print("Time elapsed create graph: ",t1)
    
    t0=time.clock()
    # Create a list of channelIds to subset the graph
    channel_ids = [channel['id'] for channel in channel_response]
    channel_id_dict = {channel_id:channel_id for channel_id in channel_ids}
    
    t1 = time.clock()-t0
    print("Time elapsed channelId list: ",t1)
    
    # Create a dictionary of distance
    distance_dict = {channel['id']:channel['distance'] \
                     if 'distance' in channel\
                     else '' for channel in channel_response}
    
    # Subset created graph to only include channels we have details on
    if directed == True:
        h = g.subgraph(channel_ids)#.to_undirected()
        # In-degree Centrality only matters for Directed graphs
        in_degree_dict = {node:h.in_degree()[node] for node in h.nodes()}
        
        # Set attribute for in_degree
        nx.set_node_attributes(h,
                               values=in_degree_dict,
                               name='in_degree')
    else:
        
        
        h = g.subgraph(channel_ids)#.to_undirected()

        
    # Set node attributes to include position
    #pos = nx.drawing.layout.spring_layout(g)
    #pos = nx.nx.drawing.layout.fruchterman_reingold_layout(g)
    
    t0=time.clock()
    
    # Assigning positional layout
    pos = nx.drawing.layout.kamada_kawai_layout(h)
    nx.set_node_attributes(g, pos, name='pos')
    t1 = time.clock()-t0
    
    print("Time elapsed determine position: ",t1)
    t0=time.clock()
    # Set attribute for names
    nx.set_node_attributes(h, channel_names, name='title')
    # Set attribute for SubscribeCount
    nx.set_node_attributes(h, subscriber_count_dict, name='subscriberCount')
    # Set the Id as an attribute
    nx.set_node_attributes(h, channel_id_dict, name='id')
    # Set the distance of each node
    nx.set_node_attributes(h, distance_dict, name='distance')
    t1 = time.clock()-t0
    print("Time elapsed Setting Attributes: ",t1)
    return h

def graph_nx_graph(g):
    
    #pos = nx.drawing.layout.spring_layout(g)
    # Plot the graph
    fig = plt.figure()
    #fig = plt.figure(figsize = (12,12))
    nx.draw_networkx(g,
        with_labels=True,
        pos={node:g.nodes()[node]['pos'] for node in g.nodes()},
        labels={node:g.nodes()[node]['title'] for node in g.nodes},
        font_size=12, font_color = 'red')
    plt.close()
    return fig

def simple_page_rank(g):
    a = nx.adjacency_matrix(g)
    n, _ = a.shape
    v0 = np.ones(n) / n
    for i in range(20):
        v1 = a @ v0
        v1 /= v1.sum(0)
        #print(np.linalg.norm(v1 - v0))
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


def plotly_network_graph(g, 
                         color_setting, 
                         title='Graph of Featured Channels', 
                         display_list = []):
    '''"Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>"
    
    Test Test'''
    # Extract a list of channel names from node attributes
    channel_names_list = [g.nodes[node]['title'] for node in g.nodes()]
    if len(display_list) == 0: # Use Origin points
        # Get a list of nodes to display text
        display_list = [g.nodes[node]['id'] for node in g.nodes() if g.nodes[node]['distance'] == 0]
    
    channels_display = [g.nodes[node]['title'] \
                        if g.nodes[node]['id'] in display_list \
                        else None \
                        for node in g.nodes()]
    # Extract list of subscriber counts from node attributes
    subscriber_count_list = [g.nodes[node]['subscriberCount'] for node in g.nodes()]
    
    # Instantiate Edges
    edge_x = []
    edge_y = []
    
    # Cycle through graph edges to generate positions
    for edge in g.edges():
        x0, y0 = g.nodes[edge[0]]['pos']
        x1, y1 = g.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    
    
    # Create Scatter for edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')
    
    
    # Instantiate Nodes
    node_x = []
    node_y = []
    for node in g.nodes():
        x, y = g.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    #
    
    node_size_list = [np.log2(subcount + 1) for subcount in subscriber_count_list]
    
    # Create Scatter for nodes
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=channels_display,
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | @'YlGnBu'@ | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=node_size_list,
            colorbar=dict(
                thickness=15,
                title=color_setting,
                xanchor='left',
                titleside='right'
            ),
            line_width=2))
    node_adjacencies = []
    node_text = []
    node_distance = [g.nodes[node]['distance'] for node in g.nodes()]
    
    for node, adjacencies in enumerate(g.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append(f'{channel_names_list[node]} ({node_distance[node]}) has {str(len(adjacencies[1]))} connections and {subscriber_count_list[node]} subscribers')
    node_distance = [g.nodes[node]['distance'] for node in g.nodes()]
    
    # Set the setting for the
    if color_setting == 'Distance':
        node_trace.marker.color = node_distance
    elif color_setting == 'Connections':
        node_trace.marker.color = node_adjacencies
    else:
        print("Invalid color setting; options: ['Connections','Distance']. Used 'Connections'")
        
    node_trace.hovertext = node_text
    
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    scene=dict(aspectmode="data"),
                    autosize=True,
                    title=title,
                    titlefont_size=16,
                    #width=700,
                    height=550,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    annotations=[ dict(
                        text=f"Size is log(Subscriber Count);<br>Color is {color_setting}",
                        showarrow=False,
                        xref="paper", yref="paper",
                        x=0.005, y=-0.002 ) ],
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    return fig