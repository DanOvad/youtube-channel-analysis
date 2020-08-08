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
def request_youtube_search_channels(query, n):
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
        #print(len(set(channel['id']['channelId'] for channel in channel_list)))
    return channel_list

#CHANNEL_LIST = request_youtube_search_channels('Minecraft',23)

# Extract Channel Ids from the list of dictionaries
#CHANNELID_LIST = [channel['snippet']['channelId'] for channel in CHANNEL_LIST]

# Get channel details and snippet
def request_channel_list(channelid_list):
    
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
#CHANNEL_RESP = request_channel_list(CHANNELID_LIST)