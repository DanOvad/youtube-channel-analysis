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

def determine_max_result_list(n, batch_size):
    '''Function to return a list of max results parameters for a specific number of requests and batch_sizes.
    
    For example: (123,50) returns [50,50,23]'''
    # Logic to determine maxResults parameter
    if n%50 == 0:
        request_size_list = [batch_size]*(n//batch_size)
    # Determine a list of request sizes []
    else:
        request_size_list = [batch_size]*(n//batch_size) + [n%batch_size]
    return request_size_list

# Search for channels by a specific query
def youtube_request_search_channels(query, n):
    '''Returns a list of n channels that match the query.\n
    Uses /youtube/v3/search'''
    
    request_size_list = determine_max_result_list(n,50)
        
    # Empty list to store 50 items from each response
    channel_list = list()
    
    # Instantiate nextPageToken, when '' method interprets null
    nextPageToken = ''


    for request_size in request_size_list:
        
        # Create request object
        resp = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params=dict(part='snippet', 
                        type='channel',
                        maxResults=request_size,
                        pageToken=nextPageToken,
                        q=query,
                        key=config.api_key)
        )
        assert resp.ok
        nextPageToken = json.loads(resp.content)['nextPageToken']
        channel_list.extend(json.loads(resp.content)['items'])
    return channel_list



# Get channel details and snippet
def youtube_request_channel_list(channelid_list):
    
    # Check for non-unique elements
    if len(channelid_list) != len(set(channelid_list)):
        print("There are non-unique elements in this list")
        
    # Determine request size list
    request_size_list = determine_max_result_list(len(set(channelid_list)),50)

    # Instantiate channel response list
    channel_resp_list = []
    
    # Set the start_index to 0
    start_index = 0
    # Loop 
    for request_size in request_size_list:
        
        # Debug
        #print(request_size_list, request_size, start_index, start_index+request_size)
        
        resp = requests.get(
            'https://www.googleapis.com/youtube/v3/channels',
            params=dict(part='contentDetails, snippet, statistics,\
                        brandingSettings, topicDetails, status, id, contentOwnerDetails',
                    id=channelid_list[start_index:start_index+request_size],
                    maxResults=50,
                    key=config.api_key)
        )
        # Increase the start_index
        start_index += request_size
        
        # Extend channel response list
        channel_resp_list.extend(json.loads(resp.content)['items'])
        
    return channel_resp_list

### Pulling channel details by search
def youtube_channel_details_by_search(query, n):
    '''Returns a details list of channels for a specific search query and number of requested results.'''
    # Load cached dictionary with {key:value} is {query string:response_items}
    with open('data/query_cache.json','r') as query_cache:
        query_cache_dict = json.load(query_cache)
        
    if query in query_cache_dict:
        channel_details_items_list = query_cache_dict[query]
        print("Already seen this query")
    else:
        print("Haven't seen this query yet")
        # API REQUEST (quota cost 100)
        channels_list = youtube_request_search_channels(query,n)

        # Retrieve Channel Ids from the list of dictionaries
        channels_id_list = [channel['snippet']['channelId'] for channel in channels_list]

        # API REQUEST (quota cost 1) Request details for all channels in a list of channelIds
        channels_details_items_list = youtube_request_channel_list(channels_id_list)

        # Extract channel details to a list of dictionaries for pandas
        #channels_details_list = extract_channel_details(channels_detail_items_list)
        
        query_cache_dict[query] = channels_details_items_list
        with open('data/query_cache.json','w') as query_json:
            json.dump(query_cache_dict, query_json)
    
    channels_list = youtube_request_search_channels(query,n)

    # Retrieve Channel Ids from the list of dictionaries
    channels_id_list = [channel['snippet']['channelId'] for channel in channels_list]

    # Request details for all channels in a list of channelIds
    channels_details_items_list = youtube_request_channel_list(channels_id_list)

    # Extract channel details to a list of dictionaries for pandas
    #channels_details_list = extract_channel_details(channels_detail_items_list)
    
    return channels_details_items_list



def extract_featured_channels(channels_details_items_list):
    ''' Function to extract a set of featured channelIds from a list of channelIds'''
    
    featured_channels_id_list = list()
    channels_wo_features_count = 0
    for channel in channels_details_items_list:

        if 'featuredChannelsUrls' in channel['brandingSettings']['channel']:
            featured_channels_id_list.extend(channel['brandingSettings']['channel']['featuredChannelsUrls'])
        else:
            channels_wo_features_count +=1
    print(f'{len(set(featured_channels_id_list))} total neighbors; {channels_wo_features_count} out of {len(channels_details_items_list)} channels do not feature channels')
    return list(set(featured_channels_id_list))



def youtube_channel_details_by_network(channels_details_items_list, max_degree):
    
    network_channels_id_set = set([channel['id'] for channel in channels_details_items_list])
    
    # get a response for the list of channel Ids
    #channel_resp = youtube_request_channel_list(channelid_list)
    
    # Instantiate the output, a list of dictionaries, each dict represents a channel
    network_channels_items_list = []
    
    # Add our origin channel responses
    network_channels_items_list.extend(channels_details_items_list)
    
    # Instantiate a neighbors channel response
    neighbors_channels_items_list = channels_details_items_list
    
    # Loop over each degree of separate (breadth first search)
    for degree in range(1,max_degree+1):
        
        # Extract a list of featured channels ids
        neighbors_channels_id_set = set(extract_featured_channels(neighbors_channels_items_list))
        added_channels_id_set = neighbors_channels_id_set.difference(
                                    network_channels_id_set.intersection(
                                        neighbors_channels_id_set))
        
        network_channels_id_set = added_channels_id_set | network_channels_id_set
        #print(added_channels_id_set)
        
        # Request channel details from Youtube using list of channel ids
        neighbors_channels_items_list = youtube_request_channel_list(list(added_channels_id_set))
        
        # Add n-degree channel details response
        network_channels_items_list.extend(neighbors_channels_items_list)
        
        
        
        
    return network_channels_items_list